# Parcial 2 — Mapa completo (profesor → principiante)

**Regla de oro bayesiana (una frase):**  
*Actualizo creencias sobre parámetros con datos: posterior ∝ verosimilitud × prior.*

**Ejemplo mínimo (binomial):** 4 clics de 20 usuarios. Prior uniforme → posterior Beta(5, 17). Media posterior = 5/22 ≈ 0.23 (“creo ~23 % de clics”, no un solo número fijo).

---

## Parte 1 — Ficha por tema

Cada bloque: **tema → cuándo → idea clave → fórmulas obligatorias → tener presente → ejemplo concreto**

---

### 0. Marco bayesiano (base de todo)

| | |
|---|---|
| **Tema** | Inferencia bayesiana |
| **Cuándo** | Siempre que quieras **incertidumbre sobre parámetros** (no solo “un estimador”) |
| **Idea clave** | El parámetro es **aleatorio**; después de ver datos, describes **distribución posterior**. |
| **Fórmulas** | \(p(\theta\mid y)=\dfrac{p(y\mid\theta)\,p(\theta)}{p(y)}\); **núcleo:** \(p(\theta\mid y)\propto p(y\mid\theta)\,p(\theta)\) |
| **Tener presente** | **Prior** = lo que creías antes; **verosimilitud** = qué datos favorece cada \(\theta\); **evidencia** \(p(y)\) a veces no la calculas (solo proporcionalidad). **IC creíble** = “con 95 % de probabilidad posterior, \(\theta\) está aquí” (no es “95 % de veces en repetición”). |

**Ejemplo:** Moneda. Prior: “no sé” = Beta(1,1). 7 caras en 10 lanzamientos → posterior Beta(8,4). P(cara|datos) ≈ 8/12 = 2/3, pero aún hay incertidumbre (intervalo creíble no es un punto).

---

### 1. Normal–Normal (media \(\mu\), varianza \(\sigma^2\) **conocida**) — S13

| | |
|---|---|
| **Tema** | Prior Normal en \(\mu\) + datos Normal i.i.d. |
| **Cuándo** | Mediciones con error conocido; actualizar media con \(n\) observaciones |
| **Idea clave** | **Precisión posterior = prior + datos** (sumas de precisiones). |
| **Fórmulas** | \(\tau_n^{-2}=\tau_0^{-2}+n\sigma^{-2}\); \(\mu_n=\dfrac{\tau_0^{-2}\mu_0+n\sigma^{-2}\bar y}{\tau_n^{-2}}\); posterior \(\mu\mid y\sim N(\mu_n,\tau_n^2)\). **Predictiva** \(y^*\mid y\sim N(\mu_n,\sigma^2+\tau_n^2)\) (suma de incertidumbres). |
| **Tener presente** | \(\mu_n\) = promedio ponderado entre \(\mu_0\) y \(\bar y\). Predictiva **más ancha** que IC de \(\mu\) (también no sabes el error del **nuevo** dato igual que si \(\mu\) fuera fijo). |

