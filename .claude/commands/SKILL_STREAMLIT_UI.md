# SKILL_STREAMLIT_UI.md — Streamlit UI Patterns & Rules

## UI Structure Order

- Every page must follow this top-to-bottom order, without exception:
  1. Page title and subtitle (`st.title`, `st.caption`).
  2. Sidebar with all filters.
  3. KPI metrics row (`st.metric` inside `st.columns`).
  4. Data table (`st.dataframe`).
  5. Charts (`st.plotly_chart`).
- Never place filters in the main canvas — filters belong exclusively in `st.sidebar`.
- Never place metrics below charts — metrics summarize the data; charts detail it.

## Sidebar Filter Patterns

- Open the sidebar block with `with st.sidebar:` and keep all filter widgets inside it.
- Display filters in this order: categorical → geographic → numeric → date → text search.
- Use `st.multiselect` for columns with 2–30 unique values.
- Use `st.selectbox` only for single-value selections when multiselect is not appropriate.
- Use `st.slider` with `(min_value, max_value)` for numeric ranges.
- Use `st.text_input` for free-text search (partial match, case-insensitive).
- Cascading filters (e.g., Region → Province): recompute the child option list based on
  the currently selected parent value before rendering the child widget.
- Always provide a "Select all" default: initialize multiselect with the full option list.
- Label every widget clearly — no cryptic labels, no column code names exposed to the user.
- Add `st.sidebar.markdown("---")` as a visual divider between filter groups.

## Data Loading and Caching Rules

- Decorate every data-loading function with `@st.cache_data`.
- Never call `pd.read_excel` or any I/O function inside `app.py` — delegate to `src/loader.py`.
- Pass the file path as a parameter to the cached function, not as a global.
- Do not cache filtered DataFrames — only cache the raw, cleaned source DataFrame.
- If the source file changes, instruct the user to use `st.cache_data.clear()` or restart.
- Never call `st.cache_data.clear()` automatically inside the app flow.

## Empty State Handling

- After every filter operation, check `if df_filtered.empty:` before rendering anything.
- When the filtered DataFrame is empty:
  - Show `st.info("No records match the current filters. Adjust the sidebar filters.")`.
  - Do not render metrics, tables, or charts.
  - Do not raise exceptions or show raw Python errors.
- When a specific chart's data subset is empty (e.g., a grouped aggregate):
  - Show `st.warning("Not enough data to display this chart.")` in place of the chart.
  - Continue rendering the rest of the page normally.

## Error Messaging Patterns

- Use `st.error("...")` for errors that block the app from functioning
  (e.g., file not found, missing required column).
- Use `st.warning("...")` for non-critical issues that degrade but don't stop the app
  (e.g., optional column missing, nulls in a chart field).
- Use `st.info("...")` for neutral informational states (e.g., empty filter result).
- Never display raw Python tracebacks to the user — catch exceptions and show `st.error`.
- Always include a human-readable action hint in error messages
  (e.g., "Check that the file exists at the configured path.").
- Log the full exception to `stderr` with `logging.exception(...)` before showing `st.error`.

## Performance Guardrails

- Never run heavy computations (groupby, sort, merge) inside widget callbacks or render loops.
- Compute derived DataFrames once per rerun, assign to a variable, and reuse that variable.
- Never call the same filter or aggregation function more than once per rerun.
- Limit `st.dataframe` display to a maximum of 500 rows by default; add a toggle to show all.
- For charts with more than 1,000 data points, aggregate before plotting — never plot raw rows.
- Avoid `st.experimental_rerun()` — redesign the flow so reruns happen naturally.

## Keeping UI Code Simple

- `app.py` must read like an outline: one function call per section, no inline logic.
- Every `st.*` call must display data that was computed in `src/` — never compute inline.
- Keep `app.py` under 100 lines total.
- Use `st.columns([ratio1, ratio2])` for side-by-side layout — never use HTML/CSS hacks.
- Use `st.expander` to hide secondary content (raw table, debug info) that is not critical.
- Do not use `st.markdown` with raw HTML unless absolutely necessary for formatting.
- Never use `st.write` for displaying DataFrames or figures — use `st.dataframe` and
  `st.plotly_chart` explicitly.
