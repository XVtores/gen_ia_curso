"""Data loading and cleaning functions."""

import logging
from pathlib import Path

import pandas as pd
import streamlit as st

from src.utils import COLUMN_RENAME, REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load, rename, parse, and clean the company directory Excel file."""
    try:
        df = pd.read_excel(path, engine="openpyxl")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Excel file not found: {path}") from exc

    df = df.rename(columns=COLUMN_RENAME)

    if "INDUSTRIA" not in df.columns:
        if "CIIU_NIVEL_1" in df.columns:
            logger.warning(
                "Column 'INDUSTRIA' not found; falling back to 'CIIU NIVEL 1'."
            )
            df["INDUSTRIA"] = df["CIIU_NIVEL_1"]
        else:
            raise ValueError(
                "Required column missing: 'INDUSTRIA' and fallback "
                "'CIIU NIVEL 1' are both absent from the file."
            )

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Required column missing after rename: '{col}'")

    df["FECHA_CONSTITUCION"] = pd.to_datetime(
        df["FECHA_CONSTITUCION"], dayfirst=True, errors="coerce"
    )
    df["AÑO_CONSTITUCION"] = df["FECHA_CONSTITUCION"].dt.year.astype("Int64")

    df["BARRIO"] = df["BARRIO"].fillna("No informado")
    df["CAPITAL_SUSCRITO"] = (
        pd.to_numeric(df["CAPITAL_SUSCRITO"], errors="coerce").fillna(0.0)
    )

    return df
