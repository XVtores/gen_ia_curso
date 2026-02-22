# SKILL_ARCHITECTURE.md — Module & Code Structure Rules

## Module Boundaries

- `app.py` is the **only** file that imports Streamlit and renders UI elements.
- `src/` contains **pure Python only** — no Streamlit imports allowed inside `src/`.
- Every `src/` module has exactly one responsibility:
  - `loader.py` → reads and cleans the Excel file.
  - `filters.py` → applies filter logic to a DataFrame.
  - `metrics.py` → computes KPI values from a DataFrame.
  - `charts.py` → builds and returns Plotly figures.
  - `utils.py` → holds constants, formatters, and shared helpers.
- `app.py` calls functions from `src/`; it never contains business logic itself.
- Never import from `app.py` into any `src/` module — that direction is forbidden.

## File and Function Size Limits

- Hard limit: **300 lines per file**. If a file exceeds this, split it.
- Hard limit: **50 lines per function**. If a function exceeds this, extract helpers.
- If a function needs more than 3 levels of indentation, refactor it.
- One function = one action. If you use "and" to describe what a function does, split it.

## Naming Conventions

- Files: `snake_case.py` — all lowercase, underscores only.
- Functions: `snake_case` verbs — e.g., `load_data`, `apply_filters`, `build_bar_chart`.
- Variables: `snake_case` nouns — e.g., `df_filtered`, `capital_min`, `province_list`.
- Constants: `UPPER_SNAKE_CASE` — defined only in `src/utils.py`.
- Do not use abbreviations unless they are universally understood (e.g., `df` for DataFrame).
- Boolean variables and function names must start with `is_`, `has_`, or `should_`.

## No Duplication — Extract Helpers

- Before writing a new function, search existing `src/` files for equivalent logic.
- If the same data transformation appears in two places, move it to `src/utils.py`.
- If a chart pattern repeats across figures, extract a shared builder function in `charts.py`.
- If a filter pattern repeats, extract it into a helper in `filters.py`.
- Never copy-paste code blocks between modules — always reference a shared function.

## How to Add a New File

- Only create a new file when:
  - An existing file would exceed 300 lines after the addition.
  - A clearly distinct new responsibility emerges that does not fit any existing module.
- Justify the new file explicitly before creating it (one sentence is enough).
- New files must follow the same structure rules: `src/` for logic, naming conventions, size limits.
- Never create a file "just in case" or speculatively — only when concretely needed.
- Add the new file to the project structure tree in `CLAUDE.md` after creation.

## Expected Folder Structure

```
CODE/
├── app.py                  # UI wiring only — Streamlit calls live here
├── CLAUDE.md               # Project rules
├── requirements.txt        # Pinned dependencies
├── filtrado_directorio_companias.xlsx
└── src/
    ├── __init__.py         # Empty — marks src as a package
    ├── loader.py           # load_data() — reads, cleans, caches Excel
    ├── filters.py          # apply_filters() — pure filter logic
    ├── metrics.py          # compute_metrics() — KPI calculations
    ├── charts.py           # build_*_chart() — Plotly figure builders
    └── utils.py            # Constants, formatters, shared helpers
```

- Do not place files at the project root unless they are entry points or config files.
- Do not nest `src/` further (no sub-packages) unless a file exceeds 300 lines.
- The `.claude/` folder is reserved for Claude Code skills and must not contain source code.
