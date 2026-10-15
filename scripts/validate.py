#!/usr/bin/env python3
"""Validate the draft workbook HTML, DOCX, PDF, and EPUB.

Does not read journal/private/. Run after scripts/build_all.py.
"""

from __future__ import annotations

import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import build_all

ROOT = build_all.ROOT
MIN_BYTES = {
    build_all.HTML_PATH: 5000,
    build_all.DOCX_PATH: 10000,
    build_all.EPUB_PATH: 2000,
    build_all.PDF_PATH: 8000,
}


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def main() -> int:
    configure_stdio()
    failures: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        line = f"{'PASS' if ok else 'FAIL'}  {name}"
        if detail:
            line += f" — {detail}"
        print(line)
        if not ok:
            failures.append(name)

    try:
        build_all.assert_readable(ROOT / "journal" / "private" / "unused.md")
        check("private journal is unread", False, "guard did not refuse the path")
    except SystemExit as exc:
        check("private journal is unread", "Refusing" in str(exc), str(exc))

    try:
        build_all.assert_sources_unchanged()
        check("source DOCX checksums", True)
    except SystemExit as exc:
        check("source DOCX checksums", False, str(exc))

    for path in (build_all.WORKBOOK_CSS, build_all.EPUB_CSS, ROOT / "scripts" / "build_all.py", ROOT / "README.md"):
        check(f"present {path.relative_to(ROOT).as_posix()}", path.is_file())

    workbook_css = (ROOT / "styles" / "workbook.css").read_text(encoding="utf-8") if (ROOT / "styles" / "workbook.css").is_file() else ""
    for token in ("7in", "10in", "#F6F1E7", "#241F1C", "Georgia", "Palatino Linotype", "#FBF8F2", "nav.toc a"):
        check(f"workbook.css includes {token}", token in workbook_css)

    epub_css = (ROOT / "styles" / "epub.css").read_text(encoding="utf-8") if (ROOT / "styles" / "epub.css").is_file() else ""
    for token in ("Georgia", "Palatino Linotype", "#F6F1E7", "#241F1C", "#FBF8F2", "writing-lines"):
        check(f"epub.css includes {token}", token in epub_css)

    try:
        docs, _parts = build_all.load_sources(proof=False)
        chapters = [doc for doc in docs if doc.kind == "chapter"]
        check("real chapter headings", True, f"{len(chapters)} chapter file(s)")
    except SystemExit as exc:
        check("real chapter headings", False, str(exc))

    for path, minimum in MIN_BYTES.items():
        if not path.is_file():
            check(f"exists {path.name}", False, "file is missing")
            continue
        size = path.stat().st_size
        check(f"size {path.name}", size >= minimum, f"{size} bytes")

    html = ""
    if build_all.HTML_PATH.is_file():
        html = build_all.HTML_PATH.read_text(encoding="utf-8")
        check("HTML contents nav", 'id="contents"' in html and 'href="#' in html)
        check("HTML inlines print CSS", "size: 7in 10in" in html and "#F6F1E7" in html)
        check("HTML does not embed a private journal file", "DO_NOT_COMMIT" not in html)
        for anchor in (
            "index-alphabetical",
            "index-time",
            "index-emotional-intensity",
            "index-energy",
            "index-format",
            "index-mood",
            "index-revisit",
        ):
            check(f"HTML index {anchor}", f'id="{anchor}"' in html)
        if (ROOT / "assets" / "parts" / "01-opener.svg").is_file():
            check(
                "HTML part opener art",
                'class="part-art"' in html
                and ("assets/parts/01-opener.svg" in html or "assets/parts/01-opener.jpg" in html),
            )
        if (ROOT / "research" / "BIBLIOGRAPHY.md").is_file():
            check("HTML bibliography", 'id="bibliography"' in html and "Buehlman" in html)
        if "FIXTURE NOT A CHAPTER" in html:
            for token in ('class="journal-spread"', 'class="card-grid"', 'class="writing-lines"', "<table>"):
                check(f"proof HTML has {token}", token in html)

    if build_all.DOCX_PATH.is_file():
        check_docx(build_all.DOCX_PATH, html, check)

    if build_all.EPUB_PATH.is_file():
        check_epub(build_all.EPUB_PATH, html, check)

    if build_all.PDF_PATH.is_file():
        check_pdf(build_all.PDF_PATH, check)

    if failures:
        print(f"FAIL  {len(failures)} check(s)")
        return 1
    print("PASS  validation")
    return 0


