# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

out = Path(__file__).resolve().parent / "Resumen_contexto_proyecto_bayesiano.docx"

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

title = doc.add_heading("Proyecto de Estadística Bayesiana", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub = doc.add_paragraph("Universidad Externado de Colombia · Pregrado Ciencia de Datos · 4° semestre")
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph(
    "Documento de contexto: comprensión del proyecto, estado de entregas y propuesta de trabajo."
).alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph()

doc.add_heading("1. Confirmación de contexto", level=1)
doc.add_paragraph(
    "Se revisó el README del repositorio, la carpeta teorias/ (mapa del parcial 2, guía de interpretaciones, "
    "material de Gibbs, MH/HMC, regresión bayesiana, etc.), la base datos/base_hogar_modelo.csv y las entregas "
    "en entregas/ (segundaentrega_bayesiana.pdf, Avance 2 de diseño analítico y el cuaderno segundaentrega_bayes.ipynb). "
    "En el disco las rutas usan nombres datos/, teorias/ y entregas/ (equivalentes a 02_datos/, 01_teoria/ y 03_entregas/ del README)."
)

doc.add_heading("2. De qué trata el proyecto", level=1)
p = doc.add_paragraph()
p.add_run("Problema de negocio. ").bold = True
p.add_run(
    "Una comercializadora de artículos para el hogar debe decidir inventario y pedidos. "
    "El proyecto pasó del caso de un producto nuevo (primera entrega) al "
    "sector agregado de muebles y artículos para el hogar en Estados Unidos, "
    "como referencia de cuánto puede variar la demanda del conjunto antes de pronosticar un SKU concreto."
)

p = doc.add_paragraph()
p.add_run("Pregunta de investigación. ").bold = True
p.add_run(
    "¿De qué manera el crecimiento de otras categorías del comercio minorista, el ingreso disponible de los hogares "
    "y el nivel de inventarios explican el crecimiento mensual de las ventas de muebles y artículos para el hogar "
    "en EE. UU., y qué tanta incertidumbre queda bajo inferencia bayesiana con verosimilitud robusta a los datos extremos de 2020?"
)

p = doc.add_paragraph()
p.add_run("Datos. ").bold = True
p.add_run(
    "Series mensuales FRED (Census Bureau / BEA), marzo 1992 – julio 2026: 413 meses totales, "
    "389 de entrenamiento (hasta julio 2024) y 24 reservados para prueba (ago 2024 – jul 2026). "
    "Variable respuesta: crecimiento mensual y_t = 100·(log S_t − log S_{t−1}) en puntos de log-diferencia. "
    "Ocho covariables (crecimientos sectoriales, ingreso, razón inventarios/ventas rezagada, rezago de y)."
)

p = doc.add_paragraph()
p.add_run("Enfoque bayesiano (intuición). ").bold = True
p.add_run(
    "El parámetro no es un número fijo sino una distribución posterior ∝ verosimilitud × prior. "
    "Interesan intervalos creíbles, probabilidades posteriores P(β_j > 0 | datos) y la predictiva posterior "
    "(incertidumbre del parámetro más ruido del mes nuevo), no solo un pronóstico puntual para inventario."
)

doc.add_heading("3. Modelo acordado (segunda entrega)", level=1)
doc.add_paragraph(
    "Regresión lineal bayesiana con errores t de Student (posterior no conjugada → MCMC):"
)
doc.add_paragraph(
    "y_t = β_0 + Σ_{j=1}^8 β_j z_{jt} + ε_t,    ε_t ~ t_ν(0, σ_t)",
    style="List Bullet",
)
doc.add_paragraph(
    "σ_t = σ · λ_t · ψ^{I(t≥jul 2020)}, con λ_t = κ_m en mar–jun 2020 y λ_t = 1 en el resto.",
    style="List Bullet",
)
doc.add_paragraph(
    "16 parámetros: β_0, β_1…β_8, σ, ν, κ_1…κ_4, ψ. Variables z_{jt} estandarizadas con media y desviación "
    "de meses normales del entrenamiento (sin filtrar la muestra de prueba)."
)

doc.add_heading("4. Hallazgos del EDA que sostienen el modelo", level=1)
items = [
    "Cuatro meses COVID (mar–jun 2020) inflan dispersión (desv. std de y: 5.46 con COVID vs 1.84 sin ellos); no se eliminan (Lenza y Primiceri, 2022).",
    "Colas pesadas en meses normales (curtosis en exceso ≈ 6.2) → verosimilitud t, no Normal.",
    "Volatilidad mayor desde julio 2020 (desv. ~1.54 antes vs ~3.25 después) → factor ψ.",
    "Correlaciones moderadas con y sin COVID (p. ej. electrónica 0.48 sin COVID); VIF < 1.73 → se mantienen las 8 variables.",
    "Interpretación: asociaciones contemporáneas, no causalidad; alcance sector EE. UU., no empresa concreta.",
]
for it in items:
    doc.add_paragraph(it, style="List Bullet")

doc.add_heading("5. Priors (débilmente informativas)", level=1)
table = doc.add_table(rows=7, cols=3)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Parámetro"
hdr[1].text = "Prior"
hdr[2].text = "Idea"
rows = [
    ("β_0, β_j", "Normal(0, 1)", "Efectos en escala de y en meses normales; sin imponer signo."),
    ("σ", "Half-Normal(2)", "Escala positiva; cubre ~1.8 pp de desviación típica."),
    ("ν", "Gamma(2, tasa 0.1)", "Grados de libertad flexibles (colas pesadas a casi normal)."),
    ("κ_m", "log κ_m ~ Half-Normal(2)", "Amplifica error en cada mes COVID (κ ≥ 1)."),
    ("ψ", "log ψ ~ Normal(0, 1)", "Cambio de volatilidad desde jul 2020; centrado en ψ = 1."),
    ("Chequeos", "Predictiva a priori, sensibilidad en β, plausibilidad MV", "Ya implementados en el cuaderno de entrega 2."),
]
for i, row in enumerate(rows, start=1):
    table.rows[i].cells[0].text = row[0]
    table.rows[i].cells[1].text = row[1]
    table.rows[i].cells[2].text = row[2]

doc.add_heading("6. Estado de las entregas", level=1)
doc.add_paragraph("Segunda entrega (Estadística Bayesiana, PDF + notebook):", style="List Bullet")
done = [
    "Planteamiento, pregunta, justificación, objetivos.",
    "EDA completo (tablas, figuras, elección de t, correlaciones, VIF, ACF).",
    "Especificación del modelo y priors con gráficos y predictiva a priori.",
]
for d in done:
    doc.add_paragraph(d, style="List Bullet 2")

doc.add_paragraph("Pendiente explícito en el cuaderno (entrega final):", style="List Bullet")
pend = [
    "Metropolis–Hastings (4 cadenas), diagnósticos (R̂, ESS, trazas).",
    "Inferencia posterior e interpretación bayesiana de coeficientes.",
    "Validación en 24 meses de prueba (RMSE, MAE, CRPS, cobertura de intervalos).",
    "Predictiva posterior y rango de referencia para discusión de inventario.",
    "Apéndice matemático de la log-posterior.",
]
for p in pend:
    doc.add_paragraph(p, style="List Bullet 2")

doc.add_paragraph(
    "Avance 2 (Pensamiento Crítico II): diseño analítico, validez, criterios de éxito/parada, "
    "referencias (media histórica, persistencia, rango solo con historia desde jul 2020) y lectura "
    "anticipada de resultados (incluido el caso en que el valor central no mejora a la media histórica)."
)

doc.add_heading("7. Propuesta de trabajo inmediato", level=1)
doc.add_paragraph(
    "Continuar con el objetivo específico 4: implementar la log-posterior, Metropolis–Hastings con cuatro cadenas "
    "y diagnósticos MCMC antes de interpretar coeficientes; luego predictiva posterior, métricas en la prueba "
    "y redacción alineada con la guía del curso (IC creíbles, P(θ > c | y), predictiva vs parámetro)."
)

doc.add_paragraph()
foot = doc.add_paragraph(
    "Generado como apoyo al proyecto del curso. Revisar fechas y referencias en los PDFs oficiales antes de entregar."
)
foot.runs[0].italic = True
foot.runs[0].font.size = Pt(9)

doc.save(out)
print(out)
