"""Plotly figure builders — one function per chart."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_industry_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar: top 10 industries by number of companies."""
    counts = (
        df["INDUSTRIA"]
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={"count": "Empresas"})
        .sort_values("Empresas")
    )
    fig = px.bar(
        counts,
        x="Empresas",
        y="INDUSTRIA",
        orientation="h",
        title="Top 10 Industrias",
        labels={"INDUSTRIA": ""},
        color="Empresas",
        color_continuous_scale="Blues",
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return fig


def build_province_bar(df: pd.DataFrame) -> go.Figure:
    """Vertical bar: top 15 provinces by company count."""
    counts = (
        df["PROVINCIA"]
        .value_counts()
        .head(15)
        .reset_index()
        .rename(columns={"count": "Empresas"})
    )
    fig = px.bar(
        counts,
        x="PROVINCIA",
        y="Empresas",
        title="Empresas por Provincia (Top 15)",
        labels={"PROVINCIA": ""},
        color="Empresas",
        color_continuous_scale="Teal",
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35)
    return fig


def build_legal_status_pie(df: pd.DataFrame) -> go.Figure:
    """Donut chart: distribution by legal status."""
    counts = (
        df["SITUACION_LEGAL"]
        .value_counts()
        .reset_index()
        .rename(columns={"count": "Empresas"})
    )
    fig = px.pie(
        counts,
        names="SITUACION_LEGAL",
        values="Empresas",
        title="Distribución por Situación Legal",
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def build_type_bar(df: pd.DataFrame) -> go.Figure:
    """Vertical bar: distribution by company type."""
    counts = (
        df["TIPO"]
        .value_counts()
        .reset_index()
        .rename(columns={"count": "Empresas"})
    )
    fig = px.bar(
        counts,
        x="TIPO",
        y="Empresas",
        title="Distribución por Tipo de Empresa",
        labels={"TIPO": ""},
        color="Empresas",
        color_continuous_scale="Purp",
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


def build_capital_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram: capital suscrito distribution on a linear scale."""
    data = df.loc[df["CAPITAL_SUSCRITO"] > 0, "CAPITAL_SUSCRITO"]
    fig = px.histogram(
        data,
        x="CAPITAL_SUSCRITO",
        nbins=40,
        title="Distribución de Capital Suscrito",
        labels={"CAPITAL_SUSCRITO": "Capital Suscrito (USD)"},
        color_discrete_sequence=["#2196F3"],
    )
    return fig


def build_top_capital_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar: top 10 companies by subscribed capital."""
    top = (
        df[["NOMBRE", "CAPITAL_SUSCRITO"]]
        .nlargest(10, "CAPITAL_SUSCRITO")
        .sort_values("CAPITAL_SUSCRITO")
    )
    fig = px.bar(
        top,
        x="CAPITAL_SUSCRITO",
        y="NOMBRE",
        orientation="h",
        title="Top 10 Empresas por Capital Suscrito",
        labels={"CAPITAL_SUSCRITO": "Capital (USD)", "NOMBRE": ""},
        color="CAPITAL_SUSCRITO",
        color_continuous_scale="Oranges",
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig
