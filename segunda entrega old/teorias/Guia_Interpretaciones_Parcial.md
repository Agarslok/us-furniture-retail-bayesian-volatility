# Cómo interpretar en el parcial

Regla de una frase: el número describe la posterior, y la frase dice qué significa para la decisión.

Plantilla que sirve en casi todo:

1. Qué es el número (media, mediana, intervalo, probabilidad).
2. En qué escala está (probabilidad, log-odds, dólares, proporción).
3. Qué decisión cambia (¿hay asociación? ¿el gasto pasa de 317? ¿la categoría en cero queda en cero?).

---

## 1. Lenguaje que siempre se puede usar

| Lo que calculaste | Frase correcta |
|---|---|
| Media posterior | El centro de la posterior. Es el estimador puntual. |
| Mediana posterior (columna 50%) | El valor que deja la mitad de la posterior a cada lado. Si está cerca de la media, la posterior es simétrica. |
| IC creíble 95% | El 95% de la posterior cae entre estos dos números. |
| IC de confianza 95% | Si repitiera el muestreo muchas veces, el 95% de esos intervalos atraparían el parámetro. No es una probabilidad sobre el parámetro. |
| P(θ > c \| datos) | Proporción de la posterior que queda por encima de c. |

Cuando el IC creíble y el de confianza salen iguales (parte 3, ejercicio 6): los números coinciden porque la prior es plana y manda la verosimilitud. La interpretación no coincide.

---

## 2. Beta–Binomial (parte 1, ejercicio 5)

Datos: n = 20, y = 4 clics. Tres priors, la misma actualización.

Posterior: Beta(α + 4, β + 16). Media: (α + 4) / (α + β + 20).

| Prior | α, β | Qué dices |
|---|---|---|
| Uniforme | 1, 1 | No favorecías ningún θ. |
| Jeffreys | 1/2, 1/2 | Poca información, distinta de la uniforme. |
| Beta(3, 10) | 3, 10 | La experiencia previa ya creía en pocos clics (media previa 3/13 ≈ 0.23). |

Interpretación de la sensibilidad: compara las tres medias. Si quedan cerca, con n = 20 la verosimilitud manda y la decisión no depende del prior. Si una se separa, esa prior todavía empuja y hay que justificarla. Aquí 4/20 = 0.20 y la prior Beta(3, 10) ya estaba cerca de 0.23, así que no se contradicen. Con la muestra pequeña del ejercicio 6 (1 defecto en 15) sí se separan: ahí la prior informativa pesa más.

---

## 3. Dirichlet (parte 1, ejercicios 7 y 9)

Posterior: Dirichlet(α + conteos). Media de la categoría j: (α_j + y_j) / (suma de α + n).

Ejercicio 7. Prior de unos y conteos 20, 12, 8. Cada media es un poco más suave que la proporción muestral, porque sumas 1 a cada conteo y 3 al total.

Ejercicio 9. Deficiente tiene 0 reseñas. El frecuentista dice 0%. La media Dirichlet no es 0: el prior reparte un poco de probabilidad a la categoría que no viste. Frase: con 15 reseñas no se puede concluir que sea imposible obtener Deficiente.

No confundas esto con la logística multinomial. Aquí no hay covariables. Las proporciones suman 1 y se actualizan sumando conteos.

---

## 4. Parte 3, lo que todavía interpreta el examen

Ejercicio 3. La posterior logística es verosimilitud binomial por prior normal. No tiene forma cerrada. Se simula con Metropolis–Hastings o HMC. Gibbs con condicionales cerradas no aplica.

Ejercicio 4. El intervalo viene en odds. Pásalo a probabilidad con p = odds / (1 + odds). El límite superior de la probabilidad base se compara con 0.40. Si ese límite pasa 0.40, la regla del banco rechaza el perfil.

Ejercicio 5. 9250 de 10000 muestras con β > 0. La probabilidad posterior de efecto positivo es 0.925. El umbral pedido es 0.95, así que no alcanza para implementar la campaña.

Ejercicio 6. Mismos números, distinta lectura: el de confianza habla de repetición del experimento. El creíble habla de la posterior. Coinciden porque la prior no informativa deja que mande la verosimilitud.

---

## 5. Regresión lineal en R (parte 4, ejercicio 2, gastos)

Respuesta: SE75, gasto por persona en dólares. No está en logaritmo. No uses (exp(β) − 1) × 100. Eso era de lungcap.

### Coeficiente

β_j es el cambio en el gasto esperado cuando esa covariable sube una unidad y las otras se quedan quietas.

- Positivo: a más urbanización, ingreso o proporción de menores, el gasto esperado sube.
- Negativo: baja.
- IC creíble que contiene 0: no hay evidencia clara de asociación.
- IC que no contiene 0: sí hay asociación, en el sentido del signo.

