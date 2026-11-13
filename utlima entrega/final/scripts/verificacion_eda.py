"""Verifica carga de datos y estadísticos clave del EDA (sin MCMC)."""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
Y = "crec_muebles_hogar"


def main() -> None:
    df = pd.read_csv(DATA / "base_hogar_modelo.csv", parse_dates=["fecha"])
    entren = df[df["conjunto"] == "entrenamiento"].copy()
    prueba = df[df["conjunto"] == "prueba"]
    assert len(entren) == 389, len(entren)
    assert len(prueba) == 24, len(prueba)

    entren["es_covid"] = entren["covid_2020"] == 1
    entren["excluir"] = entren["es_covid"] | entren["es_covid"].shift(1, fill_value=False)
    normales = entren.loc[~entren["excluir"]]

    sd_y = normales[Y].std()
    print(f"SD Y meses normales: {sd_y:.3f} (esperado ~1.84)")
    assert 1.7 < sd_y < 2.0

    pearson = normales[[Y, "crec_electro"]].corr(method="pearson").iloc[0, 1]
    print(f"Pearson Y-electro: {pearson:.3f} (esperado ~0.48)")
    assert 0.4 < pearson < 0.55

    print("OK: datos y EDA básico consistentes con el informe.")


if __name__ == "__main__":
    main()
