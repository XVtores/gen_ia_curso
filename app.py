"""Streamlit entry point — UI wiring only."""

import logging
import sys

import streamlit as st

from src.charts import (
    build_capital_histogram,
    build_industry_bar,
    build_legal_status_pie,
    build_province_bar,
    build_top_capital_bar,
    build_type_bar,
)
from src.filters import FilterParams, apply_filters, get_provincia_options
from src.loader import load_data
from src.metrics import compute_metrics
from src.utils import DATA_FILE, TABLE_COLUMNS, TABLE_LABELS

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

st.set_page_config(
    page_title="Directorio de Compañías — Ecuador",
    page_icon="🏢",
    layout="wide",
)

st.title("Directorio de Compañías — Ecuador")
st.caption("Exploración interactiva del registro de compañías constituidas en Ecuador.")

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
try:
    df_raw = load_data(DATA_FILE)
except Exception as exc:
    logging.exception("Error loading data")
    st.error(f"No se pudo cargar el archivo de datos: {exc}")
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Filtros")

    situacion_opts = sorted(df_raw["SITUACION_LEGAL"].dropna().unique().tolist())
    situacion = st.multiselect("Situación Legal", situacion_opts, default=situacion_opts)

    tipo_opts = sorted(df_raw["TIPO"].dropna().unique().tolist())
    tipo = st.multiselect("Tipo de Empresa", tipo_opts, default=tipo_opts)

    st.markdown("---")

    region_opts = sorted(df_raw["REGION"].dropna().unique().tolist())
    region = st.multiselect("Región", region_opts, default=region_opts)

    provincia_opts = get_provincia_options(df_raw, region)
    provincia = st.multiselect("Provincia", provincia_opts, default=provincia_opts)

    industria_opts = sorted(df_raw["INDUSTRIA"].dropna().unique().tolist())
    industria = st.multiselect("Industria", industria_opts, default=industria_opts)

    st.markdown("---")

    cap_min_raw = float(df_raw["CAPITAL_SUSCRITO"].min())
    cap_max_slider = float(df_raw["CAPITAL_SUSCRITO"].quantile(0.99))
    cap_max_actual = float(df_raw["CAPITAL_SUSCRITO"].max())

    capital_range = st.slider(
        "Capital Suscrito (USD)",
        min_value=cap_min_raw,
        max_value=cap_max_slider,
        value=(cap_min_raw, cap_max_slider),
        format="$%.0f",
    )
    capital_max_filter = (
        cap_max_actual if capital_range[1] >= cap_max_slider else capital_range[1]
    )

    año_min_raw = int(df_raw["AÑO_CONSTITUCION"].dropna().min())
    año_max_raw = int(df_raw["AÑO_CONSTITUCION"].dropna().max())
    año_range = st.slider(
        "Año de Constitución",
        min_value=año_min_raw,
        max_value=año_max_raw,
        value=(año_min_raw, año_max_raw),
    )

    st.markdown("---")

    balance_opts = ["Todos"] + sorted(
        df_raw["PRESENTO_BALANCE"].dropna().unique().tolist()
    )
    presento_balance = st.selectbox("Presentó Balance Inicial", balance_opts)

    nombre_busqueda = st.text_input("Buscar por Nombre", placeholder="Ej. PETROECUADOR")

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------
params = FilterParams(
    situacion_legal=situacion,
    tipo=tipo,
    region=region,
    provincia=provincia,
    industria=industria,
    capital_min=capital_range[0],
    capital_max=capital_max_filter,
    año_min=año_range[0],
    año_max=año_range[1],
    presento_balance=presento_balance,
    nombre_busqueda=nombre_busqueda,
)

df_filtered = apply_filters(df_raw, params)

# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------
if df_filtered.empty:
    st.info("No hay registros con los filtros actuales. Ajusta los filtros del panel lateral.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI metrics
# ---------------------------------------------------------------------------
metrics = compute_metrics(df_filtered, df_raw)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Empresas", metrics.total_empresas, delta=metrics.total_empresas - metrics.total_raw)
c2.metric("Capital Total", metrics.capital_total)
c3.metric("Capital Promedio", metrics.capital_promedio)
c4.metric("Provincias", metrics.provincias)

st.markdown("---")

# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------
show_all = st.checkbox("Mostrar todas las filas")
display_df = df_filtered[TABLE_COLUMNS].rename(columns=TABLE_LABELS)
row_limit = len(display_df) if show_all else min(500, len(display_df))
st.dataframe(display_df.head(row_limit), use_container_width=True)

csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Descargar CSV",
    data=csv,
    file_name="directorio_filtrado.csv",
    mime="text/csv",
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(build_industry_bar(df_filtered), use_container_width=True)
with col2:
    st.plotly_chart(build_province_bar(df_filtered), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(build_legal_status_pie(df_filtered), use_container_width=True)
with col4:
    st.plotly_chart(build_type_bar(df_filtered), use_container_width=True)

col5, col6 = st.columns(2)
with col5:
    if df_filtered["CAPITAL_SUSCRITO"].gt(0).any():
        st.plotly_chart(build_capital_histogram(df_filtered), use_container_width=True)
    else:
        st.warning("No hay datos de capital para mostrar el histograma.")
with col6:
    st.plotly_chart(build_top_capital_bar(df_filtered), use_container_width=True)
