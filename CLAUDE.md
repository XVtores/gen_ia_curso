# CLAUDE.md — Project Rules for Claude Code

## 1. Project Goal
Build a Streamlit web application that loads an Excel file
(`filtrado_directorio_companias.xlsx`), applies interactive sidebar filters,
displays KPI metrics, and renders Plotly charts. Target users are business
analysts who need fast, no-code exploration of a company directory dataset.

## 2. Non-Negotiables
- Work **incrementally**: one file or one feature at a time.
- Never generate multiple files in a single response unless explicitly requested.
- Never invent files, modules, or utilities that were not requested.
- Never rewrite working code unless a bug is confirmed or a change is explicitly asked.
- Always confirm the task scope before generating code.

## 3. Default Project Structure
```
CODE/
├── app.py                  # Streamlit entry point — UI wiring only
├── CLAUDE.md               # This file
├── requirements.txt        # Pinned dependencies
├── filtrado_directorio_companias.xlsx
└── src/
    ├── __init__.py
    ├── loader.py           # Data loading and cleaning
    ├── filters.py          # Filter logic (pure functions)
    ├── metrics.py          # KPI calculations (pure functions)
    ├── charts.py           # Plotly figure builders (pure functions)
    └── utils.py            # Formatters, constants, helpers
```

## 4. Code Quality Rules
- Maximum **300 lines per file**. Split if exceeded.
- Maximum **50 lines per function**. Extract helpers if exceeded.
- Each function/module has **one responsibility only**.
- No dead code, no commented-out blocks left in final output.
- No duplicate logic — reuse existing functions before writing new ones.

## 5. Style Rules
- Python **3.10+** syntax (use `match`, union types `X | Y`, etc. where appropriate).
- **Type hints required** for all public functions.
- **Short docstrings** (one line) for all public functions.
- No global mutable state. Pass data explicitly as function arguments.
- Use `pathlib.Path` for all file paths — never raw strings.
- Constants go in `src/utils.py`, not scattered in modules.

## 6. Streamlit Rules
- `app.py` contains **only UI wiring**: calls to `src/` functions + Streamlit layout.
- All business logic lives in `src/`. Never put `pd.read_excel`, calculations, or
  chart-building directly in `app.py`.
- Sidebar hosts all filters — never inline filters in the main canvas.
- Use `@st.cache_data` on every data-loading function.
- Use `st.session_state` only when strictly necessary (multi-step interactions).
- Graceful empty states: if filtered DataFrame is empty, show
  `st.info("No records match the current filters.")` — never let charts crash.

## 7. Dependencies Rules
- Keep dependencies **minimal**.
- Excel reading: `openpyxl` (via `pandas`).
- Charts: `plotly` only — no matplotlib, no altair, no bokeh.
- No heavy ML/stats libraries unless explicitly requested.
- `requirements.txt` must pin major versions (e.g., `streamlit>=1.32,<2`).

## 8. Linting / Formatting Assumptions
- Formatter: **black** with `--line-length 88`.
- Linter: **flake8** with `max-line-length = 88`.
- No unused imports (`F401` is an error).
- No bare `except:` clauses (`E722` is an error).
- All generated code must pass `black --check` and `flake8` with zero errors.

## 9. Error Handling Rules
- **Never crash the Streamlit UI.** All I/O and computation must be wrapped in
  `try/except`.
- Use `st.error("...")` for unrecoverable errors (e.g., file not found).
- Use `st.warning("...")` for recoverable issues (e.g., missing optional columns).
- Log errors to `stderr` with Python's `logging` module — never use `print()`.
- Validate DataFrame columns on load; raise a clear `ValueError` with column name
  if an expected column is missing.

## 10. Response Protocol
When writing code, Claude must:
1. **State the file(s)** being created or modified (path + reason).
2. **Provide the complete file content** inside a fenced code block.
3. **Give the exact run command** (e.g., `streamlit run app.py`).
4. Nothing else — no lengthy explanations, no alternatives, no commentary.
