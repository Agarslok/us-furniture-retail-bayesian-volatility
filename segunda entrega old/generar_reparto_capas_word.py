# -*- coding: utf-8 -*-
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

out = Path(__file__).resolve().parent / "Reparto_equipo_y_metricas_por_capas.docx"
alt = Path(__file__).resolve().parent / "Reparto_capas_dos_equipos.docx"

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

title = doc.add_heading("Reparto por equipos de capa (no por microtareas)", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph(
    "Quedan dos equipos con dominios completos. Cada equipo reparte el trabajo por dentro como quiera; "
    "aquí solo se define qué capa es, para qué sirve, cómo se sabe que quedó bien y qué bloques de trabajo incluye."
)

doc.add_heading("Equipos", level=1)
tab = doc.add_table(rows=3, cols=3)
tab.style = "Table Grid"
headers = ["Equipo", "Integrantes", "Dominio"]
for j, h in enumerate(headers):
    tab.rows[0].cells[j].text = h
tab.rows[1].cells[0].text = "Equipo Capa A"
tab.rows[1].cells[1].text = "Juan Triana + Juan Jiménez"
tab.rows[1].cells[2].text = (
    "Diseño, narrativa, validez, puente al negocio y al informe"
)
tab.rows[2].cells[0].text = "Equipo Capa B"
tab.rows[2].cells[1].text = "David Quijano (+ el cuarto integrante del grupo, si aplica, dentro del mismo equipo B)"
tab.rows[2].cells[2].text = (
    "Modelamiento bayesiano, cómputo, figuras/tablas numéricas y redacción de resultados"
)

doc.add_paragraph(
    "Si el cuarto compañero no es Quijano, trátalo como miembro del Equipo B bajo la misma capa; "
    "Triana y Jiménez no microgestionan esa parte."
)

# --- CAPA A ---
doc.add_heading("Capa A — Diseño, análisis y validez (Notion §3.1–3.8)", level=1)

p = doc.add_paragraph()
p.add_run("Descripción. ").bold = True
p.add_run(
    "Es el informe de diseño: por qué el proyecto importa, cómo se mide el fenómeno, qué datos hay, "
    "qué riesgos y amenazas tiene el análisis, qué estrategia es coherente con la pregunta y qué se esperaba "
    "ver antes de correr el modelo. Debe leerse como un solo argumento en prosa, no como plantilla por casillas "
    "ni como apéndice de estadística."
)

p = doc.add_paragraph()
p.add_run("Objetivo. ").bold = True
p.add_run(
    "Que una persona externa entienda el proyecto sin abrir el notebook y pueda decir si el diseño es defendible "
    "y alineado con la pregunta (asociación sectorial + incertidumbre para inventario, sin causalidad ni pronóstico "
    "adelantado mal planteado)."
)

doc.add_paragraph("Cómo se mide que se logró (criterios de “capa lista”)", style="List Bullet")
criterios_a = [
    "Cadena cerrada en prosa: problema → pregunta → medición → datos → estrategia → validación planificada → límites (rúbrica Notion).",
    "§3.6 solo expectativas (resultados esperados / escenarios esperado–contrario–nulo), sin pegar RMSE, posteriores ni rango MUSD de la corrida.",
    "§3.7 con pocas amenazas bien argumentadas (no checklist de clase), cada una con control previsto.",
    "Puente explícito hacia Capa B: una sección corta del tipo “Lo que el modelo debe entregar al informe es…” (posterior, prueba 24 meses, rango en dólares, contraste con Paso 9).",
    "Coherencia con lo ya escrito en Avance 2 (medición, holdout, referencias), pero reescrito narrativamente.",
    "Revisión cruzada interna A: un integrante escribe, el otro solo revisa cadena lógica y tono (no números del MH).",
]
for c in criterios_a:
    doc.add_paragraph(c, style="List Bullet 2")

doc.add_paragraph(
    "Bloques de trabajo del Equipo A (ustedes se reparten)", style="List Bullet"
)
tab_a = doc.add_table(rows=7, cols=2)
tab_a.style = "Table Grid"
tab_a.rows[0].cells[0].text = "Bloque"
tab_a.rows[0].cells[1].text = "Qué incluye (conjunto, no tareas sueltas)"
bloques_a = [
    (
        "Problema y puente",
        "Contexto inventario, pregunta, objetivos, alcance, UK vs US, mismo mes ≠ causalidad, producto final = rango sectorial",
    ),
    (
        "Medición y datos",
        "Conceptos → variables → FRED → 389/24 → proxies y brechas (prosa + tabla reducida)",
    ),
    (
        "Antecedentes",
        "Síntesis que obliga Bayes + t + incertidumbre (Lenza, demanda, Gelman, etc.)",
    ),
    (
        "Estrategia y expectativas",
        "Qué análisis se hará, qué se interpretará, qué contaría como éxito/límite antes de ver resultados",
    ),
    (
        "Validez y responsabilidad",
        "Amenazas plausibles + ética concreta del uso del rango",
    ),
    (
        "Estructura del documento",
        "Índice final, transiciones A→B, resumen/conclusiones marco (conclusiones numéricas las cierra B)",
    ),
]
for i, (b, q) in enumerate(bloques_a, start=1):
    tab_a.rows[i].cells[0].text = b
    tab_a.rows[i].cells[1].text = q

p = doc.add_paragraph()
p.add_run("Entregable del Equipo A hacia el grupo: ").bold = True
p.add_run(
    "borrador Capa A listo para pegar + brief de 1 página para B (“qué números y figuras necesitamos en el informe y dónde van”)."
)

# --- CAPA B ---
doc.add_heading("Capa B — Ejecución bayesiana, cómputo y resultados", level=1)

p = doc.add_paragraph()
p.add_run("Descripción. ").bold = True
p.add_run(
    "Es la materialización del modelo: EDA mínimo que justifique la spec, priors, posterior por MH, diagnósticos, "
    "chequeo predictivo, validación en 24 meses, traducción a ventas/rango de inventario e interpretación bayesiana "
    "(IC creíbles, P(β_j > 0 | y), predictiva). Incluye redacción de esos resultados y evidencia reproducible "
    "(notebook corrido, tablas exportadas)."
)

p = doc.add_paragraph()
p.add_run("Objetivo. ").bold = True
p.add_run(
    "Demostrar que el diseño de A se ejecutó bien, responder la pregunta de investigación con datos "
    "(qué se asocia, cuánta incertidumbre queda) y entregar el producto útil (rango de referencia en USD + limitaciones honestas), "
    "contrastando con lo que A había anticipado en §3.6."
)

doc.add_paragraph("Cómo se mide que se logró (criterios de “capa lista”)", style="List Bullet")
criterios_b = [
    "Modelo = spec acordada: misma verosimilitud t, κ_m, ψ, priors y holdout que el diseño A describe.",
    "Inferencia confiable: R̂ ≲ 1.01, ESS reportado, trazas; log-posterior verificada (scipy vs implementación).",
    "Pregunta respondida en tres niveles: (a) coeficientes + P(· | y); (b) R² / variación explicada con definición clara; (c) rango predictivo inventario (p. ej. Tabla 10) con lectura para compras/finanzas.",
    "Validación externa: métricas y cobertura en 24 meses vs tres referencias; se dice explícitamente si el punto mejora o no y si el rango sí aporta.",
    "Contraste Paso 9: tabla o sección esperado / contrario / nulo vs observado (puente con Equipo A).",
    "Paquete congelado: CSV/figuras con nombres estables para que A no invente números en §3.8 y conclusiones finales.",
]
for c in criterios_b:
    doc.add_paragraph(c, style="List Bullet 2")

doc.add_paragraph(
    "Bloques de trabajo del Equipo B (Quijano reparte adentro)", style="List Bullet"
)
tab_b = doc.add_table(rows=5, cols=2)
tab_b.style = "Table Grid"
tab_b.rows[0].cells[0].text = "Bloque"
tab_b.rows[0].cells[1].text = "Qué incluye (conjunto)"
bloques_b = [
    ("Cómputo", "Notebook, MH, exports, figuras, semilla fija"),
    ("Modelamiento escrito", "Ecuaciones, priors, apéndice log-posterior (breve)"),
    (
        "Resultados e interpretación",
        "Posterior, PPC, prueba 24 meses, inventario, limitaciones empíricas",
    ),
    (
        "Redacción Capa B",
        "Secciones B del informe + texto que A pegará en §3.8 y conclusiones numéricas",
    ),
]
for i, (b, q) in enumerate(bloques_b, start=1):
    tab_b.rows[i].cells[0].text = b
    tab_b.rows[i].cells[1].text = q

p = doc.add_paragraph()
p.add_run("Entregable del Equipo B hacia el grupo: ").bold = True
p.add_run(
    "Capa B redactada + paquete de números congelados + notebook ejecutado (o equivalente)."
)

# --- Colaboración ---
doc.add_heading("Cómo trabajan juntos (solo 3 momentos globales)", level=1)
tab_m = doc.add_table(rows=4, cols=3)
tab_m.style = "Table Grid"
for j, h in enumerate(["Momento", "Qué pasa", "Quién"]):
    tab_m.rows[0].cells[j].text = h
momentos = [
    ("1. Arranque", "A entrega índice + expectativas §3.6; B confirma que el diseño es implementable", "A → B"),
    (
        "2. Congelación",
        "B entrega paquete numérico + borrador resultados; A completa §3.8 y pide ajustes de redacción, no de modelo",
        "B → A",
    ),
    (
        "3. Cierre",
        "Un solo PDF: A+B; los dos equipos pasan checklist de su capa; 30 min lectura cruzada “¿suena un solo argumento?”",
        "Todos",
    ),
]
for i, row in enumerate(momentos, start=1):
    for j, txt in enumerate(row):
        tab_m.rows[i].cells[j].text = txt

doc.add_paragraph(
    "No hace falta reestructurar el repo ni el notebook por ahora; hace falta dos entregables de capa y dos checklists de “objetivo logrado”."
)

doc.add_heading("Resumen en una línea por equipo", level=1)
doc.add_paragraph(
    "Triana + Jiménez (A): “Convencemos de que medir y validar así tiene sentido, y dejamos escrito qué debería salir del modelo.”",
    style="List Bullet",
)
doc.add_paragraph(
    "Quijano (B): “Corremos el Bayes, mostramos resultados con rigor y respondemos la pregunta con números y límites honestos.”",
    style="List Bullet",
)

doc.add_paragraph()
doc.add_paragraph(
    "Siguiente paso opcional: plantilla de 2 páginas (“Brief A→B” y “Checklist capa A / capa B”) para copiar en Notion, sin tocar el código."
).italic = True

try:
    doc.save(out)
    print(out)
except PermissionError:
    doc.save(alt)
    print(alt)
    print("(Cierra el .docx abierto en Word y vuelve a correr el script para sobrescribir el archivo original.)")
