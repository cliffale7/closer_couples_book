"""Print the template-route HTML with the book project's Chrome path."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import build_all  # noqa: E402

HERE = Path(__file__).resolve().parent.parent / "design" / "proofs"
build_all.print_pdf(HERE / "template-routes.html", HERE / "template-routes.pdf", timeout=180)
print("WROTE", HERE / "template-routes.pdf")
