# Explicación Paso a Paso de `01_Dashboard_conteo.py`

Este documento explica cómo funciona el Dashboard interactivo creado con Streamlit para el análisis de frecuencia de palabras.

## 1. Librerías Utilizadas

Para este dashboard, además de las librerías básicas de procesamiento, utilizamos herramientas para la web y visualización avanzada:

*   **`streamlit`**: Es el corazón del dashboard. Permite crear aplicaciones web usando solo Python, sin necesidad de saber HTML, CSS o JavaScript.
*   **`re` (Expresiones Regulares)**: La usamos para limpiar el texto y extraer solo las palabras (tokenización), igual que en el ejercicio anterior.
*   **`collections.Counter`**: Se encarga de contar cuántas veces aparece cada palabra de forma eficiente.
*   **`pandas`**: Una librería fundamental para el análisis de datos. La usamos para organizar los resultados en tablas (DataFrames) que las gráficas puedan leer fácilmente.
*   **`plotly.express`**: Permite crear gráficas interactivas y profesionales (como el gráfico de donut) que el usuario puede explorar con el ratón.

---

## 2. Estructura de Secciones (Navegación)

El Dashboard ahora se divide en dos herramientas principales que puedes seleccionar desde la **Sidebar (barra lateral)**:

### A. Conteo palabras
*   **Propósito**: Realiza un análisis de frecuencia puro.
*   **Funcionamiento**: Cuenta todas las palabras tal cual las ingresas, sin filtros adicionales (excepto la conversión a minúsculas).
*   **Resultados**: Muestra el total de palabras, palabras únicas, un gráfico de barras del Top 10 y un gráfico de donut.

### B. Limpieza texto/palabra (Basado en Ejercicio 2)
*   **Propósito**: Revelar el significado real del texto eliminando el ruido.
*   **Controles Adicionales**:
    *   **Longitud mínima**: Slider para ignorar palabras cortas (ej: descarta palabras de menos de 3 letras).
    *   **Eliminar Stopwords**: Interruptor para filtrar palabras vacías según el idioma.
*   **Resultados Comparativos**: Muestra dos gráficos de barras ("Antes" vs "Después") para que veas visualmente cómo la limpieza hace que las palabras clave emerjan.
*   **Visualizaciones de Impacto**:
    *   **Nube de Palabras (WordCloud)**: Una representación artística donde el tamaño indica la relevancia. Útil para captar la esencia del texto en un segundo.
    *   **Diccionario de Stopwords**: Un botón desplegable (`expander`) que te permite auditar exactamente qué palabras está filtrando el sistema como ruido.

---

## 3. Métricas de Eficiencia (Sección Limpieza)

En la sección de limpieza, el Dashboard calcula tres indicadores clave:
1.  **Palabras Originales**: El tamaño inicial de tu texto.
2.  **Palabras Limpias**: Cuántas palabras "con sustancia" quedaron tras aplicar los filtros.
3.  **% Ruido Eliminado**: Qué porcentaje del texto era irrelevante. Esto te dice qué tan denso en información es tu contenido.

---

## 4. Lógica de Autenticación y Configuración

*   **Seguridad**: El sistema requiere usuario (`admin`) y contraseña (`1234`) para acceder.
*   **Idioma**: Puedes alternar entre **Español** e **Inglés** desde la barra lateral. Esto ajusta automáticamente la lista de Stopwords que se aplicará en la sección de Limpieza.

---

## Conclusión
Este dashboard transforma un script de consola en una herramienta visual interactiva, facilitando la interpretación de los datos para cualquier usuario sin necesidad de leer el código fuente.
