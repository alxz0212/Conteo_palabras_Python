# Explicación Paso a Paso de `02_limpieza_texto.py`

Este documento explica el segundo ejercicio, donde el objetivo principal es aprender a **eliminar el ruido** (stopwords) del texto para que las palabras con significado real salgan a la luz.

## 1. Librerías Utilizadas

*   **`re` (Expresiones Regulares)**: Se usa para la **Tokenización**. Permite extraer solo las palabras, eliminando signos de puntuación de forma inteligente.
*   **`collections.Counter`**: Se encarga del **conteo matemático**. Cuenta automáticamente cuántas veces aparece cada palabra una vez que el texto está limpio.
*   **`matplotlib.pyplot`**: Se utiliza para la **visualización comparativa**. En este ejercicio, creamos dos figuras independientes para un análisis profundo.
*   **`wordcloud`**: Genera la **Nube de Palabras**, una forma visual y artística de identificar temas dominantes.
*   **`rich`**: La librería estrella de este ejercicio. Se encarga de convertir la aburrida terminal de texto plano en una **interfaz profesional** con colores, tablas, reglas y paneles.

---

## 2. El Concepto de Stopwords (Líneas 29-40)

En este paso introducimos la *gran diferencia* respecto al primer ejercicio: **La Limpieza Selectiva**.

Las **Stopwords** son palabras vacías como "el", "la", "de", "que". Aparecen mucho pero no aportan significado.

### 💡 Lo Nuevo: Definición del Filtro
A diferencia del script anterior donde contábamos *todo*, aquí hemos añadido manualmente una lista de palabras a ignorar.

```python
# [NUEVO] Definimos un conjunto (set) con las palabras que queremos ELIMINAR
stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 
    'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 
    'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 
    'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 
    'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 
    'e', 'o', 'u', 'algunos', 'aspectos'
])
```

**Explicación para tu equipo:**
1.  **¿Por qué un `set` y no una lista?**: En Python, buscar en un `set` (conjunto) es instantáneo, mientras que buscar en una `list` se vuelve más lento cuantas más palabras tengas. Es una optimización de velocidad.
2.  **Personalización**: Esta lista es totalmente editable. Si analizas textos médicos, podrías añadir palabras como "paciente" o "doctor" si consideras que son ruido para tu objetivo específico.

---

## 3. Procesamiento Inteligente (Función `procesar_y_contar`)

En lugar de repetir código, este script usa una **función** (línea 37) que hace tres cosas:
1.  **Normalización**: Pasa todo a minúsculas (`.lower()`).
2.  **Tokenización**: Divide el texto en palabras.
3.  **Filtrado (Limpieza)**: Si le pasamos la lista de stopwords, usa una "lista por comprensión" para quedarse solo con las palabras que NO están en esa lista.
4.  🔴 <span style="color:red">**NUEVA MEJORA: Filtrado por Longitud**</span>: Ahora el script ignora palabras muy cortas (ej: menos de 3 letras). Esto es clave porque palabras como "ni", "a", "u" o "lo" suelen ser ruido estadístico que no aporta significado.
    ```python
    # Solo guardamos palabras que tengan al menos 'min_len' caracteres
    if min_len > 1:
        words = [word for word in words if len(word) >= min_len]
    ```
5.  **Retorno Doble**: La función ahora devuelve tanto la lista de palabras filtradas como el objeto `Counter`.

---

## 4. Análisis Comparativo (Líneas 45-56)

El script realiza dos análisis sobre el mismo texto:
*   **Paso 1**: Cuenta todas las palabras originales para tener una base de comparación.
*   **Paso 2**: Realiza el conteo tras aplicar los dos filtros (Stopwords + Longitud >= 3).
*   🔴 <span style="color:red">**NUEVA MEJORA: Métricas de Eficiencia (Porcentaje de Ruido)**</span>: El script calcula matemáticamente cuánto texto se eliminó.

    ```python
    # Calculamos cuántas palabras hemos eliminado
    total_sin = len(words_sin)
    total_con = len(words_con)
    ruido_eliminado = total_sin - total_con
    
    # Regla de tres simple para sacar el porcentaje
    porcentaje_ruido = (ruido_eliminado / total_sin) * 100
    ```

    *   **Métrica 1**: Porcentaje de ruido (ej: "46.9% del texto eliminado").
    *   **Métrica 2**: Cantidad exacta de palabras descartadas.
    Esto permite cuantificar la "limpieza" de nuestros datos.

---

## 5. Visualización de "Impacto" (Líneas 63-88)

Para que el aprendizaje sea visual, el script genera una ventana con **dos sub-gráficos** (`subplots`):
*   **Gráfico Rojo**: Muestra las palabras dominantes antes de limpiar (verás muchas preposiciones y artículos).
*   **Gráfico Verde**: Muestra las palabras que quedan tras la limpieza. 

Aquí es donde ocurre la "magia": palabras como **'fantástico'**, **'producto'** o **'terrible'** pasan a los primeros puestos, permitiéndonos entender de qué trata realmente el texto.

---

## 7. Estructura de Ventanas (Dos Figuras)

