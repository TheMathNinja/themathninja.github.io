# Analytics Fantasy Labs Directory

Published at https://themathninja.github.io/. Static directory for the three dashboards and the ten analyticsFF Linktree resources. Edit index.html to update the page; links.json records the imported Linktree destinations.

## True Position Cheatsheet

`true-position/` contains all 471 historical player rows and original notes from the 2021–2025 Google Sheets tabs, plus a dated 2026 snapshot of applied ADL and FAFL position overrides from public MFL player exports. Sources are recorded on the page and in the JSON files. The 2026 data is a snapshot, not an automatic refresh. It reflects overrides against current MFL defaults, not every change event earlier in the year.

Rebuild the page and CSV downloads after editing the template or source snapshots with `python true-position/build.py`. The historical rows are preserved verbatim. Shared 2026 changes are merged by MFL ID, custom position, and default position; league-specific differences retain separate rows.