def check_docx(path: Path, html: str, check) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            document = archive.read("word/document.xml").decode("utf-8")
            styles = archive.read("word/styles.xml").decode("utf-8") if "word/styles.xml" in names else ""
    except (zipfile.BadZipFile, KeyError, OSError) as exc:
        check("DOCX opens", False, str(exc))
        return
    check("DOCX opens", True)
    check("DOCX content types", "[Content_Types].xml" in names and "word/document.xml" in names)
    check("DOCX title", "The Closer Project" in document)
    check("DOCX Georgia", "Georgia" in styles or "Georgia" in document)
    check("DOCX Palatino Linotype", "Palatino Linotype" in styles or "Palatino Linotype" in document)
    if "FIXTURE NOT A CHAPTER" in html:
        check("DOCX fixture title", "FIXTURE NOT A CHAPTER" in document)
    check("DOCX has no private journal part", not any("journal/private" in name.replace("\\", "/") for name in names))
    check("DOCX indexes", "Alphabetical index" in document and "Generated from the chapter frontmatter" in document)
    if (ROOT / "assets" / "parts" / "01-opener.svg").is_file():
        embedded = any(name.startswith("word/media/") for name in names)
        check("DOCX part opener", embedded or "01-opener.svg" in document)


def check_epub(path: Path, html: str, check) -> None:
    payload = path.read_bytes()
    problems = build_all.epub_mimetype_problems(payload)
    check("EPUB mimetype is first and stored", not problems, "; ".join(problems))
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if "META-INF/container.xml" not in names:
                check("EPUB container.xml", False, "missing")
                return
            container = archive.read("META-INF/container.xml")
            check("EPUB container.xml", b"container" in container and b"content.opf" in container)
            nav_names = [name for name in names if name.endswith("nav.xhtml") or name.endswith("/nav")]
            check("EPUB nav", bool(nav_names), ", ".join(nav_names) or "missing")
            if "OEBPS/content.opf" not in names:
                check("EPUB package", False, "missing content.opf")
                return
            opf = archive.read("OEBPS/content.opf")
            check("EPUB package", b"<manifest" in opf and b"<spine" in opf)
            root = ET.fromstring(opf)
            ns = {"opf": "http://www.idpf.org/2007/opf"}
            hrefs = [node.get("href") for node in root.findall(".//opf:item", ns)]
            missing = [href for href in hrefs if href and f"OEBPS/{href}" not in names]
            check("EPUB manifest files exist", not missing, ", ".join(missing))
            for name in sorted(names):
                if name.endswith((".xhtml", ".opf", ".xml")):
                    ET.fromstring(archive.read(name))
            check("EPUB XML parses", True)
            nav_text = ""
            if nav_names:
                nav_text = archive.read(nav_names[0]).decode("utf-8")
                check("EPUB nav links", "epub:type=\"toc\"" in nav_text and "<a " in nav_text)
            blob = nav_text
            for name in names:
                if name.endswith(".xhtml"):
                    blob += archive.read(name).decode("utf-8")
            if "FIXTURE NOT A CHAPTER" in html:
                check("EPUB fixture title", "FIXTURE NOT A CHAPTER" in blob)
                check("EPUB journal and cards", "journal-spread" in blob and "card-grid" in blob)
            check("EPUB has no private journal entry", not any("journal/private" in name for name in names))
            check("EPUB indexes", "index-alphabetical" in blob and 'id="index-revisit"' in blob)
            if (ROOT / "assets" / "parts" / "01-opener.svg").is_file():
                check("EPUB part opener", any("01-opener" in name for name in names))
    except (zipfile.BadZipFile, ET.ParseError, OSError) as exc:
        check("EPUB structure", False, str(exc))


def check_pdf(path: Path, check) -> None:
    data = path.read_bytes()
    check("PDF header", data.startswith(b"%PDF-"))
    text = pdf_text(data)
    pages = len(re.findall(r"/Type\s*/Page(?!s)", text))
    check("PDF has pages", pages >= 2, f"{pages} page(s)")
    boxes = [
        tuple(float(part) for part in match.groups())
        for match in re.finditer(r"/MediaBox\s*\[\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s*\]", text)
    ]
    if not boxes:
        check("PDF trim size", False, "MediaBox not found")
        return
    _x0, _y0, width, height = boxes[0]
    wide = abs(width - 504) <= 4
    high = abs(height - 720) <= 4
    check("PDF trim is 7 by 10 inches", wide and high, f"MediaBox {width:.1f} x {height:.1f} pt")


def pdf_text(data: bytes) -> str:
    import zlib

    parts = [data.decode("latin-1", errors="ignore")]
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.DOTALL):
        raw = match.group(1)
        for candidate in (raw, raw.strip(b"\r\n")):
            try:
                parts.append(zlib.decompress(candidate).decode("latin-1", errors="ignore"))
                break
            except zlib.error:
                continue
    return "\n".join(parts)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"FAIL  validation crashed: {exc}")
        raise SystemExit(1) from exc
