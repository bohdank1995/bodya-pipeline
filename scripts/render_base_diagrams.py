#!/usr/bin/env python3
"""Re-render the three base diagrams (combined pipeline, idea validation, solution validation)
from their candidate.json files, then keep the line breaks in the descriptions.

Run after editing any of those candidate.json files:
    python3 scripts/render_base_diagrams.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_project_diagram import finalize  # noqa: E402

DIAGRAMS = [
    ("pipeline", "validation-to-solution"),
    ("idea-validation", "idea-validation"),
    ("solution-validation", "solution-validation"),
]

failed = False
for folder, name in DIAGRAMS:
    base = os.path.join("diagrams", folder)
    result = finalize(os.path.join(base, "candidate.json"), os.path.join(base, name + ".html"),
                      os.path.join(base, "review-latest"))
    print(folder, result.get("status"))
    if result.get("status") != "pass":
        failed = True
        print(result.get("diagnostics", [])[:3])
sys.exit(1 if failed else 0)
