# -*- coding: utf-8 -*-
"""Guía de sustentación basada en Incertidumbre..._actualizado.pdf."""
from pathlib import Path
from fpdf import FPDF

BASE = Path(__file__).resolve().parent
GUIA = BASE / "guia"
GUIA.mkdir(exist_ok=True)
OUT = GUIA / "Guia_sustentacion_PDF_actualizado.pdf"
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"
FONT_I = r"C:\Windows\Fonts\ariali.ttf"


class Guia(FPDF):
    def footer(self):
        self.set_y(-14)
        self.set_font("A", "", 9)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f"Pagina {self.page_no()}", align="C")


pdf = Guia()
pdf.set_auto_page_break(auto=True, margin=16)
pdf.set_margins(16, 16, 16)
pdf.add_font("A", "", FONT)
pdf.add_font("A", "B", FONT_B)
pdf.add_font("A", "I", FONT_I)


def w():
    return pdf.w - pdf.l_margin - pdf.r_margin


def h1(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("A", "B", 15)
    pdf.multi_cell(w(), 7, t)
    pdf.ln(2)


def h2(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("A", "B", 12)
    pdf.multi_cell(w(), 6, t)
    pdf.ln(1)


def h3(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("A", "B", 11)
    pdf.multi_cell(w(), 5.5, t)
    pdf.ln(0.5)


def body(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("A", "", 10.5)
    pdf.multi_cell(w(), 5.2, t)
    pdf.ln(1)


def bullet(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("A", "", 10.5)
    pdf.multi_cell(w(), 5.2, "- " + t)
    pdf.ln(0.3)


def say(t):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("A", "I", 10.5)
    pdf.multi_cell(w(), 5.2, t)
    pdf.ln(0.5)


def symbol_row(simbolo, nombre, que_es, influye, por_que):
    pdf.set_font("A", "B", 10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w(), 5, f"{simbolo} — {nombre}")
    pdf.set_font("A", "", 10)
    for label, txt in [
        ("Que es (simple):", que_es),
        ("En la analitica:", influye),
        ("Por que lo usamos:", por_que),
    ]:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("A", "B", 10)
        pdf.cell(38, 5, label)
        pdf.set_font("A", "", 10)
        pdf.multi_cell(w() - 38, 5, txt)
    pdf.ln(1)


pdf.add_page()
h1("Guia para sustentar — PDF actualizado")
body(
    "Archivo de referencia: compañeros/Incertidumbre en ventas de muebles y hogar_actualizado.pdf "
    "(4 diapositivas). Curso: Estadistica Bayesiana, Universidad Externado. "
    "Informe y codigo: entrega final/proyecto_fina_bayesiana.pdf y codigo_final_v3f.ipynb."
)

h2("Contexto en una historia corta")
body(
    "Imagina una tienda de muebles que cada mes debe adivinar cuanto comprar. Si apuesta poco, se queda sin "
    "stock; si apuesta mucho, la bodega se llena. Casi siempre usan UN numero. Nosotros miramos todo el "
    "mercado de muebles y hogar en Estados Unidos (FRED/Census), mes a mes desde 1992 hasta 2026: "
    "413 meses. No reemplazamos el pronostico interno de una empresa; damos un mapa de cuanto puede "
    "moverse el sector y con que certeza, para que compras, comercial y finanzas hablen el mismo idioma."
)
body(
    "Pregunta del proyecto: cuanto pueden subir o bajar las ventas mensuales del sector y con que seguridad "
    "lo decimos. Herramienta: regresion bayesiana con incertidumbre honesta (intervalos y probabilidades). "
    "Mensaje honesto del trabajo: el punto central no mejora a la media historica; los intervalos del 90% "
    "sí se calibran mejor (23 de 24 meses de prueba)."
)

h2("Diapositiva 1 — Planteamiento (que hay y que contar)")
bullet("Titulo: decidir inventario con una sola cifra.")
bullet("Riesgo arriba: venden mucho mas -> faltantes. Riesgo abajo: venden mucho menos -> bodega llena.")
bullet("Pregunta grande (caja azul): cuanto suben o bajan ventas mensuales de muebles/hogar en EE.UU. "
       "y con que certeza.")
bullet("413 meses, mar. 1992 - jul. 2026, datos Census via FRED.")
bullet("Barra amarilla: mismo mes = van juntos, no causalidad; es el clima del sector, no una tienda.")
say(
    "Que decir: «Partimos del problema de inventario. Nuestra pregunta es sectorial y bayesiana: no un "
    "numero, sino cuanto puede moverse el mes con probabilidad. Desde ya: no es causalidad ni SKU.»"
)

h2("Diapositiva 2 — Estado del arte (que hay y que contar)")
bullet("Lenza y Primiceri: no borrar COVID; amplificador kappa.")
bullet("Van Steenbergen y Mes: medir confiabilidad de todo el pronostico, no solo el centro.")
bullet("Lange / t-Student: colas pesadas; la normal seria demasiado optimista.")
bullet("Gelman: priors debiles estabilizan sin imponer el resultado.")
bullet("Frase inferior: clasico = numero + p-valor; Bayes = intervalos y probabilidades con los datos.")
say(
    "Puente hacia diapositiva 3: «Estos autores nos dicen QUE necesitamos: no esconder 2020, medir "
    "incertidumbre, tolerar sustos, priors suaves. En la siguiente lamina les mostramos COMO lo montamos "
    "en ecuaciones y en el codigo.»"
)

pdf.add_page()
h1("PARTE A — Diapositiva 3: que hay en la lamina (recorrido visual)")
body(
    "Tu diapositiva se llama «Metodologia y validez del diseno». Subtitulo: «Como construimos el modelo». "
    "Abajo va cada cajita como si le explicaras a alguien de 10 anos."
)

h3("Franja azul superior")
body(
    "y = cambio mensual de las ventas (100 x delta-log), explicado por 8 covariables estandarizadas "
    "del mismo mes. Traduccion: y es casi el porcentaje en que subio o bajo el sector este mes respecto "
    "al mes anterior; las 8 ayudantes son otras ventas macro del mismo mes, puestas en la misma escala."
)

h3("Tarjeta «Error — t de Student»")
body(
    "Cuenta que los errores no son campana perfecta: hay meses locos. La t permite colas gordas "
    "(sustos grandes sin romper el modelo)."
)

h3("Tarjeta kappa — marzo a junio 2020")
body(
    "En esos cuatro meses permitimos que el error sea mas grande (kappa). No borramos el COVID: "
    "lo etiquetamos para que no empuje todo lo demas."
)

h3("Tarjeta psi — desde julio 2020")
body(
    "Despues de julio 2020 el mercado se movio mas (desviacion del cambio ~1,54 a ~3,25). psi es el "
    "interruptor que deja respirar esa nueva volatilidad."
)

h3("Tarjetas 389 entrenar / 24 probar")
body(
    "389 meses: aqui el modelo aprende. 24 meses finales (ago. 2024 - jul. 2026): prueba honesta; "
    "no entran al exploratorio ni al ajuste (sin trampa)."
)

h3("Tarjeta Metropolis-Hastings — 4 cadenas")
body(
    "Metropolis-Hastings es el algoritmo MCMC que pasea muchas versiones posibles de los parametros; "
    "4 cadenas independientes para verificar convergencia. R-hat menor que 1,01; 16 parametros; "
    "priors debiles. Chequeo predictivo en entrenamiento: simular datos como los vistos y ver si "
    "el modelo se comporta razonable (solo en train)."
)

h3("Barra amarilla inferior de diap. 3")
body(
    "Asociacion contemporanea · no pronostico con anticipacion. Refuerza la diap. 1: medimos quien "
    "se mueve junto en el mismo mes, no «X del mes pasado causa Y manana»."
)

pdf.add_page()
h1("PARTE B — Diccionario de simbolos y parametros (diapositiva 3)")
body(
    "Para cada pieza: nombre, significado simple, como influye en el analisis, y por que esta ahi."
)

symbol_row(
    "y (y_t)",
    "Crecimiento mensual de ventas de muebles/hogar",
    "100 veces el cambio del logaritmo de ventas de un mes al otro. Es como un porcentaje aproximado.",
    "Es lo que queremos entender y predecir: que tan brusco fue el mes.",
    "El inventario vive en cambios mes a mes, no solo en niveles eternos.",
)
symbol_row(
    "delta-log (100 x Delta log)",
    "Diferencia de logaritmos",
    "Resta log(venta_mes) - log(venta_mes_anterior), x100. Cambios relativos estables en el tiempo.",
    "Define la escala de y y hace comparables decadas distintas.",
    "Evita que un millon de dolares en 1992 pese distinto que en 2024.",
)
symbol_row(
    "z_j (z_jt)",
    "Covariable estandarizada j en el mes t",
    "Cada ayudante (electronica, construccion, etc.) medida en unidades de desviacion tipica "
    "(SD de meses pre-mar. 2020).",
    "Permite decir «si electronica sube 1 desviacion, muebles suben beta_j desviaciones».",
    "Sin estandarizar, las escalas no se comparan (gasolina vs ingreso).",
)
symbol_row(
    "beta_0 (beta cero)",
    "Intercepto",
    "Crecimiento de muebles cuando todas las z estan en su promedio (cero).",
    "Ancla el nivel medio del cambio mensual.",
    "Toda recta necesita punto de partida; prior debil N(0,1).",
)
symbol_row(
    "beta_j (betas)",
    "Coeficientes de regresion (j=1..8)",
    "Cuanto se asocia el cambio de cada z_j con el cambio de muebles, en la misma escala z.",
    "En diap. 4 veras los +0.64 etc. (no causalidad).",
    "Traducen el mapa macro: que sectores caminan juntos con muebles.",
)

pdf.add_page()
body("Las 8 variables z del proyecto (mismo mes salvo donde dice rezago):")
bullet("crec_electro — ventas de electronica.")
bullet("crec_sin_tienda — ventas sin tienda (online).")
bullet("crec_construccion — materiales de construccion y jardin.")
bullet("crec_tiendas_generales — tiendas generales.")
bullet("crec_gasolineras — gasolineras (proxy costo de usar auto).")
bullet("crec_ingreso_disponible — ingreso personal.")
bullet("razon_inv_ventas_rezago1 — inventarios/ventas minoristas (1 mes antes).")
bullet("crec_muebles_hogar_rezago1 — crecimiento de muebles del mes anterior (inercia).")

symbol_row(
    "epsilon_t (e_t)",
    "Error del mes t",
    "Lo que el modelo no explica con las betas: sorpresa del mercado.",
    "Alimenta la incertidumbre de cada mes.",
    "Ningun modelo captura todo; epsilon guarda el resto.",
)
symbol_row(
    "t_nu (t de Student, nu)",
    "Error con colas pesadas",
    "Distribucion t con grados de libertad nu. Mas nu -> mas parecida a normal.",
    "Controla que tan extremos pueden ser los meses malos.",
    "EDA: hay colas; normal subestimaria sustos (Lange).",
)
symbol_row(
    "nu",
    "Grados de libertad de la t",
    "Parametro que afloja o aprieta las colas.",
    "Nu bajo = mas sustos probables; nu alto = colas mas delgadas.",
    "Prior Gamma debil; se estima con los datos.",
)
symbol_row(
    "sigma",
    "Escala base del error",
    "Tamano tipico del error cuando lambda=1 y psi no aplica.",
    "Fija el ancho de intervalos en meses tranquilos.",
    "Prior half-normal; siempre positiva.",
)
symbol_row(
    "sigma_t",
    "Error escalado del mes t",
    "sigma_t = sigma x lambda_t x psi^(indicador desde jul-2020).",
    "Mes t puede ser mas nervioso que otro (COVID o post-2020).",
    "Un solo sigma seria injusto tras la pandemia.",
)
symbol_row(
    "lambda_t",
    "Multiplicador mensual de volatilidad",
    "En mar-jun 2020 vale kappa_m; en otros meses vale 1.",
    "Permite meses COVID sin borrarlos.",
    "Sigue a Lenza: modelar volatilidad COVID, no deletear.",
)
symbol_row(
    "kappa (kappa_m)",
    "Amplificador COVID (4 meses)",
    "Cuatro numeros (mar, abr, may, jun 2020) >= 0 que agrandan el error esos meses.",
    "Absorbe picos sin deformar betas de todo el siglo.",
    "16 parametros incluyen log kappa_m con prior half-normal.",
)
symbol_row(
    "psi",
    "Factor post-julio 2020",
    "Multiplica error desde julio 2020 (aprox. 1,5 en posterior).",
    "Reconoce que despues de 2020 el mercado se movio mas (EDA 1,54 a 3,25).",
    "Un interruptor de epoca, no un mes suelto.",
)

pdf.add_page()
symbol_row(
    "Prior debil",
    "Opinion inicial suave (Gelman)",
    "Distribucion antes de ver datos; no fuerza el resultado.",
    "Betas ~ N(0,1), sigma half-normal, etc.",
    "Estabiliza sin imponer historia de negocio fuerte.",
)
symbol_row(
    "16 parametros",
    "Todo lo que estimamos",
    "beta_0 + 8 betas + sigma + nu + 4 kappa + psi (en log donde aplica).",
    "Cada uno tiene posterior e intervalos bayesianos.",
    "Cuenta total del MH y del articulo.",
)
symbol_row(
    "Metropolis-Hastings (MH)",
    "Algoritmo MCMC",
    "Propone pasos al azar; acepta si mejoran la posterior; repite miles de veces.",
    "Genera miles de mundos compatibles con datos y priors.",
    "La posterior no tiene formula cerrada; hay que muestrear.",
)
symbol_row(
    "4 cadenas",
    "Cuatro simulaciones paralelas",
    "Corren igual con distintas semillas.",
    "Si convergen al mismo sitio, confiamos mas.",
    "Buena practica MCMC.",
)
symbol_row(
    "R-hat",
    "Diagnostic R-hat",
    "Compara variacion entre cadenas vs dentro de cadena. Meta < 1,01.",
    "Si R-hat alto, no confiar en intervalos.",
    "Criterio de convergencia en la lamina.",
)
symbol_row(
    "Chequeo predictivo (entrenamiento)",
    "Simular datos con el modelo ajustado",
    "Ver si datos simulados parecen reales (solo 389 meses train).",
    "Valida que el modelo no sea absurdo; no usa holdout.",
    "Validez del diseno, no optimismo en prueba.",
)
symbol_row(
    "389 / 24",
    "Particion temporal",
    "389 = aprendizaje; 24 = prueba final ago 2024 - jul 2026.",
    "Metricas de diap. 4 (RMSE, 23/24) salen de los 24.",
    "Sin fuga de informacion del futuro al pasado.",
)

pdf.add_page()
h1("PARTE C — Guion detallado para TU diapositiva 3 (oral)")
say("Apertura (15 s): «En la diapositiva anterior vieron el POR QUE bayesiano. Aqui el COMO.»")

h3("Paso 1 — Franja azul (y y las 8 z)")
say(
    "«Medimos y: cuanto cambio el sector este mes, en porcentaje aproximado. Metemos ocho "
    "companeros del mismo mes — electronica, construccion, ingreso, etc. — todos en la misma "
    "regla de medida (estandarizados con meses tranquilos antes de marzo 2020).»"
)

h3("Paso 2 — Error t")
say(
    "«No asumimos campana perfecta: usamos t de Student porque hay meses muy extremos. Si usaramos "
    "normal, diríamos que los sustos son imposibles y mentiriamos sobre el riesgo.»"
)

h3("Paso 3 — kappa y psi (unir las dos tarjetas)")
say(
    "«En marzo a junio 2020 kappa agranda el error: no borramos esos meses. Desde julio 2020 psi "
    "porque el mercado entero se movio mas — lo vimos en el dato: desviacion de 1,54 a 3,25. "
    "kappa es por mes loco; psi es por epoca nueva.»"
)

h3("Paso 4 — 389 y 24")
say(
    "«Ensenamos con 389 meses. Guardamos 24 al final como examen sorpresa: eso es validez del "
    "diseno — no miramos esas respuestas al estudiar el pasado.»"
)

h3("Paso 5 — Metropolis-Hastings")
say(
    "«Con Metropolis-Hastings y cuatro cadenas dibujamos miles de curvas posibles. R-hat cerca de 1 "
    "significa que las cuatro historias coinciden. Dieciséis parametros con priors debiles. Chequeo "
    "predictivo solo en entrenamiento: el modelo debe poder fingir datos parecidos a los que vio.»"
)

h3("Paso 6 — Barra amarilla + cierre hacia diap. 4")
say(
    "«Repito: asociacion contemporanea, no pronostico con anticipacion. En la siguiente lamina "
    "respondemos: ¿sirve en el examen de 24 meses? Ahi veran RMSE, 23 de 24 y los betas.»"
)

h1("PARTE D — Retorica: unir diapositivas y metricas entre si")

h2("Puente 2 -> 3 (ideas -> ecuacion)")
body(
    "Diap. 2 dijo: no borrar COVID (Lenza), medir incertidumbre entera (Van Steenbergen), colas "
    "t (Lange), priors debiles (Gelman). Diap. 3 responde pieza por pieza: kappa = Lenza; t y nu = "
    "Lange; psi = EDA post-2020; priors y MH = Gelman + Bayes; chequeo predictivo = Van Steenbergen "
    "(confiabilidad del modelo, no solo coeficientes)."
)
say(
    "Frase puente: «Cada tarjeta de metodologia es la respuesta a una tarjeta de literatura.»"
)

h2("Puente 3 -> 4 (modelo -> resultados)")
body(
    "De la 3 llevas tres hilos a la 4: (1) Que es y y que son las betas -> en 4 lees +0.64 electronica "
    "(asociacion estandarizada, IC 95%). (2) sigma, psi, t -> en 4 ancho de intervalos 6,9 vs 9,5 y "
    "23/24 cobertura. (3) 389/24 y MH -> en 4 RMSE 2,04 vs 2,02 es el examen honesto; R2 cae en "
    "prueba (ruido real)."
)
say(
    "Frase puente: «Montamos el circo en la 3; en la 4 contamos si el circo atrapa al publico — "
    "no con un truco de numero unico, sino con el cerco del 90%.»"
)

h2("Como conectar metricas entre si (mapa mental)")
bullet(
    "Betas (diap. 4) nacen de z y y (diap. 3): «quien camina con muebles el mismo mes»."
)
bullet(
    "psi y t (diap. 3) explican por que intervalos en 4 son mas angostos pero honestos (6,9 vs 9,5)."
)
bullet(
    "RMSE (diap. 4) mide el centro; 23/24 mide el cerco. Mensaje: empate en centro, gana el cerco."
)
bullet(
    "R2 entrenamiento vs prueba (0,31 vs 0,05): el modelo aprende patrones viejos; meses nuevos "
    "siguen ruidosos — coherente con errores t y psi."
)
bullet(
    "Agosto 2026 (diap. 4): usa la posterior del modelo (diap. 3) para nivel en millones USD; "
    "prospectivo, sin validar aun."
)

pdf.add_page()
h1("PARTE E — Diapositiva 4 — Resultados (explicacion simple)")
bullet("Titulo: el centro no mejora, el intervalo si.")
bullet("RMSE 2,04 vs 2,02: error tipico del punto = media historica (sin humo).")
bullet("23/24 meses dentro del IC 90%; diciembre 2024 salio (decirlo con honestidad).")
bullet("Ancho 6,9 vs 9,5: intervalos mas utiles que regla simple sin covariables.")
bullet("Betas estandarizados: electronica +0,64, construccion +0,40, tiendas +0,27, gasolineras -0,18.")
bullet("R2 ~ 0,31 train, ~ 0,05 test: poca explicacion en meses nuevos.")
bullet("Agosto 2026 prospectivo: 10 134 - 11 050 MUSD (90%), mediana 10 542.")
bullet("Cierre: empresa escala la forma del rango; limites: agregado US, asociacion, 24 meses prueba.")
say(
    "Cierre oral (20 s): «Nuestro regalo es el mapa de incertidumbre del sector para inventario "
    "discutido en común. Bayes nos dejo honestos: el centro empata, el intervalo gana.»"
)

h2("Si te preguntan en Q&A (diap. 3)")
bullet("Causalidad? No. Mismo mes (y rezagos explicitos en dos z).")
bullet("Por que no borrar COVID? Subestimarias riesgo (Lenza).")
bullet("Por que MH y no solo formulas? Posterior compleja; hay que muestrear.")
bullet("Que es R-hat? Termometro de convergencia de cadenas.")
bullet("16 parametros? beta_0 + 8 betas + sigma + nu + 4 kappa + psi.")

h2("Checklist antes de presentar diap. 3")
bullet("Decir asociacion / no pronostico (barra amarilla).")
bullet("Separar kappa (4 meses) y psi (desde jul-2020).")
bullet("Decir 389/24 sin trampa.")
bullet("Nombrar Metropolis-Hastings y chequeo predictivo (solo train).")
bullet("Puente claro a diap. 4: centro vs intervalo.")

pdf.output(OUT)
print("OK:", OUT)
