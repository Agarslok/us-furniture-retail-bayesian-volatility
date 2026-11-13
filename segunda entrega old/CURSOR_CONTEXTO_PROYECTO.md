# Contexto del proyecto — leer primero en Cursor

**Instrucción para el asistente:** Al trabajar en este repositorio, lee **este archivo completo** antes de proponer código, redacción o cambios de estructura. Resume el acuerdo del equipo, el estado de entregas y cómo está organizado el trabajo en **dos capas** (no siete partes repartidas por persona).

**Curso:** Estadística Bayesiana + Pensamiento Crítico en Ciencia de Datos 2 · 4° semestre · Universidad Externado de Colombia · Año 2026.

**Integrantes:** Juan Esteban Jiménez Aristizábal, David Adolfo Quijano Zuleta, Juan Andrés Zambrano Mora, Juan Angel Triana Olarte.

**Usuario habitual en Cursor:** Juan (Triana) — perfil ingeniero de software; prefiere iterar en código y notebooks.

---

## 1. De qué trata el proyecto (una página)

Una comercializadora de artículos para el hogar necesita criterio sobre **cuánto puede variar la demanda del sector** (no solo un pronóstico puntual) para discutir inventario entre compras, comercial y finanzas.

- **Escala del análisis:** sector agregado de **muebles y artículos para el hogar en EE. UU.**, series mensuales FRED (Census Bureau / BEA), marzo 1992 – julio 2026.
- **Pregunta:** ¿Cómo se **asocian** (no causal) el crecimiento de otras categorías del comercio, el ingreso disponible y los inventarios con el **crecimiento mensual** de ventas de muebles, y **qué incertidumbre queda** bajo inferencia bayesiana con verosimilitud **t de Student** robusta a los meses extremos de 2020?
- **Producto útil:** rango de referencia del sector (p. ej. ventas mensuales en USD con intervalo creíble), **no** el pedido exacto de una empresa. Avance 1 hablaba de producto nuevo / empresa UK; el diseño actual usa datos **US** y declara el alcance.
- **Limitaciones explícitas:** variables explicativas del **mismo mes** que la respuesta → no es pronóstico con meses de anticipación; no causalidad; series recientes sujetas a revisión FRED.

**Regla bayesiana del curso:** \(p(\theta \mid y) \propto p(y \mid \theta)\, p(\theta)\). IC **creíbles** ≠ IC de confianza frecuentista. Predictiva posterior = incertidumbre del parámetro + ruido del dato nuevo.

---

## 2. Mapa del repositorio (nombres reales en disco)

| Ruta en disco | Contenido |
|---------------|-----------|
| `README.md` | Objetivo general; nombra `01_teoria/`, `02_datos/`, `03_entregas/` (aliases lógicos). |
| `teorias/` | Teoría del curso: `Mapa_Parcial2_Completo.md`, `Guia_Interpretaciones_Parcial.md`, PDFs sesiones, HTML Gibbs/MH/HMC/Lasso. |
| `datos/base_hogar_modelo.csv` | Base oficial del modelo (413 filas). |
| `datos/diccionario_variables.csv` | Referenciado en notebooks; puede faltar en copias parciales — verificar al correr. |
| `entregas/segundaentrega_bayes.ipynb` | Notebook entrega 2 (EDA + priors; MH pendiente al cierre de esa entrega). |
| `entregas/segundaentrega_bayesiana.pdf` | PDF entrega 2 (§1–6: planteamiento, EDA, priors). |
| `entregas/Avance_2_Diseno_analitico_completado (1) (1).pdf` | Avance Pensamiento Crítico II: diseño, validez, criterios de éxito, referencias de validación. |
| `avance compañeros/bayes_avance_final.ipynb` | Notebook **más completo**: incluye MH, validación 24 meses, inventario. |
| `avance compañeros/bayes_avance_final.pdf` | Informe final (~24 páginas) con resultados numéricos. |
| `Reparto_capas_dos_equipos.docx` | Acuerdo oficial de **dos equipos / dos capas** (fuente de verdad organizacional). |
| `generar_reparto_capas_word.py` | Regenera el `.docx` de reparto (cierra Word si PermissionError). |

**Partición de datos:** columna `conjunto`: **389** meses `entrenamiento` (hasta jul 2024), **24** meses `prueba` (ago 2024 – jul 2026). La prueba **no** debe usarse en EDA, estandarización ni ajuste.

**Respuesta `Y`:** `crec_muebles_hogar` = \(100 \times \Delta \log(\text{nivel\_muebles\_hogar})\).

**Covariables `X` (8):** `crec_electro`, `crec_sin_tienda`, `crec_construccion`, `crec_tiendas_generales`, `crec_gasolineras`, `crec_ingreso_disponible`, `razon_inv_ventas_rezago1`, `crec_muebles_hogar_rezago1`.

**COVID:** `covid_2020` = 1 en mar–jun 2020. Estandarización de X con media/desv. de **meses normales** del entrenamiento (excluyen COVID y jul 2020 por rezago contaminado).

