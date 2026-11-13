# -*- coding: utf-8 -*-
"""Genera PPTX corregido y PDF guía para sustentación. No modifica v2."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from fpdf import FPDF

BASE = Path(__file__).resolve().parent
OUT_PPTX = BASE / "compañeros" / "Presentacion_incertidumbre_inventario_v3_corregida.pptx"
GUIA_DIR = BASE / "guia"
GUIA_DIR.mkdir(exist_ok=True)
OUT_PDF = GUIA_DIR / "Guia_contexto_y_diapositivas_sustentacion.pdf"
FONT = r"C:\Windows\Fonts\arial.ttf"

# --- PPTX ---
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_title_slide(title: str, bullets: list[str], subtitle: str = ""):
    slide = prs.slides.add_slide(BLANK)
    top = Inches(0.35)
    box = slide.shapes.add_textbox(Inches(0.6), top, Inches(12.1), Inches(1.2))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    if subtitle:
        box2 = slide.shapes.add_textbox(Inches(0.6), Inches(1.35), Inches(12.1), Inches(0.55))
        p2 = box2.text_frame.paragraphs[0]
        p2.text = subtitle
        p2.font.size = Pt(14)
        p2.font.italic = True
    body = slide.shapes.add_textbox(Inches(0.75), Inches(1.95), Inches(11.8), Inches(5.2))
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate(bullets):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.text = line
        para.font.size = Pt(17)
        para.space_after = Pt(8)
        if line.startswith("•"):
            para.level = 0


add_title_slide(
    "Diapositiva 1 — Planteamiento y formulación",
    "¿Qué tan lejos puede quedar la demanda de lo esperado?",
    "Universidad Externado · Estadística Bayesiana · Proyecto final",
)

slide1 = prs.slides[-1]
extra = slide1.shapes.add_textbox(Inches(0.75), Inches(2.35), Inches(11.8), Inches(4.8))
tf1 = extra.text_frame
tf1.word_wrap = True
lines1 = [
    "Problema: en inventario se usa una sola cifra de ventas; si la realidad se aleja mucho, hay faltantes o bodega llena.",
    "Compras, comercial y finanzas discuten con intuición distinta, sin medir cuánto puede variar el mercado.",
    "Pregunta: ¿Cuánto pueden subir o bajar las ventas mensuales de muebles y hogar en EE. UU., y con qué certeza?",
    "Objetivo: estimar ese cambio y su incertidumbre (modelo bayesiano) como referencia para inventario.",
    "Datos: FRED / Census — mensual, mar. 1992 – jul. 2026 (413 meses). Ámbito: sector agregado EE. UU.",
    "Límites de diseño: covariables del mismo mes (asociación, no causalidad); no sustituye pronóstico por producto/SKU.",
]
for i, t in enumerate(lines1):
    p = tf1.paragraphs[0] if i == 0 else tf1.add_paragraph()
    p.text = "• " + t
    p.font.size = Pt(16)
    p.space_after = Pt(6)

# Slide 2
slide = prs.slides.add_slide(BLANK)
tbox = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12), Inches(0.8))
tbox.text_frame.paragraphs[0].text = "Diapositiva 2 — Estado del arte y contexto teórico"
tbox.text_frame.paragraphs[0].font.size = Pt(26)
tbox.text_frame.paragraphs[0].font.bold = True
body = slide.shapes.add_textbox(Inches(0.75), Inches(1.3), Inches(11.8), Inches(5.8))
tf = body.text_frame
tf.word_wrap = True
lines2 = [
    "Lenza y Primiceri (2022): borrar mar.–jun. 2020 puede ayudar a estimar, pero subestima incertidumbre al pronosticar → conservamos COVID con factores κ.",
    "Van Steenbergen y Mes (2020): poco se estudia qué tan confiable es un pronóstico → medimos la incertidumbre completa.",
    "Lange et al. (1989): la t de Student tolera colas pesadas → errores t, no normales.",
    "Gelman (2006/2008): priors débilmente informativas estabilizan sin forzar resultados.",
    "Bayes entrega intervalos y probabilidades P(·|datos), no solo “un número” ni p-valores aislados.",
]
for i, t in enumerate(lines2):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = "• " + t
    p.font.size = Pt(17)
    p.space_after = Pt(8)

# Slide 3
slide = prs.slides.add_slide(BLANK)
tbox = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.75))
tbox.text_frame.paragraphs[0].text = "Diapositiva 3 — Enfoque analítico y metodología"
tbox.text_frame.paragraphs[0].font.size = Pt(26)
tbox.text_frame.paragraphs[0].font.bold = True
body = slide.shapes.add_textbox(Inches(0.75), Inches(1.15), Inches(11.8), Inches(6))
tf = body.text_frame
tf.word_wrap = True
lines3 = [
    "Respuesta yₜ = 100·Δlog(ventas). Regresión bayesiana con 8 covariables estandarizadas (meses normales del entrenamiento).",
    "yₜ = β₀ + Σβⱼzⱼₜ + εₜ;  εₜ ~ tν(0, σₜ);  σₜ = σ·λₜ·ψᴵ⁽ᵗ≥jul-2020⁾;  λₜ = κₘ en mar.–jun. 2020.",
    "EDA: SD ~1.54 antes de mar. 2020 y ~3.25 desde jul. 2020 → justifica ψ; t mejor que normal (colas pesadas).",
    "Partición: 389 meses entrenamiento · 24 meses prueba (ago. 2024 – jul. 2026), sin usar prueba en EDA ni ajuste.",
    "Priors: βⱼ ~ N(0,1); σ half-normal; ν Gamma; log κₘ y log ψ (16 parámetros en total).",
    "Inferencia: Metropolis–Hastings, 4 cadenas, burn-in + muestreo; criterio R̂ < 1.01 y ESS alto; chequeo predictivo en entrenamiento.",
    "Importante: asociación contemporánea — no es pronóstico con meses de anticipación.",
]
for i, t in enumerate(lines3):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = "• " + t
    p.font.size = Pt(15)
    p.space_after = Pt(5)

# Slide 4
slide = prs.slides.add_slide(BLANK)
tbox = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.75))
tbox.text_frame.paragraphs[0].text = "Diapositiva 4 — Resultados e implicaciones"
tbox.text_frame.paragraphs[0].font.size = Pt(26)
tbox.text_frame.paragraphs[0].font.bold = True
body = slide.shapes.add_textbox(Inches(0.75), Inches(1.1), Inches(11.8), Inches(6.1))
tf = body.text_frame
tf.word_wrap = True
lines4 = [
    "Mensaje: no gana en el punto, gana en la incertidumbre bien calibrada.",
    "Asociaciones (β estandarizados, IC 95%): electrónica +0.64, construcción +0.40, tiendas generales +0.27; gasolineras −0.18 (cautela); resto sin evidencia clara.",
    "R² bayesiano ~0.31 entrenamiento vs ~0.05 prueba → poca explicación en meses nuevos.",
    "Validación 24 meses: RMSE 2.04 vs media histórica 2.02; persistencia 3.28 (sí mejora vs esta); cobertura IC 90%: 23/24; ancho medio 6.9 vs 9.5 (t solo en y).",
    "Volatilidad: ψ ≈ 1.5 post-2020 (error típico ~1.4 → ~2.1 puntos de crecimiento).",
    "Agosto 2026 (prospectivo): ventas sector 10 134 – 10 542 – 11 050 MUSD (piso–mediana–techo al 90%); brecha mediana→techo ~508 M (~4.8%) referencia de colchón.",
    "Implicación: la empresa escala el rango macro (participación s o factor k) para techo, piso e inventario de seguridad — complementa, no reemplaza, pronóstico interno.",
    "Límites: solo 24 meses de prueba; agregado US; asociación no causal; agosto 2026 sin validar; diciembre 2024 fuera del 90%.",
]
for i, t in enumerate(lines4):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = "• " + t
    p.font.size = Pt(14)
    p.space_after = Pt(4)

prs.save(OUT_PPTX)
print("PPTX:", OUT_PPTX)


class GuiaPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("ArialUni", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


pdf = GuiaPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(18, 18, 18)
pdf.add_font("ArialUni", "", FONT)
pdf.add_font("ArialUni", "B", r"C:\Windows\Fonts\arialbd.ttf")
pdf.add_font("ArialUni", "I", r"C:\Windows\Fonts\ariali.ttf")


def _w():
    return pdf.w - pdf.l_margin - pdf.r_margin


def h1(text):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "B", 16)
    pdf.multi_cell(_w(), 8, text)
    pdf.ln(2)


def h2(text):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "B", 13)
    pdf.multi_cell(_w(), 7, text)
    pdf.ln(1)


def body(text):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "", 11)
    pdf.multi_cell(_w(), 6, text)
    pdf.ln(2)


def bullet(text):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "", 11)
    pdf.multi_cell(_w(), 6, "- " + text)
    pdf.ln(1)


pdf.add_page()
h1("Guía para la sustentación — Proyecto de Estadística Bayesiana")
body(
    "Equipo: Juan Esteban Jiménez, David Quijano, Juan Andrés Zambrano, Juan Angel Triana. "
    "Universidad Externado de Colombia, Ciencia de Datos. "
    "Presentación usada: Presentacion_incertidumbre_inventario_v3_corregida.pptx (4 diapositivas)."
)

h2("Parte 1 — Todo el contexto (qué hicimos, cómo y qué decidimos)")
body(
    "Imagina que una tienda de cosas para el hogar tiene que adivinar cuánto va a vender el próximo mes "
    "para saber cuánto pedir al proveedor. Si pide de menos, se quedan sin productos. Si pide de más, "
    "la bodega se llena y el dinero queda quieto. Casi siempre usan UN solo número: “venderemos tanto”. "
    "Pero la vida no es tan exacta: a veces venden mucho más o mucho menos. Lo caro no es fallar un poquito; "
    "es fallar MUCHO."
)
body(
    "Nosotros miramos todo el mercado de muebles y artículos del hogar en Estados Unidos, mes por mes, "
    "desde 1992 hasta 2026, con datos públicos de FRED (como un termómetro del país). No miramos una "
    "tienda sola: miramos el clima del bosque entero para que una empresa tenga una referencia común."
)
body(
    "Pregunta final: ¿cuánto pueden subir o bajar esas ventas de un mes al otro y con qué seguridad podemos "
    "decirlo? La respuesta no es “un número mágico”, sino un RANGO: “podría quedar entre aquí y allá”, "
    "con probabilidades."
)
h2("Decisions importantes que tomamos (y por qué)")
bullet(
    "No borramos los meses locos de la COVID (marzo–junio 2020). Borrarlos haría creer que el mundo "
    "es más calmado de lo que es. Les dimos un “amplificador” propio (κ) sin tirar esos datos."
)
bullet(
    "Después de julio de 2020 el mercado se movió más (como cuando el piso está mojado y resbalas más). "
    "Pusimos un factor ψ para que el modelo admita más movimiento en esa época."
)
bullet(
    "Los errores no son “campana perfecta” (normal): hay meses muy extremos. Por eso usamos la distribución t "
    "de Student, que acepta sustos grandes sin romperse."
)
bullet(
    "Usamos Bayes porque queremos decir cosas como “hay 95% de probabilidad de que el efecto esté en este "
    "intervalo”, no solo “sí significativo / no significativo”."
)
bullet(
    "Partimos los datos en tiempo: 389 meses para enseñar al modelo y 24 meses finales para probarlo, "
    "sin hacer trampa (no miramos el futuro al estudiar el pasado)."
)
bullet(
    "Las otras variables (electrónica, construcción, etc.) son del MISMO mes que las ventas de muebles. "
    "Eso mide “se mueven juntos”, no “una causa a la otra” ni “adivinar el futuro con un mes de ventaja”."
)
bullet(
    "Trabajamos en dos capas en el equipo: Capa A (diseño, validez, historia de negocio) y Capa B "
    "(código, Bayes, números). El informe final y el notebook codigo_final_v3f.ipynb juntan todo."
)

h2("Qué salió (resultado honesto)")
body(
    "El modelo NO adivina mejor el número del centro que la media histórica (error parecido: ~2.04 vs ~2.02). "
    "Eso está bien contarlo: no vendimos humo. Lo que sí hace mejor: los intervalos del 90% acertaron en 23 de 24 "
    "meses de prueba y son más angostos que una regla simple sin nuestras variables. "
    "En palabras simples: no prometemos el número exacto, pero sí un cerco más útil alrededor de lo posible."
)
body(
    "Para agosto 2026 (futuro cercano) damos un rango de ventas del sector entre ~10 134 y ~11 050 millones de "
    "dólares (90% de confianza bayesiana), con mediana ~10 542. La empresa puede copiar la FORMA del rango "
    "(sube/baja cuánto) y aplicarla a su propio tamaño."
)

h2("Parte 2 — Qué decir en cada diapositiva (muy simple)")
body(
    "Abajo va qué significa cada lámina de la v3 y qué puedes contar en voz alta. Piensa que le explicas a "
    "alguien pequeño: pocas palabras, ideas grandes."
)

h2("Diapositiva 1 — Planteamiento")
body(
    "Qué ves: el título y la pregunta grande.\n"
    "Qué significa: “A veces la venta real no es la que esperábamos. ¿Qué tan lejos puede ir?” "
    "Compras, ventas y finanzas pelean sin una regla común. Nosotros medimos el clima del mercado entero "
    "en EE. UU., no de una sola tienda.\n"
    "Qué decir: “No venimos a adivinar un producto; venimos a decir qué tan ancho puede ser el mes del sector, "
    "para que todos discutan con el mismo mapa.”"
)
body(
    "No olvides los límites: mismo mes = “van juntos”, no “uno empuja al otro”; no es pronóstico con tiempo de "
    "sobra."
)

h2("Diapositiva 2 — Estado del arte")
body(
    "Qué ves: nombres de papers y frases cortas.\n"
    "Qué significa: otros ya dijeron tres cosas que copiamos con cabeza: (1) no esconder 2020, (2) medir "
    "confianza del pronóstico, (3) usar errores que aguanten sustos. Bayes suma: en vez de un punto, "
    "damos un abanico de posibilidades.\n"
    "Qué decir: “No inventamos Bayes; lo elegimos porque el problema pide rangos y probabilidades, "
    "como un pronóstico del tiempo con chance de lluvia, no solo ‘hace sol’.”"
)

pdf.add_page()
h2("Diapositiva 3 — Metodología")
body(
    "Qué ves: una fórmula rara y números 389/24.\n"
    "Qué significa en simple:\n"
    "  – y es ‘cuánto cambió el mes’ en porcentaje aproximado.\n"
    "  – Metemos 8 ayudantes (otras ventas, ingreso, inventario, etc.).\n"
    "  – Si el mes es de COVID, dejamos que el error sea más grande (κ).\n"
    "  – Si estamos después de julio 2020, también permitimos más movimiento (ψ).\n"
    "  – Enseñamos con 389 meses y probamos con 24 sin trampa.\n"
    "  – La computadora muestrea muchas versiones posibles del mundo (Metropolis–Hastings) hasta que "
    "las 4 cadenas coinciden (R̂ cerca de 1)."
)
body(
    "Qué decir: “Es como jugar muchas veces el mismo juego con los datos hasta entender qué tan "
    "anchos pueden ser los resultados, respetando los meses locos y el mundo después de 2020.”"
)
body(
    "No metas aquí los +0.64 todavía: eso es resultado, va en la diapositiva 4."
)

h2("Diapositiva 4 — Resultados e implicaciones")
body(
    "Qué ves: 23/24, RMSE, números de millones, límites.\n"
    "Frase estrella: “No ganamos en el punto exacto; ganamos en el cerco.”\n"
    "En simple:\n"
    "  – Electrónica, construcción y tiendas generales suelen subir/bajar con muebles (amigos que caminan juntos).\n"
    "  – Aun así, en meses nuevos explicamos poquito (R² bajo en prueba): el mercado tiene mucho ruido.\n"
    "  – El intervalo del 90% casi siempre atrapa la venta real (23 de 24) y es más estrecho que una regla simple.\n"
    "  – El error del centro es igual que mirar el promedio viejo; repetir el mes anterior es peor.\n"
    "  – Para agosto 2026 el sector podría estar entre ~10.1 y ~11.0 mil millones de dólares (90%).\n"
    "  – La empresa toma ESE rango y lo achica o agranda según su tamaño (como copiar la forma de una galleta, "
    "no el tamaño exacto)."
)
body(
    "Límites que debes decir sin miedo: pocos meses de prueba, datos del país entero, no causalidad, "
    "agosto 2026 es prospectivo, un mes se salió del intervalo (diciembre 2024). Eso muestra madurez."
)

h2("Cierre sugerido (20 segundos)")
body(
    "“Nuestro regalo no es un número único, es un mapa de incertidumbre del sector para que compras, "
    "comercial y finanzas hablen el mismo idioma al pedir inventario. Bayes nos dejó honestos: el centro "
    "no mejora, el intervalo sí. Eso es lo que defendemos.”"
)

h2("Si te preguntan cosas difíciles")
bullet("¿Causalidad? No. Mismo mes, solo ‘van juntos’.")
bullet("¿Por qué Bayes? Porque queremos probabilidades e intervalos, no solo una línea.")
bullet("¿Por qué no borrar COVID? Porque esconder sustos miente sobre el riesgo.")
bullet("¿Sirve para mi tienda en Colombia? Es referencia US; hay que escalar con el historial propio.")
bullet("¿Qué archivo corro? codigo_final_v3f.ipynb y PDF proyecto_fina_bayesiana.pdf.")

pdf.output(OUT_PDF)
print("PDF:", OUT_PDF)
