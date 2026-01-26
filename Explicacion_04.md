# Explicación Paso a Paso de `04_similitud_jaccard.py`

Este documento explica el script `04_similitud_jaccard.py`, diseñado para enseñar cómo medir la similitud matemática entre diferentes textos y visualizar esas relaciones.

## 1. Librerías Utilizadas

- **`numpy`**: Fundamental para operaciones matemáticas eficientes y manejo de matrices (arrays multidimensionales).
- **`seaborn`**: Librería de visualización basada en Matplotlib que facilita la creación de **mapas de calor (heatmaps)** estéticos y complejos.
- **`matplotlib.pyplot`**: Base para la creación de figuras y subgráficos.
- **`re`**: Para preprocesamiento y limpieza de texto.

## 2. El Corpus Temático

A diferencia del ejercicio anterior, aquí el corpus está estructurado intencionalmente en **3 categorías claras** para validar si el algoritmo funciona:

1.  **Fútbol**: Frases sobre goles, árbitros y partidos (Índices 0-2).
2.  **Tecnología**: Frases sobre procesadores, RAM y discos duros (Índices 3-5).
3.  **Cocina**: Frases sobre pasta, recetas e ingredientes (Índices 6-8).

El objetivo es ver si el algoritmo logra "agrupar" estos temas automáticamente basándose solo en las palabras que usan.

## 3. Concepto Matemático: Similitud de Jaccard

El corazón conceptual de este script es la fórmula de Jaccard. Para dos textos (convertidos en conjuntos de palabras únicas A y B):

$$ J(A, B) = \frac{|A \cap B|}{|A \cup B|} = \frac{\text{Palabras en común}}{\text{Total de palabras únicas combinadas}} $$

- **1.0**: Textos idénticos (mismas palabras).
- **0.0**: Textos totalmente diferentes (ninguna palabra en común).

### Ejemplo Numérico Paso a Paso

Imaginemos que comparamos dos frases muy cortas:

- **Frase A**: "Me gusta Python"
- **Frase B**: "Me gusta programar"

**Paso 1: Convertir a Conjuntos (Sets)**

- Set A = `{"me", "gusta", "python"}` (3 palabras)
- Set B = `{"me", "gusta", "programar"}` (3 palabras)

**Paso 2: Calcular Intersección (Comunes)**

- Palabras en ambos: `{"me", "gusta"}`
- Tamaño Intersección: **2**

**Paso 3: Calcular Unión (Totales Únicas)**

- Todas las palabras juntas: `{"me", "gusta", "python", "programar"}`
- Tamaño Unión: **4**

**Paso 4: Fórmula Jaccard**
$$ J = \frac{2}{4} = 0.5 $$

Resultado: Tienen una similitud del **50%**.

## 4. Procesamiento

### Preprocesamiento `preprocess_to_set`

Cada frase se convierte en un **set** (conjunto matemático) de Python. Esto es crucial porque:

- Elimina duplicados automáticamente.
- Permite operaciones de conjuntos rápidas como intersección (`&`) y unión (`|`).

### Matriz de Similitud

Se crea una matriz cuadrada de tamaño `NxN` (donde N es el número de frases). Un doble bucle `for` compara **cada frase contra todas las demás**, calculando su índice de Jaccard y llenando la matriz.

## 5. Visualización de Datos

El script genera una visualización compleja con 4 paneles:

1.  **Mapa de Calor Triangular**: Muestra la matriz de similitud. Usamos una máscara triangular porque la matriz es simétrica (A vs B es igual a B vs A), lo que limpia visualmente el gráfico.
    - **Qué buscar**: Bloques de colores cálidos (rojos) a lo largo de la diagonal, indicando que las frases del mismo tema se parecen mucho entre sí.

2.  **Barras (Intra vs Inter)**: Compara numéricamente cuánto se parecen los textos de una misma categoría entre sí vs cuánto se parecen a textos de otras categorías. Valida que la cohesión temática es alta.

3.  **Histograma**: Muestra la distribución de los valores de similitud. Permite ver si nuestro algoritmo distingue bien (picos separados) o si todo se parece un poco (distribución plana).

4.  **Análisis de Pares**: Lista textualmente cuáles son las frases más parecidas, permitiendo inspeccionar qué palabras clave (ej. "fútbol", "pasta") están detonando la similitud.

## Conclusión

Este ejercicio demuestra cómo las matemáticas simples de conjuntos pueden usarse para **detectar tópicos** y agrupamientos en texto no estructurado, una base fundamental para motores de búsqueda y sistemas de recomendación.
