# -*- coding: utf-8 -*-
"""Genera guion oral para 4 integrantes (1 diapositiva c/u + apertura/cierre)."""
from pathlib import Path
from fpdf import FPDF

BASE = Path(__file__).resolve().parent
GUIA_DIR = BASE / "guia"
GUIA_DIR.mkdir(exist_ok=True)
OUT_PDF = GUIA_DIR / "Guion_sustentacion_4_personas.pdf"
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"
FONT_I = r"C:\Windows\Fonts\ariali.ttf"


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("ArialUni", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(16, 16, 16)
pdf.add_font("ArialUni", "", FONT)
pdf.add_font("ArialUni", "B", FONT_B)
pdf.add_font("ArialUni", "I", FONT_I)


def w():
    return pdf.w - pdf.l_margin - pdf.r_margin


def h1(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "B", 15)
    pdf.multi_cell(w(), 7, t)
    pdf.ln(2)


def h2(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "B", 12)
    pdf.multi_cell(w(), 6, t)
    pdf.ln(1)


def body(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "", 11)
    pdf.multi_cell(w(), 5.5, t)
    pdf.ln(1.5)


def say(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "I", 11)
    pdf.multi_cell(w(), 5.5, t)
    pdf.ln(1)


def bullet(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("ArialUni", "", 11)
    pdf.multi_cell(w(), 5.5, "- " + t)
    pdf.ln(0.5)


pdf.add_page()
h1("Guion de sustentacion - 4 personas")
body(
    "Presentacion: Presentacion_incertidumbre_inventario_v3_corregida.pptx (4 diapositivas). "
    "Duracion sugerida total: 9 a 11 minutos + preguntas."
)
body(
    "Reparto recomendado (pueden intercambiar si alguien se siente mas comodo con metodo o resultados):"
)
bullet("Juan Angel Triana - Apertura breve + Diapositiva 1 (planteamiento).")
bullet("Juan Esteban Jimenez - Diapositiva 2 (estado del arte y Bayes).")
bullet("David Quijano - Diapositiva 3 (metodologia y validez del diseno).")
bullet("Juan Andres Zambrano - Diapositiva 4 (resultados, limites y cierre).")

h2("Reglas en grupo")
bullet("Solo habla quien tenga el micro; los otros miran al publico, no lean la pantalla palabra por palabra.")
bullet("Al terminar cada bloque: «Paso la palabra a [nombre]».")
bullet("Repitan en voz alta al menos una vez: «mismo mes = van juntos, no causalidad» y «el centro no mejora, el intervalo si».")

h2("0. Apertura conjunta - Juan Angel Triana (aprox. 40 segundos)")
say(
    "«Buenas [tardes/noches]. Somos Juan Esteban Jimenez, David Quijano, Juan Andres Zambrano y yo, "
    "Juan Angel Triana. Presentamos el trabajo final de Estadistica Bayesiana: incertidumbre en las ventas "
    "del sector de muebles y hogar en Estados Unidos, con datos mensuales de FRED desde 1992. "
    "No venimos a dar un numero magico para una tienda: venimos a mostrar un mapa de cuanto puede "
    "moverse el mercado mes a mes, para que inventario no dependa solo de una cifra. Con eso, yo "
    "abro el planteamiento.»"
)
body("[Accion: pasar a diapositiva 1.]")

h2("1. Diapositiva 1 - Juan Angel Triana (aprox. 2 minutos)")
say(
    "«Empezamos por el dolor de negocio. Cuando compras pide al proveedor, casi siempre usa una sola cifra: "
    "venderemos tanto. Si venden mucho mas, hay faltantes y clientes molestos. Si venden mucho menos, "
    "la bodega se llena y el dinero queda quieto. Comercial, compras y finanzas discuten con intuiciones "
    "distintas, sin medir que tan lejos puede quedar la demanda de lo esperado.»"
)
say(
    "«Nuestra pregunta es directa: cuanto pueden subir o bajar las ventas mensuales de muebles y hogar "
    "en Estados Unidos, y con que certeza podemos decirlo? El objetivo es estimar ese cambio y su "
    "incertidumbre con un modelo bayesiano, como referencia macro para decisiones de inventario.»"
)
say(
    "«Usamos datos publicos mensuales del Census via FRED: 413 meses, de marzo de 1992 a julio de 2026. "
    "Es el clima del bosque entero del sector en EE. UU., no una tienda ni un SKU.»"
)
say(
    "«Dos limites que deben quedar claros desde ya: las otras variables son del mismo mes que las ventas "
    "de muebles; eso es asociacion, no causalidad ni pronostico con meses de anticipacion. "
    "Paso la palabra a Juan Esteban para el marco teorico.»"
)
body("[Accion: diapositiva 2.]")

pdf.add_page()
h2("2. Diapositiva 2 - Juan Esteban Jimenez (aprox. 2 minutos)")
say(
    "«Por que Bayes y por que estos autores? Lenza y Primiceri advierten que borrar marzo a junio de 2020 "
    "puede hacer ver el mundo mas calmado de lo que es; por eso nosotros no escondemos esos meses y "
    "les damos un amplificador propio, kappa.»"
)
say(
    "«Van Steenbergen y Mes senalan que poco se mide que tan confiable es un pronostico; nosotros "
    "medimos la incertidumbre completa, no solo el punto central.»"
)
say(
    "«Lange y la familia t de Student: hay meses muy extremos, colas pesadas; un error normal seria demasiado "
    "optimista. Gelman nos recuerda priors debiles: estabilizan sin forzar el resultado.»"
)
say(
    "«En una frase: la estadistica clasica muchas veces entrega un numero y un p-valor; Bayes entrega "
    "intervalos y probabilidades dados los datos, como el pronostico del tiempo con chance de lluvia, "
    "no solo dice hace sol. Con esa idea, David explica como construimos el modelo. Paso la palabra a David.»"
)
body("[Accion: diapositiva 3.]")

h2("3. Diapositiva 3 - David Quijano (aprox. 2,5 a 3 minutos)")
say(
    "«La variable que modelamos, y, es aproximadamente cuanto cambian las ventas de un mes al otro, "
    "en escala logaritmica veces cien. Es regresion bayesiana con ocho covariables estandarizadas: "
    "electronica, construccion, ingreso, inventarios, y otras del mismo mes, todas medidas con la "
    "desviacion tipica de meses normales antes de la pandemia.»"
)
say(
    "«El error no es una campana perfecta: es t de Student. En marzo a junio de 2020 el error puede "
    "ser mas grande con kappa; desde julio de 2020 dejamos un factor psi porque vimos en el EDA que "
    "la volatilidad subio: antes de marzo 2020 la desviacion del cambio mensual ronda 1,54; "
    "desde julio 2020 ronda 3,25.»"
)
say(
    "«Para no hacer trampa: 389 meses para entrenar y 24 meses para probar, de agosto 2024 a julio 2026. "
    "El holdout no se uso en el analisis exploratorio ni en el ajuste. Dieciséis parametros en total; "
    "priors debiles en betas, half-normal en sigma, gamma en grados de libertad.»"
)
say(
    "«La inferencia es Metropolis-Hastings con cuatro cadenas; revisamos R-hat menor que 1,01 y ESS alto, "
    "y chequeo predictivo en entrenamiento. Importante repetirlo: esto mide asociacion en el mismo mes, "
    "no es pronostico con un mes de ventaja. Juan Andres cuenta que salio al probarlo. Paso la palabra a Juan Andres.»"
)
body("[Accion: diapositiva 4.]")

pdf.add_page()
h2("4. Diapositiva 4 - Juan Andres Zambrano (aprox. 2,5 a 3 minutos)")
say(
    "«El mensaje honesto del trabajo esta en esta diapositiva. No ganamos en el punto exacto: "
    "el RMSE en prueba es 2,04, casi igual que usar la media historica, 2,02. No vendemos humo. "
    "Si ganamos en el cerco: los intervalos del noventa por ciento acertaron veintitres de veinticuatro meses; "
    "el ancho medio fue 6,9 contra 9,5 de una regla simple; repetir el mes anterior da peor, 3,28.»"
)
say(
    "«En asociaciones estandarizadas, con intervalos del noventa y cinco por ciento, electronica "
    "va mas con muebles, alrededor de mas 0,64; construccion mas 0,40; tiendas generales mas 0,27; "
    "gasolineras un poco hacia abajo. El R cuadrado bayesiano es unos 0,31 en entrenamiento pero "
    "cae a unos 0,05 en prueba: en meses nuevos el mercado sigue siendo muy ruidoso.»"
)
say(
    "«Despues de 2020, psi ronda 1,5: el error tipico crece. Para agosto de 2026, prospectivo, "
    "el sector podria estar entre unos diez mil ciento treinta y cuatro y once mil cincuenta millones "
    "de dolares, con mediana diez mil quinientos cuarenta y dos, al noventa por ciento bayesiano. "
    "La empresa puede copiar la forma del rango y escalarlo con su participacion, no copiar el tamano exacto.»"
)
say(
    "«Limites sin miedo: solo veinticuatro meses de prueba; datos agregados de EE. UU.; asociacion no causal; "
    "agosto 2026 aun no se valida; diciembre de 2024 se salio del intervalo del noventa. Eso muestra madurez.»"
)

h2("5. Cierre - Juan Andres Zambrano (aprox. 25 segundos)")
say(
    "«Cerramos asi: nuestro aporte no es un numero unico, es un mapa de incertidumbre del sector "
    "para que compras, comercial y finanzas hablen el mismo idioma al pedir inventario. "
    "Bayes nos dejo honestos: el centro no mejora, el intervalo si. Gracias; quedamos atentos a preguntas.»"
)

h2("Repaso rapido - quien hace que (1 linea cada uno)")
bullet("Triana: inventario, pregunta, datos FRED, limites diseno.")
bullet("Jimenez: papers, por que t, por que Bayes, intervalos vs punto.")
bullet("Quijano: formula en simple, COVID/psi, 389/24, MH y R-hat.")
bullet("Zambrano: RMSE honesto, 23/24, betas, agosto 2026, cierre.")

h2("Si reparten preguntas en el Q&A (sugerencia)")
bullet("Causalidad / Colombia / negocio -> Triana o Jimenez.")
bullet("Papers / por que Bayes vs frecuentista -> Jimenez.")
bullet("Priors, cadenas, codigo, datos FRED -> Quijano.")
bullet("Metricas, intervalos, que conclusion llevarse -> Zambrano.")

h2("Timing de ensayo")
body(
    "Ensayen dos veces con cronometro. Si se pasan de 12 minutos, recorten ejemplos en diapositiva 2 "
    "y detalle de priors en diapositiva 3; no recorten el mensaje honesto de la diapositiva 4."
)

pdf.output(OUT_PDF)
print("PDF:", OUT_PDF)