**Ejemplo (parte1 #2):** Termómetro marca 98 °C; prior media 100, \(\sigma^2_{\text{datos}}=8\). La posterior de \(\mu\) se acerca a 98 pero no igual; la **siguiente medición** tiene varianza predictiva = incertidumbre de \(\mu\) **+** 8 (ruido del instrumento).

---

### 2. Normal con media y varianza **desconocidas** (Normal–InvGamma / NIG) — S14

| | |
|---|---|
| **Tema** | \(\mu\) y \(\sigma^2\) juntos; prior conjugado |
| **Cuándo** | Datos normales sin saber ni media ni dispersión |
| **Idea clave** | Actualizas **media** y **dispersión** a la vez; la marginal de \(\mu\) ya no es Normal pura. |
| **Fórmulas** | Prior típico NIG: \(\mu\mid\sigma^2\sim N(\mu_0,\sigma^2/\kappa_0)\), \(\sigma^2\sim\text{Inv-Gamma}(\nu_0/2,\nu_0\sigma_0^2/2)\). Posterior mismo tipo con \(\kappa_n,\mu_n,\nu_n,\nu_n\sigma_n^2\). **Marginal** \(\mu\mid y \sim t_{\nu_n}\) (colas más gruesas que Normal). |
| **Tener presente** | \(\nu_n=\nu_0+n\). Con pocos datos, **no ignores** incertidumbre en \(\sigma^2\). |

**Ejemplo:** 6 carreras, \(\bar y=220\), \(s^2=20\). Si trataras \(\sigma^2\) como fija, subestimarías incertidumbre en \(\mu\). Con NIG, \(\mu\mid y\) es **t**: colas más gruesas → intervalos más honestos con \(n\) pequeño.

---

### 3. Priors: informativos, débiles, Jeffreys, sensibilidad — S15

| | |
|---|---|
| **Tema** | Elección del prior |
| **Cuándo** | Pocos datos, parámetro en \((0,1)\), o quieres “poca información” sin mentir |
| **Idea clave** | El prior **pesa** como “datos ficticios”; con **poco \(n\)** manda más. |
| **Fórmulas** | Binomial: posterior \(\text{Beta}(\alpha+y,\beta+n-y)\). **Uniforme** \(U(0,1)\) = Beta\((1,1)\). **Jeffreys** binomial = Beta\((\tfrac12,\tfrac12)\). Jeffreys ≈ “invariante a reparametrización” (idea, no memorizar integral). |
| **Tener presente** | Prior **plano** no siempre es “mejor”. Compara posteriores con 2 priors razonables = **análisis de sensibilidad**. Jeffreys puede ser **impropia** en otros modelos. |

**Ejemplo (parte1 #5):** 4/20 clics. Uniforme → media 5/24 ≈ 0.21. Jeffreys Beta(½,½) → media 4.5/20.5 ≈ 0.22. Informativa Beta(3,10) → tira hacia ~0.23 histórico. Con \(n=20\) casi igual; con **1/15 defectos** (#6) las tres priors **sí** separan.

---

### 4. Multinomial–Dirichlet — S16–S17

| | |
|---|---|
| **Tema** | Proporciones en categorías (\(\sum_j\theta_j=1\)) |
| **Cuándo** | Conteos por categoría, encuestas, proporciones en simplex |
| **Idea clave** | Dirichlet = “Beta multivariada”; posterior **misma familia** sumando conteos al hiperparámetro. |
| **Fórmulas** | \(y\sim\text{Multinomial}(n,\theta)\), \(\theta\sim\text{Dir}(\alpha)\) → \(\theta\mid y\sim\text{Dir}(\alpha+y)\). \(E[\theta_j\mid y]=(\alpha_j+y_j)/(\sum_k\alpha_k+n)\). **Suavizado:** categorías con 0 en datos aún tienen masa si \(\alpha_j>0\). |
| **Tener presente** | \(\alpha\) grande = prior fuerte hacia \(\alpha/\sum\alpha\). No confundir con **multinomial logística** (covariables); aquí \(\theta\) es fijo por grupo. |

**Ejemplo (#9):** Excelente 10, Aceptable 5, Deficiente **0** en 15 reseñas. Frecuente: Deficiente = 0 %. Bayes Dir(1,1,1)+datos → Deficiente esperado > 0 (prior reparte masa). Evita decir “imposible” con muestra chica.

---

### 5. Normal multivariada: prior en \(\mu\), \(\Sigma\) conocida — S19

| | |
|---|---|
| **Tema** | Vector medio \(\mu\) con datos MVN |
| **Cuándo** | Varias variables medidas juntas, covarianza del muestreo conocida |
| **Idea clave** | Misma lógica que Normal–Normal, pero con **matrices de precisión**. |
| **Fórmulas** | \(\Lambda_n^{-1}=\Lambda_0^{-1}+n\Sigma^{-1}\); \(\mu_n=\Lambda_n(\Lambda_0^{-1}\mu_0+n\Sigma^{-1}\bar y)\). Predictiva: \(\mathrm{Var}(y^*)=\Sigma+\Lambda_n\). |
| **Tener presente** | Prior muy difuso → \(\mu_n\approx\bar y\). Condicional MVN (bloques) es base de **Gibbs** en modelos normales. |

**Ejemplo (parte2 #5):** Entrega 34 min → la **calificación** esperada no es la media marginal 4.5; usas \(X_2\mid X_1=34\) (correlación negativa: más tarde, peor nota típica).

---

### 6. \(\Sigma\) desconocida: Normal–Inverse-Wishart — S20 (idea)

| | |
|---|---|
| **Tema** | Media y matriz de covarianza juntas |
| **Cuándo** | Datos multivariados sin \(\Sigma\) fija |
| **Idea clave** | Extensión de NIG a \(p\) dimensiones; más parámetros, más incertidumbre. |
| **Fórmulas** | Prior NIW conjugado (actualización de \(\kappa,\mu,\nu,\Psi\) — mismo **espíritu** que S14). |
| **Tener presente** | En parcial suele bastar **reconocer** el caso y que marginal de \(\mu\) tiene colas pesadas; detalle de Wishart si el profe lo exige en guía. |

**Ejemplo:** Dos indicadores de agua, \(n=10\). No fijas \(\Sigma\); aprendes correlación **y** medias → más incertidumbre que asumir \(\Sigma\) conocida (parte2 #6 es el caso \(\Sigma\) fija + prior en \(\mu\)).

---

### 7. Regresión lineal bayesiana (concepto + ejercicios)

| | |
|---|---|
| **Tema** | \(y = X\beta + \varepsilon\), priors en \(\beta,\sigma^2\) |
| **Cuándo** | Predecir \(y\) con covariables; cuantificar incertidumbre en coeficientes |
| **Idea clave** | Coeficientes son **parámetros** con prior; posterior mezcla datos y creencia previa. |
| **Fórmulas** | Verosimilitud: \(y\mid\beta,\sigma^2\sim N(X\beta,\sigma^2 I)\). Con prior Normal conjugado en \(\beta\) (y Inv-Gamma en \(\sigma^2\)) → posterior analítica o Gibbs. **Predictiva:** simular \(\beta,\sigma^2\) de la posterior y luego \(y^{\text{new}}\). |
| **Tener presente** | Prior difuso en \(\beta\) ≈ OLS con incertidumbre bayesiana. Multicolinealidad = posteriors correlacionadas, intervalos anchos. |

**Ejemplo (parte3 #1):** Fumar y capacidad pulmonar: IC creíble de \(\beta_{\text{smoke}}\) = \([-0.087,-0.003]\) → casi todo negativo → \(P(\beta<0\mid y)\) alta → evidencia de efecto, no solo “media = −0.046”.

---

### 8. Regresión logística **binaria**

| | |
|---|---|
| **Tema** | \(Y\in\{0,1\}\), probabilidad \(\pi(x)\) |
| **Cuándo** | Éxito/fracaso, sí/no, con covariables |
| **Idea clave** | Modelas **log-odds** como función lineal de \(x\); **no hay** posterior conjugada cerrada típica. |
| **Fórmulas** | \(\text{logit}(\pi)=\log\frac{\pi}{1-\pi}=\beta_0+x^T\beta\); \(\pi=\dfrac{1}{1+e^{-(\beta_0+x^T\beta)}}\). Log-verosimilitud: \(\sum_i[y_i(\beta_0+x_i^T\beta)-\log(1+e^{\beta_0+x_i^T\beta})]\). |
| **Tener presente** | OR = \(e^{\beta_j}\). Separación perfecta → problemas frecuentistas; prior regulariza en Bayes. **Gibbs “puro”** no estándar → **MH/HMC**. |

**Ejemplo (parte3 #2):** \(\beta_0=-4\), \(\beta_1=0.1\), humedad 60 % → log-odds = −4+6 = 2 → \(\pi=1/(1+e^{-2})\approx 0.88\). OR por 1 % humedad: \(e^{0.1}\approx 1.11\) (11 % más odds). Umbral 15 % lluvia → hoy **no** cancelarías solo con 15 %.

---

### 9. Lasso / Ridge bayesiano — S27

| | |
|---|---|
| **Tema** | Muchas variables; shrinkage |
| **Cuándo** | \(p\) grande, sobreajuste, variables ruidosas |
| **Idea clave** | Penalización frecuentista = **prior** que empuja coeficientes a 0. |
| **Fórmulas** | Ridge: \(\lambda\sum\beta_j^2\) ↔ \(\beta_j\sim N(0,\tau^2)\). Lasso: \(\lambda\sum|\beta_j|\) ↔ Laplace: \(p(\beta_j)=\frac{\lambda}{2}e^{-\lambda|\beta_j|}\). Log-posterior (idea): residuos al cuadrado \(-\lambda\sum|\beta_j|\) + priors. |
| **Tener presente** | Lasso bayesiano **no** deja ceros exactos en muestras; “selección” con IC o \(P(|\beta_j|>\delta\mid y)\). Comparar **RMSE predictivo**, no solo \(R^2\). |

**Ejemplo:** 50 variables, 40 ruido. OLS infla coeficientes; Ridge/Lasso los encoge. Bayes Lasso: muestras de \(\beta_j\) cerca de 0, pero raramente **exactamente** 0 → “¿relevante?” = IC no cubre 0 o \(P(|\beta_j|>0.01\mid y)\) alta.

---

### 10. Logística **multinomial** (Agresti) — HTML

| | |
|---|---|
| **Tema** | \(J>2\) categorías **sin orden** |
| **Cuándo** | Tipo de comida, marca, diagnóstico nominal |
| **Idea clave** | Comparas cada categoría con una **referencia** vía log-odds. |
| **Fórmulas** | \(\log\frac{\pi_j(x)}{\pi_J(x)}=\beta_{j0}+x^T\beta_j\). Softmax para \(\pi_j(x)\). OR = \(e^{\beta}\) vs referencia \(J\). |
| **Tener presente** | Una fila de datos = **una** multinomial (no \(J\) binomiales independientes). Bayes → MCMC (`brms`, etc.). |

**Ejemplo (cocodrilo):** Referencia = Fish. Si \(\beta_{\text{Reptile}}=0.5\) → odds Reptile vs Fish multiplican por \(e^{0.5}\). Las tres probabilidades \(\pi_j(x)\) **suman 1** (softmax).

---

### 11. Gibbs sampling — Tutorial

| | |
|---|---|
| **Tema** | MCMC cuando hay **condicionales completas** simulables |
| **Cuándo** | NIG, jerárquicos conjugados, bloques normales |
| **Idea clave** | Rota: “fijo todo menos un parámetro y muestreo su distribución condicional”. |
| **Fórmulas** | \(\theta_j^{(t)}\sim p(\theta_j\mid\boldsymbol\theta_{-j}^{(t-1)},y)\). |
| **Tener presente** | 100 % aceptación **no** implica buena mezcla. Logística estándar → condicionales incómodas. |

**Ejemplo (tutorial peajes):** Alternar \(\mu\mid\sigma^2,y\) (Normal) y \(\sigma^2\mid\mu,y\) (Inv-Gamma). Cada paso es “legal”; si \(\mu\) y \(\sigma^2\) están correlacionados en la posterior, la cadena puede moverse lento (mucho ACF).

---

### 12. Diagnósticos MCMC — Tutorial

| | |
|---|---|
| **Tema** | ¿La cadena representa la posterior? |
| **Cuándo** | Siempre que uses MCMC |
| **Idea clave** | Muestras **correlacionadas**; hay que **quemar**, **mezclar** y **replicar** cadenas. |
| **Fórmulas** | (No una fórmula única) ESS, \(\hat R\approx 1\), MCSE pequeño. |
| **Tener presente** | Burn-in, traza, ACF. Si hay solución analítica (Beta), compara mediana/IC. |

**Ejemplo:** Beta(5,17) exacta vs media de cadena Gibbs mal mezclada: medias distintas → revisar burn-in, ESS, \(\hat R\). En `stan_glm`: \(\hat R>1.01\) o ESS bajo → **no** reportar IC todavía.

---

### 13. Aceptación–rechazo e importance sampling — S34

| | |
|---|---|
| **Tema** | Simular de \(f\) sin MCMC |
| **Cuándo** | Baja dimensión, envolvente conocida (AR); expectativas con otra densidad \(g\) (IS) |
| **Idea clave** | AR: rechazas hasta acertar; IS: **reponderas** muestras de \(g\). |
| **Fórmulas** | AR: aceptar si \(U\le f(x^*)/(Mq(x^*))\). IS: \(\hat E[h]\approx\sum w_i h(x_i)/\sum w_i\), \(w_i=f(x_i)/g(x_i)\). |
| **Tener presente** | AR escala mal en alta dimensión. IS: varianza de pesos puede explotar. |

**Ejemplo AR:** Quieres simular de una campana rara; propones Normal fácil \(q\), acotas \(f\le Mq\), lanzas muchos rechazos. **IS:** muestreas de \(g\) “fácil”, pesos \(w=f/g\); si un peso es enorme, la media estimada es inestable.

---

### 14. Metropolis–Hastings — S34

| | |
|---|---|
| **Tema** | MCMC general con propuestas |
| **Cuándo** | Posterior conocida solo hasta constante (logística, Lasso, etc.) |
| **Idea clave** | Camina al azar, a veces **acepta** saltos a zonas de mayor posterior. |
| **Fórmulas** | \(\alpha=\min\left(1,\dfrac{p(\theta^*\mid y)\,q(\theta\mid\theta^*)}{p(\theta\mid y)\,q(\theta^*\mid\theta)}\right)\). Metropolis simétrico: \(\alpha=\min(1,p(\theta^*\mid y)/p(\theta\mid y))\). |
| **Tener presente** | Tasa aceptación ~20–50 % a menudo OK en random walk. Propuesta pequeña → alta aceptación, **lento**. |

**Ejemplo:** Log-posterior Lasso: pruebas \(\beta_j'=\beta_j+0.1\); si sube log-posterior, aceptas con probabilidad \(\alpha\). Pasos minúsculos → 90 % aceptación pero 10 000 iteraciones para recorrer el espacio.

---

### 15. HMC (Hamiltonian Monte Carlo) — S34

| | |
|---|---|
| **Tema** | MCMC con **gradiente** de log-posterior |
| **Cuándo** | Muchos parámetros, Gibbs lento, modelos tipo regresión |
| **Idea clave** | “Física” en el espacio de parámetros: trayectorias largas + corrección MH. |
| **Fórmulas** | (Parcial: **idea**, no derivar ecuaciones de Hamilton) Necesitas \(\nabla\log p(\theta\mid y)\). |
| **Tener presente** | Divergencias = mala geometría / paso mal calibrado. Stan/brms usan HMC/NUTS. |

**Ejemplo:** Logística con 20 \(\beta\). Random walk MH se arrastra; HMC usa el gradiente de la log-verosimilitud para dar saltos coherentes → menos autocorrelación (mismo número de iteraciones, mejor ESS).

---

## Parte 2 — Un solo hilo: cómo se articula todo

Imagina **cuatro pisos** de un edificio. Subes cuando el piso de abajo ya no alcanza.

```
PISO 4 — COMPUTAR          Gibbs → MH → HMC + diagnósticos
PISO 3 — MODELOS RICOS     Logística, multinomial, Lasso (sin conjugada)
PISO 2 — CONJUGADOS        Normal-Normal, NIG, Dirichlet, (regresión conjugada)
PISO 1 — BAYES             posterior ∝ verosimilitud × prior
```

**Historia en 30 segundos:**  
Empiezas diciendo “quiero la distribución de \(\theta\) después de los datos”. Si prior y verosimilitud son **pareja conjugada**, la posterior es **fórmula cerrada** (Beta, Normal, Dirichlet, NIG…). Si el modelo crece (varias \(\theta\), matrices, categorías con \(x\)), la posterior **no** es de una familia conocida → **simulas** una cadena. Si puedes simular cada **condicional**, Gibbs. Si no, MH. Si hay muchos parámetros y gradiente, HMC. **Nunca** te fías de la cadena sin **diagnósticos**.

**Analogía concreta:** Conjugado = receta cerrada (Beta después de binomial). Logística Bayes = no hay receta → **degustación por muestreo** (MCMC); diagnósticos = comprobar que la degustación representó todo el plato.

---

## Parte 3 — Una palabra / frase gancho por tema (memotecnia)

Úsalas como **anclas** al explicar en voz alta:

| # | Tema | Gancho (di en voz alta) |
|---|------|-------------------------|
| 0 | Marco bayesiano | **“Multiplico y normalizo”** — prior × verosimilitud |
| 1 | Normal–Normal | **“Sumo precisiones”** |
| 2 | NIG / σ² unknown | **“Dos incógnitas, colas de t”** |
| 3 | Priors / Jeffreys | **“¿Cuántos datos ficticios pongo?”** |
| 4 | Dirichlet | **“Alpha más conteos”** |
| 5 | MVN \(\mu\) | **“Precisión en matriz”** |
| 6 | NIW | **“NIG en varias dimensiones”** |
| 7 | Regresión lineal Bayes | **“Betas con prior; predigo con ruido”** |
| 8 | Logística binaria | **“Log-odds lineal; sin conjugada”** |
| 9 | Lasso/Ridge | **“L2 es campana; L1 es Laplace”** |
| 10 | Multinomial logit | **“Todo contra la categoría J”** |
| 11 | Gibbs | **“Uno a la vez, condicional completa”** |
| 12 | Diagnósticos | **“¿Parece humo o posterior?”** |
| 13 | AR / IS | **“Rechazo o repondero”** |
| 14 | MH | **“Propongo; acepto si sube la posterior”** |
| 15 | HMC | **“Gradiente me empuja lejos”** |

**Frase que une conjugados vs MCMC:**  
**“¿Cerrado? Calculo. ¿No cerrado? Cadena.”**

**Frase que une predictivo vs parámetro:**  
**“El parámetro es incierto; el dato nuevo lleva su propio ruido.”**

**Frase que une frecuente vs Bayes en regresión:**  
**“Ellos maximizan; yo distribuyo.”**

---

## Parte 4 — Articulación en cadena (para oral o escrito)

Puedes practicar este monólogo (sustituye detalles si el profe acota temas):

1. **Bayes:** Actualizo con \(p(\theta\mid y)\propto p(y\mid\theta)p(\theta)\).  
2. **Normal–Normal:** Si \(\sigma^2\) es fija, \(\mu\) queda Normal; la predictiva suma varianzas.  
3. **NIG:** Si también \(\sigma^2\) es incierta, conjugo y \(\mu\) marginal es **t**.  
4. **Priors:** Con poco \(n\), el prior importa; Jeffreys en binomial es Beta(½,½).  
5. **Dirichlet:** Proporciones; posterior Dir(\(\alpha+y\)).  
6. **MVN/NIW:** Misma idea en vector y matriz de covarianza.  
7. **Regresión:** Pongo prior en \(\beta\); lineal puede ser conjugada; **logística** ya no.  
8. **Lasso:** Laplace encoge coeficientes; MCMC en log-posterior.  
9. **Multinomial logit:** Varias categorías vs referencia; softmax; Bayes con MCMC.  
10. **Gibbs** si hay condicionales; si no, **MH**; si hay muchos \(\beta\) y gradiente, **HMC**.  
11. **Diagnósticos:** burn-in, \(\hat R\), ESS — sin eso no hay inferencia.

---

## Parte 5 — Mini tabla “¿Qué método uso?”

| Situación | Herramienta |
|-----------|-------------|
| Beta–Binomial, Normal–Normal, Dirichlet–Multinomial | **Fórmula posterior** |
| \(\mu,\sigma^2\) normal conjugado | **Gibbs** (o analítico) |
| Logística, Lasso, multinomial Bayes | **MH o HMC** |
| Expectativa baja dim con envolvente | **Aceptación–rechazo** |
| Cualquier MCMC | **Diagnósticos** |

---

## Parte 6 — Enlace con ejercicios (PDF)

| Concepto | Dónde practicarlo |
|----------|-------------------|
| Normal–Normal, predictiva | Parte1 **1–2** |
| NIG | Parte1 **3–4** |
| Jeffreys, sensibilidad | Parte1 **5–6** |
| Dirichlet | Parte1 **7–10** |
| MVN condicional / Bayes \(\mu\) | Parte2 **5–6** |
| Regresión / logística interpretación | Parte3 **1–7** |
| R: lineal, logística, MCMC | Parte4 **1–5** (+ `Scripts_y_bases/scripts/GUIA_R_DEFINITIVA.md`) |

---

*Documento de repaso Parcial 2 — Estadística Bayesiana (Externado). Complemento: guías HTML en `Teoria/` (Gibbs, S27 Lasso, S34 MH/HMC, multinomial Agresti).*