`summary` de `stan_glm`: mean = media posterior, 50% = mediana. Las columnas 10% y 90% son un intervalo del 80%. El 95% sale de `posterior_interval`.

### Predecir Nuevo México

`posterior_predict` simula el gasto de un estado nuevo con URB70 = 698, PI73 = 3764, Y74 = 366. Cada muestra incluye la incertidumbre de los coeficientes y el ruido de un estado que no estaba en la base. Por eso el intervalo es más ancho que un intervalo del gasto medio xβ.

- `mean(pred)`: gasto estimado para Nuevo México.
- `quantile(pred, c(0.025, 0.975))`: intervalo del 95% para ese gasto.
- `mean(pred <= 317)`: probabilidad de que el gasto de ese estado sea 317 o menos. Es una probabilidad predictiva. No es un p-valor.

Prior `NULL`: prior plana. Con eso el centro se parece a los mínimos cuadrados, y la lectura sigue siendo bayesiana.

---

## 6. Logística en R (parte 4, ejercicio 4)

Tres escalas. No las mezcles.

| Escala | Dónde está | Cómo se lee |
|---|---|---|
| Coeficiente β | `summary`, columna mean | Log-odds. El signo dice si la probabilidad sube o baja. |
| Odds ratio e^β | `exp(mean)` y `exp(posterior_interval)` | Por cuánto se multiplican las chances cuando la covariable sube 1 y el resto queda fijo. |
| Probabilidad π | `posterior_epred` | Un número entre 0 y 1 para un vendedor concreto. |

### Signo y magnitud (inciso g)

- β > 0: más de esa variable, mayor probabilidad de promoción.
- β < 0: menor probabilidad.
- No digas “la probabilidad sube 0.043”. Eso es log-odds. Di “las chances se multiplican por e^β”.

Con tus resultados:

- Intercepto −21.83: log-odds cuando ventas, satisfacción y desempeño valen 0. La probabilidad ahí es casi 0. Ese perfil no es un vendedor de la base.
- sales 0.0435, e^β ≈ 1.044: cada mil dólares más multiplica las chances por 1.044 (cerca de 4.4% más), con las otras dos fijas. La probabilidad sube.
- customer_rate −1.195, e^β ≈ 0.30: un punto más de satisfacción deja las chances en cerca del 30%. La probabilidad baja.
- performance 0.30, e^β ≈ 1.35: el centro es positivo, pero el intervalo incluye negativos. No afirmes el efecto.

### Asociación (inciso h)

Mira el IC 95% de β, no el de la probabilidad.

- sales (0.031, 0.059): no contiene 0. Asociación positiva.
- customer_rate (−2.23, −0.28): no contiene 0. Asociación negativa.
- performance (−0.36, 0.97): contiene 0. No hay evidencia clara.

### Odds ratio (inciso i)

- Mayor que 1: las chances suben.
- Menor que 1: bajan.
- El intervalo contiene 1: no hay asociación clara. Es el mismo mensaje que “el IC de β contiene 0”.
- `exp(posterior_interval)` es el intervalo del odds ratio. El puntual es e elevado a la media, no un extremo del intervalo.

### Probabilidad de un vendedor (incisos j y k)

`fitted` es para filas que ya están en la base. Para sales = 150, customer_rate = 4.2, performance = 3 usa `posterior_epred`.

- `mean(p)`: probabilidad media de promoción de ese vendedor.
- `quantile(p, c(0.025, 0.975))`: IC 95% de esa probabilidad.

150 está en el mínimo de ventas de la base (mínimo 151, mediana 475) y ventas tiene efecto positivo claro. La probabilidad de ese perfil queda prácticamente en 0.

### Convergencia, antes de interpretar

Solo interpretas si las cuatro se cumplen: trazas juntas y horizontales, Rhat menor que 1.01, n_eff de miles, Heidelberger en passed desde la iteración 1. En tu ajuste se cumplieron. `mean_PPD` ≈ 0.32 no es un coeficiente: es la tasa de promoción que el modelo reproduce, cerca del 32% de la base.

---

## 7. Frases listas para copiar

Regresión lineal. “Un aumento de una unidad en X, con el resto fijo, cambia el gasto esperado en β. El intervalo creíble no incluye 0, así que hay evidencia de asociación.”

Predicción. “Para Nuevo México el gasto predicho es la media de las simulaciones. La probabilidad de que sea 317 o menos es la proporción de esas simulaciones que caen en 317 o por debajo.”

Logística. “El coeficiente está en log-odds. El signo indica la dirección de la probabilidad. Cada unidad de X multiplica las chances por e^β.”

Asociación. “Hay evidencia si el intervalo del 95% del coeficiente no contiene 0. En chances, eso es un odds ratio cuyo intervalo no contiene 1.”
