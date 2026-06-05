"""Prove-it tests for Module 03 — BI notes structure."""

from __future__ import annotations

from pathlib import Path

NOTES_DIR = Path(__file__).resolve().parents[1] / "notes"

REQUIRED_FILES: dict[str, list[str]] = {
    "grain_checklist.md": ["## Grain definition", "## Common mis-aggregation traps"],
    "lineage_example.md": ["## Report field", "## Warehouse source", "## Lineage diagram"],
    "tool_comparison.md": [
        "## Connectivity",
        "### Power BI",
        "### Tableau",
        "## Row-level security",
    ],
    "stakeholder_engagement.md": [
        "## Requirements gathering",
        "## Translating between worlds",
        "## Analytical skills that build trust",
    ],
    "power_bi_dax.md": [
        "## Storage mode: Import vs DirectQuery vs Composite",
        "## Measure vs calculated column (why the difference matters for performance)",
        "## Row-level security (RLS) in Power BI",
    ],
}


def test_notes_files_exist_with_headings() -> None:
    for filename, headings in REQUIRED_FILES.items():
        path = NOTES_DIR / filename
        assert path.exists(), f"Missing {path}"
        text = path.read_text(encoding="utf-8")
        assert len(text.strip()) > 100, f"{filename} should contain substantive starter content"
        for heading in headings:
            assert heading in text, f"{filename} missing heading: {heading}"
