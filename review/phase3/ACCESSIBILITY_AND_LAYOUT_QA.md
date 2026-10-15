# Accessibility and layout

15 October 2026. This is the rebuilt draft, 1,464 workbook pages.

## Automated

`python scripts/validate.py` passed.

- Workbook PDF MediaBox is 504 by 720 pt on the first page, and pypdfium2 reports 1,464 pages at 504 by 720 pt.
- EPUB mimetype is stored first. `nav.xhtml` has a table of contents. Package XML parses. Manifest files exist. 129 images in the XHTML, and none of those `img` tags lack `alt`. 129 SVG files are in the EPUB.
- DOCX opens, uses Georgia and Palatino Linotype, embeds media, and does not contain a private journal path.
- Companion PDF is 294 US Letter pages. Journal CSS sets handwriting rules at 0.36 in, above the 0.32 in minimum. The repeat pack PDF is 17 letter pages.
- Card PDF is 49 letter pages.
- `python scripts/raster_pages.py` rendered all 1,464 workbook pages at 144 dpi (1008 by 1440 px) and measured margin ink. Two pages were flagged: 6 and 724.

## Looked at

Opened workbook pages 1 (cover), 6 (contents), 30 (a chapter afterward), 724 (Our Story lines), and 1464 (image log). Text on those pages is inside the sheet. Page 6's flag is the dotted leader. Page 724's flag is the journal box rule. Neither cuts a word.

Opened art-review pages 1 and 12. The decision list and the motif grid are readable, and corrected drawings are marked as awaiting the owner.

## Not done

No screen reader was run. No keyboard test of the EPUB in a reading system. No physical ruler on a printed sheet. High-contrast labels were not measured with a contrast meter; the type is ink `#241F1C` on parchment `#F6F1E7` and ivory `#FBF8F2`.
