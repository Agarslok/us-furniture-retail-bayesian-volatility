"""Patch codigo_final_v1.ipynb -> entrega final (paths, feedback EDA, export LaTeX)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "codigo" / "codigo_final_vf.ipynb"
OUT_CODIGO = ROOT / "codigo" / "codigo_final_vf.ipynb"
OUT_FINAL = ROOT / "final" / "codigo_final_vf.ipynb"

CONFIG_CELL = r'''from pathlib import Path
import os
import shutil
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import optimize, stats
from scipy.special import gammaln

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 100

# --- Rutas del proyecto (local o Colab) ---
RUTA_DRIVE = os.environ.get("RUTA_DRIVE", "").strip()
# True: menos iteraciones MCMC (solo verificación local). En Colab usar False.
MODO_RAPIDO = os.environ.get("MODO_RAPIDO", "0") == "1"

SEMILLA = 2026
N_SIM = 4000
ARCHIVOS = ["base_hogar_modelo.csv", "diccionario_variables.csv"]

Y = "crec_muebles_hogar"
X = [
    "crec_electro",
    "crec_sin_tienda",
    "crec_construccion",
    "crec_tiendas_generales",
    "crec_gasolineras",
    "crec_ingreso_disponible",
    "razon_inv_ventas_rezago1",
    "crec_muebles_hogar_rezago1",
]
CUANTI = [Y] + X
rng = np.random.default_rng(SEMILLA)


def _resolver_proyecto() -> Path:
    candidatos = []
    if RUTA_DRIVE:
        candidatos.append(Path(RUTA_DRIVE))
    cwd = Path.cwd()
    candidatos.extend([cwd, cwd.parent, cwd.parent.parent])
    for base in candidatos:
        if (base / "data" / ARCHIVOS[0]).exists():
            return base
    return cwd


PROYECTO = _resolver_proyecto()
CARPETA_DATOS = PROYECTO / "data"

if RUTA_DRIVE:
    try:
        from google.colab import drive
        drive.mount("/content/drive", force_remount=False)
    except ImportError:
        pass

if not (CARPETA_DATOS / ARCHIVOS[0]).exists():
    try:
        from google.colab import files
        print("Sube los archivos de data/ a Colab si faltan:", ARCHIVOS)
        files.upload()
        CARPETA_DATOS = Path.cwd() / "data"
        CARPETA_DATOS.mkdir(exist_ok=True)
    except ImportError:
        pass

faltan = [a for a in ARCHIVOS if not (CARPETA_DATOS / a).exists()]
if faltan:
    raise FileNotFoundError(f"No se encontraron {faltan} en {CARPETA_DATOS}")

INFORME = PROYECTO / "final" / "informe_final"
CARPETA_SALIDAS = INFORME / "figuras"
CARPETA_TABLAS = INFORME / "tablas"
for p in (CARPETA_SALIDAS, CARPETA_TABLAS):
    p.mkdir(parents=True, exist_ok=True)

CARPETA = CARPETA_DATOS.parent  # compatibilidad con celdas que usan CARPETA / archivo en data
print("Proyecto:", PROYECTO)
print("Datos:", CARPETA_DATOS)
print("Figuras:", CARPETA_SALIDAS)
print("Tablas:", CARPETA_TABLAS)
print("MODO_RAPIDO:", MODO_RAPIDO)


def titulo(texto):
    print("\n" + "=" * 78)
    print(texto)
    print("=" * 78)


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(CARPETA_SALIDAS / nombre, dpi=160, bbox_inches="tight")
    plt.show()
    print(f"   [figura guardada] {nombre}")


def guardar_tabla(tabla, nombre, indice=True):
    dest = CARPETA_TABLAS / nombre
    tabla.to_csv(dest, index=indice, encoding="utf-8-sig")
    print(f"   [tabla guardada] {nombre}")
'''

COLAB_CELL = r'''# Opcional: montar Google Drive (solo Colab)
try:
    from google.colab import drive
    drive.mount("/content/drive", force_remount=False)
except ImportError:
    print("Entorno local: no se monta Drive.")
'''

TITLE_MD = """# Entrega final: Pensamiento Crítico II y Estadística Bayesiana

**Universidad Externado de Colombia · Facultad de Matemáticas · Pregrado en Ciencia de Datos**

**Proyecto:** Variación mensual de las ventas de muebles y artículos del hogar: una referencia para el inventario

**Integrantes:** Juan Esteban Jiménez Aristizábal, David Quijano, Juan Esteban Zambrano, Juan Angel Triana Olarte

**Datos:** FRED — Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org), series del U.S. Census Bureau y del Bureau of Economic Analysis.

**Salidas:** `final/informe_final/figuras` y `final/informe_final/tablas` (para Overleaf)."""

SEC0_MD = """## Sección 0. Configuración

Carga librerías y rutas. En **Colab**, define la variable de entorno `RUTA_DRIVE` con la carpeta del proyecto (que contenga `data/`). En **local**, se detecta automáticamente desde el directorio de trabajo.

