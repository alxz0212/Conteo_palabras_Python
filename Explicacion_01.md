# Explicación Paso a Paso de `01_conteo_palabras.py`

Este documento detalla el funcionamiento del script `01_conteo_palabras.py`, cuyo objetivo es introducir los conceptos básicos de Procesamiento de Lenguaje Natural (NLP).

## 1. Librerías Utilizadas y Su Propósito

Para que este código funcione, nos apoyamos en tres librerías poderosas de Python. Aquí te explicamos qué son y por qué las necesitamos:

### `re` (Expresiones Regulares)
- **¿Qué es?**: Es la librería estándar de Python para trabajar con patrones de búsqueda avanzada en texto.
- **¿Para qué la usamos aquí?**: La utilizamos en la línea `words = re.findall(...)`. Su función es **limpiar y dividir** el texto de forma inteligente. En lugar de simplemente cortar por espacios (que dejaría comas y puntos pegados a las palabras), `re` nos permite extraer solo las palabras (caracteres alfanuméricos), ignorando cualquier signo de puntuación.

### `collections.Counter`
- **¿Qué es?**: Una herramienta especializada integrada en Python diseñada exclusivamente para contar cosas.
- **¿Para qué la usamos aquí?**: Para realizar el **conteo matemático**. En lugar de crear bucles complejos para sumar apariciones palabra por palabra, `Counter` toma nuestra lista de palabras y automáticamente calcula cuántas veces aparece cada una, devolviéndonos un diccionario ordenado por frecuencia.

### `matplotlib.pyplot`
- **¿Qué es?**: La biblioteca "estándar de oro" en Python para crear visualizaciones estáticas, animadas e interactivas.
- **¿Para qué la usamos aquí?**: Para la **visualización de datos**. Nos permite tomar los números crudos del conteo y transformarlos en un gráfico de barras visualmente comprensible, lo cual es esencial para comunicar los hallazgos del análisis de texto.

## 2. El Corpus (Datos) (Líneas 19-30)
El "corpus" es simplemente nuestra base de datos de texto. En este caso, es una lista de frases simulando opiniones de clientes sobre un producto.
```python
corpus = [
    "Me encanta este producto...",
    "El servicio al cliente fue terrible...",
    ...
]
```

## 3. Procesamiento (Líneas 32-56)

### Paso 1: Unificación
Se unen todas las frases de la lista en una sola cadena de texto gigante usando `' '.join(corpus)`. Esto permite analizar todo el conjunto a la vez.

### Paso 2: Normalización
`all_text.lower()` convierte todo el texto a minúsculas.
- **¿Por qué?** Para que la computadora entienda que "Fantástico" y "fantástico" son la misma palabra.

### Paso 3: Tokenización
```python
words = re.findall(r'\b\w+\b', all_text_lower)
```
Aquí se divide el texto en palabras individuales (tokens).
- **Explicación del regex `\b\w+\b`**:
  - `\b`: Límite de palabra (comienzo o final).
  - `\w+`: Uno o más caracteres alfanuméricos (letras o números).
  - Esto asegura que signos de puntuación como `.` o `,` sean ignorados.

### Paso 4: Conteo
```python
word_counts = Counter(words)
```
`Counter` recorre la lista de palabras y crea un diccionario donde las claves son las palabras y los valores son cuántas veces aparecen.

### Paso 5: Total de palabras
```python
total_words = len(words)
```
Calculamos la longitud de la lista de tokens para conocer el tamaño total del corpus. Esto nos da una idea de la escala de los datos con los que estamos trabajando.

### Paso 6: Palabras únicas
```python
unique_words = len(word_counts)
```
Contamos cuántas entradas hay en nuestro `Counter`. Esto representa el vocabulario único o la "diversidad léxica" de nuestro texto.

## 4. Visualización (Líneas 66-86)
Se genera un gráfico de barras con las 10 palabras más comunes.

1. **Preparación de datos**: `zip(*top_10_words)` separa las palabras y sus frecuencias en dos listas distintas (`x` e `y`) para poder graficarlas.
2. **Configuración del gráfico**:
   - `plt.bar(...)`: Crea barras verticales.
   - `plt.xticks(rotation=45)`: Rota las palabras en el eje X para que se lean mejor.
   - `plt.show()`: Abre una ventana emergente con el gráfico resultante.

## Conclusión del Script
El script demuestra cómo palabras comunes (artículos, preposiciones) como "el", "es", "y" dominan la frecuencia simple, lo cual suele ser "ruido" en análisis más profundos. Esto prepara el terreno para aprender sobre "Stopwords" (palabras vacías) en futuros ejercicios.