---

## 3. Modelo acordado (16 parámetros)

\[
y_t = \beta_0 + \sum_{j=1}^{8} \beta_j z_{jt} + \varepsilon_t, \qquad \varepsilon_t \sim t_\nu(0, \sigma_t)
\]

\[
\sigma_t = \sigma \cdot \lambda_t \cdot \psi^{I(t \ge \text{jul-2020})}, \quad \lambda_t = \kappa_m \text{ en mar–jun 2020, else } 1.
\]

**Priors (débilmente informativas):**

| Parámetro | Prior |
|-----------|--------|
| \(\beta_0, \beta_j\) | Normal(0, 1) |
| \(\sigma\) | Half-Normal(2) |
| \(\nu\) | Gamma(2, tasa 0.1) |
| \(\kappa_m\) | \(\log \kappa_m \sim\) Half-Normal(2), \(\kappa_m \ge 1\) |
| \(\psi\) | \(\log \psi \sim\) Normal(0, 1) |

**Inferencia:** posterior **no conjugada** → **Metropolis–Hastings**, 4 cadenas, reparametrización en log donde aplica; ver apéndice log-posterior en PDF final.

**EDA que justifica la spec:** colas pesadas (curtosis ~6.2 sin COVID), t mejor AIC/QQ que Normal; Levene confirma más volatilidad post-2020; VIF &lt; 1.73; no borrar meses COVID (Lenza & Primiceri, 2022).

---

## 4. Resultados ya documentados (referencia rápida)

Tomados de `bayes_avance_final.pdf` — **no reescribir sin recalcular** si cambia el notebook.

| Tema | Resultado aproximado |
|------|----------------------|
| MCMC | \(\hat R \lesssim 1.01\); aceptación ~0.16–0.21 |
| PPC entrenamiento (meses normales) | Cobertura ~0.51 / 0.82 / 0.91 / 0.94 (50/80/90/95 %) |
| Prueba 24 meses | RMSE modelo ~2.04; media histórica ~2.02; persistencia ~3.27 |
| CRPS / log-dens | Modelo algo mejor que t solo en historia de Y |
| Cobertura 90 % prueba | 23/24 meses |
| \(R^2\) bayesiano | ~0.31 entrenamiento vs ~0.05 prueba (limitación fuerte) |
| Lectura | Valor central no supera media histórica; **el aporte está en el rango calibrado** |

**Tres referencias de validación (Avance 2):** (1) media histórica meses normales, (2) persistencia (rezago de y), (3) t ajustada solo a y desde jul 2020.

**Criterios de éxito/parada (Avance 2, planificados antes de resultados):** cobertura 90 % ≥ 0.85 en prueba deseable; parar si \(\hat R \ge 1.01\), cobertura 90 % &lt; 0.80, o RMSE peor que persistencia.

---

## 5. Organización del equipo — DOS CAPAS, DOS EQUIPOS

**No** repartir microtareas por cabeza en el documento maestro. Cada equipo reparte **por dentro**. Aquí solo dominios y entregables de capa.

### Equipos

| Equipo | Integrantes | Dominio |
|--------|-------------|---------|
| **Equipo Capa A** | Juan Triana + Juan Jiménez | Diseño, narrativa, validez, puente al negocio y al informe |
| **Equipo Capa B** | David Quijano (+ cuarto integrante del grupo en el mismo equipo B) | Modelamiento bayesiano, cómputo, figuras/tablas numéricas, redacción de resultados |

Si el cuarto compañero no es Quijano, es miembro de **Equipo B** bajo la misma capa; A no microgestiona B.

### Capa A — Diseño, análisis y validez (Notion §3.1–3.8)

**Qué es:** Informe de diseño en **prosa** (un argumento): por qué importa, medición, datos, amenazas, estrategia, expectativas **antes** de correr el modelo.

**Objetivo:** Que alguien externo entienda el proyecto **sin** abrir el notebook y juzgue si el diseño es defendible (asociación sectorial + incertidumbre inventario; sin causalidad ni mal planteado “pronóstico adelantado”).

**Capa lista cuando:**

- Cadena en prosa: problema → pregunta → medición → datos → estrategia → validación planificada → límites.
- **§3.6** solo escenarios esperado / contrario / nulo — **sin** RMSE, posteriores ni rango MUSD de la corrida.
- **§3.7** pocas amenazas bien argumentadas + control (no checklist vacío).
- Puente a B: “Lo que el modelo debe entregar…” (posterior, 24 meses, rango USD, Paso 9).
- Coherente con Avance 2, reescrito narrativamente.
- Revisión cruzada A: uno escribe, otro revisa lógica/tono (no números MH).

**Bloques (Equipo A se reparte internamente):** Problema y puente · Medición y datos · Antecedentes · Estrategia y expectativas · Validez y ética · Estructura del documento (índice, transiciones A→B, marco de conclusiones — números los cierra B).

**Entregable A → grupo:** borrador Capa A + **brief 1 pág. para B** (qué números/figuras y dónde van).

