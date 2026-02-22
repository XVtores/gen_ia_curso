"""Filter logic — pure functions that return filtered DataFrames."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class FilterParams:
    """All filter parameters passed from the sidebar."""

    situacion_legal: list[str]
    tipo: list[str]
    region: list[str]
    provincia: list[str]
    industria: list[str]
    capital_min: float
    capital_max: float
    año_min: int
    año_max: int
    presento_balance: str
    nombre_busqueda: str


def get_provincia_options(df: pd.DataFrame, regiones: list[str]) -> list[str]:
    """Return unique provinces for the selected regions (or all if none selected)."""
    if not regiones:
        return sorted(df["PROVINCIA"].dropna().unique().tolist())
    mask = df["REGION"].isin(regiones)
    return sorted(df.loc[mask, "PROVINCIA"].dropna().unique().tolist())


def apply_filters(df: pd.DataFrame, params: FilterParams) -> pd.DataFrame:
    """Apply all sidebar filters and return the filtered DataFrame."""
    mask = pd.Series(True, index=df.index)

    if params.situacion_legal:
        mask &= df["SITUACION_LEGAL"].isin(params.situacion_legal)

    if params.tipo:
        mask &= df["TIPO"].isin(params.tipo)

    if params.region:
        mask &= df["REGION"].isin(params.region)

    if params.provincia:
        mask &= df["PROVINCIA"].isin(params.provincia)

    if params.industria:
        mask &= df["INDUSTRIA"].isin(params.industria)

    mask &= df["CAPITAL_SUSCRITO"].between(params.capital_min, params.capital_max)

    year_valid = df["AÑO_CONSTITUCION"].notna()
    mask &= year_valid & df["AÑO_CONSTITUCION"].between(params.año_min, params.año_max)

    if params.presento_balance != "Todos":
        mask &= df["PRESENTO_BALANCE"] == params.presento_balance

    if params.nombre_busqueda.strip():
        term = params.nombre_busqueda.strip()
        mask &= df["NOMBRE"].str.contains(term, case=False, na=False)

    return df.loc[mask].copy()