Para que no pierdas ningún detalle, el script ahora genera **dos ventanas independientes** al mismo tiempo con objetivos distintos:

1.  **Figura 1 (Dashboard Avanzado)**: Es una herramienta de **analítica 360°**.
    *   **Propósito**: No solo cuenta palabras, sino que busca **interpretar** el mensaje profundo del texto. 
    *   **Nube de Palabras**: Proporciona una jerarquía visual inmediata; lo más grande es lo más relevante. Es ideal para identificar temas principales en segundos.
    *   **Perfil Emocional**: Clasifica automáticamente el texto en tres categorías críticas:
        *   **Positivo**: Identifica satisfacción, aprobación o alegría (ej: "fantástico", "recomiendo"). Ayuda a medir el éxito de un producto o campaña.
        *   **Negativo**: Detecta frustración, quejas o problemas (ej: "terrible", "desastre"). Es fundamental para la gestión de crisis y atención al cliente.
        *   **Neutro**: Palabras que informan sin carga emocional (ej: "envío", "precio"). Permite aislar los datos objetivos de las opiniones.
        *   **¿En qué ayuda?**: Permite procesar miles de opiniones humanas en segundos, identificando tendencias sin tener que leer cada frase manualmente.
    *   **Resumen Técnico**: Cuantifica la "limpieza" de los datos, mostrando la eficiencia del proceso (palabras eliminadas, longitud mínima aplicada y términos únicos).

2.  **Figura 2 (Microscopio de Limpieza)**: Es una herramienta de **validación técnica** y pedagógica.
    *   **Propósito**: Demostrar visualmente por qué el NLP requiere un pre-procesamiento riguroso.
    *   **Lado Rojo (Antes)**: Muestra cómo el "ruido" (artículos como 'el', preposiciones como 'de') oculta el mensaje real del autor.
    *   **Lado Verde (Después)**: Revela las palabras con carga semántica real (adjetivos, sustantivos, verbos) tras el filtrado.
    *   **Precisión**: Las etiquetas numéricas sobre las barras eliminan cualquier ambigüedad, permitiendo ver el conteo exacto de cada término.

## 8. Interfaz de Terminal Enriquecida con `Rich`

Para que el proyecto tenga una estética profesional fuera de los gráficos, hemos integrado la librería `rich`. Esto transforma la experiencia en la consola:

### 🔴 <span style="color:red">**NUEVA MEJORA: Diseño de Consola**</span>

*   **Reglas de Sección (`console.rule`)**: Líneas divisorias de colores que separan claramente los pasos del análisis.
    ```python
    console.rule("[bold blue]PASO 1: Análisis Inicial (Sin Limpiar)")
    ```

*   **Paneles Informativos (`Panel`)**: Los resultados de las métricas aparecen dentro de recuadros elegantes.
    ```python
    console.print(Panel(metricas_text, title="[bold green]Métricas de Eficiencia[/]", expand=False))
    ```

*   **Tablas de Datos (`Table`)**: El "Top 10" ahora es una tabla real con encabezados magenta y columnas alineadas.
    ```python
    tabla = Table(title="[bold yellow]Top 10 Palabras con Significado[/]", show_header=True, header_style="bold magenta")
    tabla.add_column("Palabra", style="cyan", justify="left")
    tabla.add_column("Frecuencia", style="green", justify="right")
    # ... se añaden las filas ...
    console.print(tabla)
    ```

---

## 9. Sistema de Menú Interactivo

El script ya no se cierra tras mostrar los gráficos, ni te obliga a ver todas las imágenes a la vez. Hemos implementado un **bucle interactivo**:

1.  **Selector de Figuras**: Al ejecutar el script, la terminal te preguntará qué deseas visualizar (Opción 1 para el Dashboard 360°, Opción 2 para la Comparativa).
2.  **Regeneración "Fresh"**: Debido a que Matplotlib libera memoria al cerrar una ventana, el script regenera la imagen completa cada vez que la seleccionas en el menú. Esto evita el problema de las "ventanas en blanco".
3.  **Salida Controlada**: La opción `3` permite cerrar el programa de forma limpia con un mensaje de despedida.

---

### Conclusión Detallada del Ejercicio

La limpieza de texto es un paso **obligatorio** en el Procesamiento de Lenguaje Natural (NLP) por las siguientes razones fundamentales:

*   **Reducción de Dimensionalidad**: Al eliminar palabras vacías (stopwords), reducimos el volumen de datos innecesarios, permitiendo que los algoritmos de IA se centren solo en los términos que realmente transmiten información valiosa.
*   **Claridad Semántica**: Sin limpieza, los términos más comunes del idioma opacan a las palabras clave. Filtrar el ruido es como "limpiar una lente" para ver con nitidez el tema real del texto.
*   **Ahorro de Cómputo**: Procesar miles de veces palabras como "el" o "de" consume recursos de CPU y memoria sin aportar valor. La eficiencia es clave en modelos de lenguaje a gran escala.
*   **Análisis de Sentimiento**: Al aislar adjetivos y verbos clave (como "fantástico" o "terrible"), podemos asignar una puntuación emocional al texto, transformando simples palabras en datos estratégicos para la toma de decisiones.
