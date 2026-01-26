# Explicación Paso a Paso de `03_sentimiento_por_lexicon.py`

Este documento detalla el funcionamiento del script `03_sentimiento_por_lexicon.py`, cuyo objetivo es construir un clasificador de sentimientos básico utilizando diccionarios de palabras (léxicos).

## 1. Librerías Utilizadas y Su Propósito

### `re` (Expresiones Regulares)

- **Uso**: Para la limpieza del texto. Nos permite extraer palabras individuales ignorando puntuación con el patrón `\b\w+\b`.

### `matplotlib.pyplot`

- **Uso**: Para generar gráficos. En este caso, se utiliza específicamente para crear un **gráfico de tarta (pie chart)** que muestra la proporción de comentarios positivos, negativos y neutros.

### `collections.Counter`

- **Uso**: Para contar rápidamente cuántas frases resultaron ser "Positivas", "Negativas" o "Neutras" al final del análisis.

## 2. Los Datos: Corpus, Stopwords y Léxicos

### El Corpus

Es nuestra lista de frases a analizar, simulando opiniones de clientes.

```python
corpus = [
    "Me encanta este producto...",
    "El servicio al cliente fue terrible...",
    ...
]
```

### Stopwords (Palabras Vacías)

Palabras muy comunes (como "de", "la", "el", "y") que generalmente no aportan significado emocional. Las eliminamos para reducir "ruido" en el análisis.

### Léxicos de Sentimiento

Son la "inteligencia" de nuestro clasificador. Definimos dos conjuntos de palabras manualmente:

- **`lexico_positivo`**: Palabras que suman puntos (ej. "encanta", "fantástico", "útil").
- **`lexico_negativo`**: Palabras que restan puntos (ej. "terrible", "decepcionante", "malo").

## 3. Lógica de Procesamiento de Sentimientos

La función principal es `analizar_sentimiento(...)`. Su funcionamiento es el siguiente:

### Paso 1: Limpieza

Se convierte la frase a minúsculas y se separan las palabras. Se filtran aquellas que están en la lista de _stopwords_.

### Paso 2: Puntuación (Scoring)

El algoritmo recorre las palabras limpias y:

- Suma **+1** por cada palabra encontrada en el `lexico_positivo`.
- Suma **+1** (que luego restaremos) por cada palabra encontrada en el `lexico_negativo`.

### Paso 3: Cálculo Final

```python
puntaje_final = score_pos - score_neg
```

- Si `puntaje_final > 0` → **Positiva**
- Si `puntaje_final < 0` → **Negativa**
- Si `puntaje_final == 0` → **Neutra**

### Ejemplos Prácticos de Cálculo

Para entenderlo mejor, veamos dos casos concretos (imaginemos que las _stopwords_ ya han sido eliminadas):

**Caso 1: Una opinión mixta**

> Frase: "El producto es **fantástico** pero el envío fue **terrible**."

1.  **Léxico Positivo (+)**: Encontramos "fantástico" (+1).
2.  **Léxico Negativo (-)**: Encontramos "terrible" (+1).
3.  **Cálculo**:
    - `score_pos = 1`
    - `score_neg = 1`
    - `puntaje_final = 1 - 1 = 0`
4.  **Resultado**: **Neutra**.

**Caso 2: Una opinión muy buena**

> Frase: "Me **encanta**, es **increíble** y **útil**."

1.  **Léxico Positivo (+)**: Encontramos "encanta", "increíble", "útil" (3 palabras).
2.  **Léxico Negativo (-)**: No encontramos ninguna (0 palabras).
3.  **Cálculo**:
    - `score_pos = 3`
    - `score_neg = 0`
    - `puntaje_final = 3 - 0 = +3`
4.  **Resultado**: **Positiva**.

## 4. Visualización de Resultados

El código finaliza generando un gráfico de tarta para resumir los resultados del corpus.

- **Datos**: Se obtienen con `Counter` sobre la lista de clasificaciones.
- **Gráfico**: Se usa `plt.pie(...)` asignando colores específicos (verde para positivo, rojo para negativo, beige para neutro) para facilitar la interpretación visual rápida.

## Conclusión y Limitaciones

Este script demuestra un enfoque **basado en reglas**. Es transparente y fácil de entender, pero tiene una limitación importante mostrada en el ejemplo _"No está mal"_:

- El script detecta "mal" (negativo) y clasifica la frase como negativa.
- Falla al no entender que el "No" anterior invierte el significado (negación).
  Esto resalta la necesidad de modelos de NLP más avanzados para entender contexto y gramática.
