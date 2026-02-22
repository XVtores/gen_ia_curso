"""KPI calculations — pure functions."""

from dataclasses import dataclass

import pandas as pd

from src.utils import format_currency


@dataclass
class Metrics:
    """Computed KPI values for the dashboard header."""

    total_empresas: int
    total_raw: int
    capital_total: str
    capital_promedio: str
    provincias: int


def compute_metrics(df_filtered: pd.DataFrame, df_raw: pd.DataFrame) -> Metrics:
    """Compute KPI metrics from the filtered and raw DataFrames."""
    total = len(df_filtered)
    total_raw = len(df_raw)
    capital_total = float(df_filtered["CAPITAL_SUSCRITO"].sum())
    capital_promedio = (
        float(df_filtered["CAPITAL_SUSCRITO"].mean()) if total > 0 else 0.0
    )
    provincias = int(df_filtered["PROVINCIA"].nunique())

    return Metrics(
        total_empresas=total,
        total_raw=total_raw,
        capital_total=format_currency(capital_total),
        capital_promedio=format_currency(capital_promedio),
        provincias=provincias,
    )
