"""Constants, column rename map, and shared formatters."""

from pathlib import Path

# ---------------------------------------------------------------------------
# File location
# ---------------------------------------------------------------------------
DATA_FILE: Path = Path(__file__).parent.parent / "filtrado_directorio_companias.xlsx"

# ---------------------------------------------------------------------------
# Column rename map: Excel header → clean Python identifier
# ---------------------------------------------------------------------------
COLUMN_RENAME: dict[str, str] = {
    "No. FILA": "NO_FILA",
    "EXPEDIENTE": "EXPEDIENTE",
    "RUC": "RUC",
    "NOMBRE": "NOMBRE",
    "SITUACIÓN LEGAL": "SITUACION_LEGAL",
    "FECHA_CONSTITUCION": "FECHA_CONSTITUCION",
    "TIPO": "TIPO",
    "PAÍS": "PAIS",
    "REGIÓN": "REGION",
    "PROVINCIA": "PROVINCIA",
    "CANTÓN": "CANTON",
    "CIUDAD": "CIUDAD",
    "CALLE": "CALLE",
    "NÚMERO": "NUMERO",
    "INTERSECCIÓN": "INTERSECCION",
    "BARRIO": "BARRIO",
    "TELÉFONO": "TELEFONO",
    "REPRESENTANTE": "REPRESENTANTE",
    "CARGO": "CARGO",
    "CAPITAL SUSCRITO": "CAPITAL_SUSCRITO",
    "CIIU NIVEL 1": "CIIU_NIVEL_1",
    "INDUSTRIA": "INDUSTRIA",
    "CIIU NIVEL 6": "CIIU_NIVEL_6",
    "ÚLTIMO BALANCE": "ULTIMO_BALANCE",
    "PRESENTÓ BALANCE INICIAL": "PRESENTO_BALANCE",
    "FECHA PRESENTACIÓN BALANCE INICIAL": "FECHA_PRESENTACION_BALANCE",
}

# Columns required in the cleaned DataFrame
REQUIRED_COLUMNS: list[str] = [
    "NOMBRE",
    "SITUACION_LEGAL",
    "TIPO",
    "REGION",
    "PROVINCIA",
    "INDUSTRIA",
    "CAPITAL_SUSCRITO",
    "FECHA_CONSTITUCION",
    "REPRESENTANTE",
    "PRESENTO_BALANCE",
]

# Columns shown in the data table
TABLE_COLUMNS: list[str] = [
    "NOMBRE",
    "SITUACION_LEGAL",
    "TIPO",
    "PROVINCIA",
    "INDUSTRIA",
    "CAPITAL_SUSCRITO",
    "REPRESENTANTE",
]

# Human-readable labels for the table
TABLE_LABELS: dict[str, str] = {
    "NOMBRE": "Nombre",
    "SITUACION_LEGAL": "Situación Legal",
    "TIPO": "Tipo",
    "PROVINCIA": "Provincia",
    "INDUSTRIA": "Industria",
    "CAPITAL_SUSCRITO": "Capital Suscrito (USD)",
    "REPRESENTANTE": "Representante",
}


def format_currency(value: float) -> str:
    """Format a float as a compact USD currency string."""
    if value >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:,.1f}K"
    return f"${value:,.0f}"
