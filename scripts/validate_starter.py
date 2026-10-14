from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'source/experience_catalog.json'
assert CATALOG.is_file(), f'Missing {CATALOG}'
data = json.loads(CATALOG.read_text(encoding='utf-8'))
items = data['experiences']
parts = data['parts']
assert len(items) == 108, f'Expected 108 experiences, got {len(items)}'
assert [c['id'] for c in items] == list(range(1,109)), 'Missing, duplicated or out-of-order IDs'
assert len(parts) == 13, f'Expected 13 parts, got {len(parts)}'
for part in parts:
    assert all(items[n-1]['part_number'] == part['part_number'] for n in part['ids'])
assert len(list((ROOT / '.cursor/agents').glob('*.md'))) >= 12
for name in ('The_Closer_Project_Working_Manuscript_v0.1.docx','The_Closer_Project_Concept_and_Feedback_Invitation.docx'):
    assert (ROOT/'source'/name).is_file(), f'Missing {name}'
assert (ROOT/'planning/ORIGINAL_IDEAS_EXPANDED.md').is_file()
print(f'PASS: {len(items)} experiences in {len(parts)} parts; project subagents, original docs, and expanded ideas are present.')