**Una línea:** *Convencer de que medir y validar así tiene sentido, y dejar escrito qué debería salir del modelo.*

### Capa B — Ejecución bayesiana, cómputo y resultados

**Qué es:** EDA mínimo que justifica spec, priors, MH, diagnósticos, PPC, validación 24 meses, ventas/rango inventario, interpretación (\(P(\beta_j>0\mid y)\), IC creíbles, predictiva), redacción + notebook reproducible.

**Objetivo:** Ejecutar bien el diseño de A, responder la pregunta con datos y entregar rango USD + limitaciones honestas, contrastando con §3.6 de A.

**Capa lista cuando:**

- Misma spec que describe A (t, \(\kappa_m\), \(\psi\), priors, holdout).
- \(\hat R \lesssim 1.01\), ESS, trazas; log-posterior verificada vs scipy.
- Respuesta en 3 niveles: (a) coeficientes + \(P(\cdot\mid y)\); (b) \(R^2\)/variación explicada definida; (c) rango inventario + lectura compras/finanzas.
- Validación 24 meses vs 3 referencias; decir si el punto mejora o no y si el rango aporta.
- Contraste Paso 9 esperado/contrario/nulo vs observado.
- **Paquete congelado:** CSV/figuras nombres estables para que A no invente números en §3.8.

**Bloques (Quijano reparte adentro):** Cómputo · Modelamiento escrito · Resultados e interpretación · Redacción Capa B (+ texto numérico para §3.8/conclusiones).

**Entregable B → grupo:** Capa B redactada + paquete numérico congelado + notebook ejecutado.

**Una línea:** *Correr el Bayes, resultados con rigor, pregunta respondida con números y límites honestos.*

### Tres momentos globales (A ↔ B)

| Momento | Qué pasa | Flujo |
|---------|----------|--------|
| **1. Arranque** | A entrega índice + expectativas §3.6; B confirma diseño implementable | A → B |
| **2. Congelación** | B entrega números + borrador resultados; A completa §3.8 (solo redacción) | B → A |
| **3. Cierre** | Un PDF A+B; checklists de capa; 30 min lectura cruzada “¿un solo argumento?” | Todos |

**Nota:** No hace falta reestructurar repo/notebook por organización; hacen falta **dos entregables de capa** + **dos checklists** “objetivo logrado”.

**Pendiente opcional acordado en chat:** plantillas Notion “Brief A→B” y “Checklist capa A / capa B” (2 páginas).

---

## 6. Estado de entregas académicas

| Entrega | Estado |
|---------|--------|
| Segunda entrega Bayesiana (PDF §1–6 + notebook EDA/priors) | **Hecho** |
| Avance 2 Pensamiento Crítico (diseño analítico PDF) | **Hecho** |
| Notebook/PDF final con MH + prueba 24 meses | **Existe** en `avance compañeros/` (verificar si es versión entregable oficial del curso) |
| Informe final único A+B (Notion §3.1–3.8 integrado) | **En construcción** según capas |
| Brief A→B y checklists | **Pendiente** |

---

## 7. Cómo debe ayudar Cursor (directrices)

1. **Rigor pregrado avanzado:** intuición bayesiana, notación formal, no solo código.
2. **Respetar capas:** no mezclar expectativas §3.6 (A) con resultados empíricos (B); no pedir microtareas por integrante salvo que el usuario lo pida.
3. **Coherencia:** usar mismos nombres de variables, priors y holdout que el notebook/PDF.
4. **Honestidad empírica:** si RMSE no bate media histórica, decirlo; enfatizar rango/cobertura si aplica.
5. **Teoría:** consultar `teorias/Mapa_Parcial2_Completo.md` y `Guia_Interpretaciones_Parcial.md` para redacción de IC creíbles, logística, etc.
6. **Commits:** solo si el usuario lo pide explícitamente.
7. **Notebooks:** orientados a Colab (`RUTA_DRIVE`, `salidas_entrega2/`); semilla `SEMILLA = 2026`.

---

## 8. Archivos generados auxiliares (ignorar salvo que pidan)

- `Resumen_contexto_proyecto_bayesiano.docx` — resumen general antiguo (sustituido organizacionalmente por reparto dos capas).
- `Reparto_equipo_y_metricas_por_capas.docx` — versión obsoleta (7 capas por persona); usar `Reparto_capas_dos_equipos.docx`.

---

## 9. Primera acción sugerida en un dispositivo nuevo

1. Abrir este archivo y `Reparto_capas_dos_equipos.docx`.
2. Confirmar qué falta para **Capa A** (Notion) vs **Capa B** (notebook + números congelados).
3. Si toca código: partir de `avance compañeros/bayes_avance_final.ipynb` o `entregas/segundaentrega_bayes.ipynb` según lo que el equipo declare “oficial”.
4. Preguntar a Juan en qué capa/equipo está trabajando hoy antes de reestructurar el repositorio.

---

*Última actualización de contexto: noviembre 2026 — conversación Cursor (Juan / proyecto Externado).*