Para una corrida corta de verificación: `MODO_RAPIDO=1`. Para la entrega: `MODO_RAPIDO=0` (30 000 quemado + 40 000 iteraciones por cadena)."""


def set_source(cell, text: str) -> None:
    cell["source"] = [line + "\n" for line in text.split("\n")]
    if cell["source"]:
        cell["source"][-1] = cell["source"][-1].rstrip("\n")


def patch(nb: dict) -> None:
    set_source(nb["cells"][0], TITLE_MD)
    set_source(nb["cells"][1], SEC0_MD)
    set_source(nb["cells"][2], COLAB_CELL)
    set_source(nb["cells"][3], CONFIG_CELL)

    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        src = src.replace('CARPETA / "base_hogar_modelo.csv"', 'CARPETA_DATOS / "base_hogar_modelo.csv"')
        src = src.replace('CARPETA / "diccionario_variables.csv"', 'CARPETA_DATOS / "diccionario_variables.csv"')
        if "guardar_tabla(sd_dec.round(3).to_frame" in src and "coef_var" not in src:
            extra = '''
cv_dec = (sd_dec / normales[Y].groupby(normales["anio"] // 10 * 10)[Y].mean().reindex(sd_dec.index)) * 100
cv_tab = pd.DataFrame({
    "desv_std_meses_normales": sd_dec.round(3),
    "coef_variacion_%": cv_dec.round(2),
})
print("\\nCoeficiente de variación de Y por década (meses normales, %):")
print(cv_tab.to_string())
guardar_tabla(cv_tab, "tabla_cv_por_decada.csv")
'''
            src = src.replace(
                'guardar_tabla(sd_dec.round(3).to_frame("desv_std_meses_normales"), "tabla_desv_por_decada.csv")',
                extra
                + '\nguardar_tabla(sd_dec.round(3).to_frame("desv_std_meses_normales"), "tabla_desv_por_decada.csv")',
            )
        if 'titulo("5.11 Matriz de correlaciones")' in src and "Pearson" not in src:
            src = src.replace(
                "titulo(\"5.11 Matriz de correlaciones\")",
                "titulo(\"5.11 Matriz de correlaciones (Pearson)\")",
            )
        if "N_BURN = 30000" in src:
            src = src.replace(
                "N_BURN = 30000      # iteraciones de calentamiento (se descartan; aquí se adapta la propuesta)\n"
                "N_ITER = 40000      # iteraciones que se conservan por cadena",
                "if MODO_RAPIDO:\n"
                "    N_BURN = 3000\n"
                "    N_ITER = 4000\n"
                "    print(\"ADVERTENCIA: MODO_RAPIDO activo (resultados distintos a la entrega).\")\n"
                "else:\n"
                "    N_BURN = 30000      # iteraciones de calentamiento\n"
                "    N_ITER = 40000      # iteraciones conservadas por cadena",
            )
        if "ruta_zip = shutil.make_archive(str(CARPETA /" in src:
            src = src.replace(
                'shutil.make_archive(str(CARPETA / "salidas_entrega_final"), "zip", CARPETA_SALIDAS)',
                'shutil.make_archive(str(INFORME / "salidas_entrega_final"), "zip", INFORME)',
            )
            src = src.replace(
                "(CARPETA_SALIDAS / \"resumen_final.txt\")",
                "(CARPETA_TABLAS / \"resumen_final.txt\")",
            )
            export = '''
# Exportar fragmentos LaTeX para el informe Overleaf
try:
    coef = res_post.loc[X].round(3) if "res_post" in dir() else None
except Exception:
    coef = None
lines_tex = ["% Generado automáticamente — no editar a mano"]
lines_tex.append(f"% R-hat max {tabla_conv['R_hat'].max():.4f}, ESS min {tabla_conv['ESS'].min():.0f}")
lines_tex.append(f"% RMSE prueba {metricas.iloc[0]['RMSE']:.3f}, cobertura 90% {tabla_t['dentro_90'].mean():.2f}")
(CARPETA_TABLAS / "metricas_informe.tex").write_text("\\n".join(lines_tex), encoding="utf-8")
print("   [latex] metricas_informe.tex")
'''
            if "metricas_informe.tex" not in src:
                src = src.replace(
                    'np.save(CARPETA_SALIDAS / "posterior_muestras.npy"',
                    export + '\nnp.save(CARPETA_TABLAS / "posterior_muestras.npy"',
                )
        src = src.replace('(CARPETA_SALIDAS / "resumen_eda.txt")', '(CARPETA_TABLAS / "resumen_eda.txt")')
        if src != "".join(cell.get("source", [])):
            set_source(cell, src.rstrip("\n"))

    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", []))
        if "### 5.13 Multicolinealidad (VIF)" in src and "regresión múltiple" not in src:
            src = src.replace(
                "Si hay colinealidad fuerte, la posterior de los coeficientes queda muy dispersa y correlacionada.",
                "Lo calculamos porque, en un modelo de regresión múltiple bayesiano, la colinealidad infla la varianza posterior de los coeficientes y puede hacerlos inestables aunque el ajuste parezca bueno. Si hay colinealidad fuerte, la posterior de los coeficientes queda muy dispersa y correlacionada.",
            )
            set_source(cell, src.rstrip("\n"))
        if "### 5.11 Matriz de correlaciones" in src and "Pearson" not in src:
            src = src.replace(
                "Se grafican las correlaciones de Pearson",
                "Se grafican las correlaciones lineales de Pearson",
            ) if "Se grafican las correlaciones de Pearson" in src else src.replace(
                "Matriz de correlaciones\n",
                "Matriz de correlaciones\n\nSe usan correlaciones de Pearson entre las variables en crecimiento mensual.\n",
            )
            set_source(cell, src.rstrip("\n"))

    # limpiar outputs para entrega limpia
    for cell in nb["cells"]:
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None


def main() -> None:
    with SRC.open(encoding="utf-8") as f:
        nb = json.load(f)
    patch(nb)
    for path in (OUT_CODIGO, OUT_FINAL):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print("Escrito:", path)


if __name__ == "__main__":
    main()
