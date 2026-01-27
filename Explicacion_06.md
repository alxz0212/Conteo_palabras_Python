# Explicación 06: Super Dashboard del Titanic con Streamlit

## 🚢 Descripción General

Este dashboard es una aplicación web interactiva construida con **Streamlit** que permite explorar el famoso conjunto de datos del Titanic. A diferencia de un script de análisis estático, este dashboard ofrece una experiencia visual inmersiva ("Super Dashboard") con animaciones, estilos modernos y gráficos 3D.

## 🌟 Características Principales

### 1. Animaciones Lottie

Se han integrado animaciones ligeras (archivos JSON) usando la librería `streamlit-lottie`. Esto añade un toque visual dinámico (un barco navegando) que hace que la aplicación se sienta "viva" y moderna, superando la estética de un dashboard corporativo estándar.

### 2. Diseño "Dark Mode" Premium

Utilizamos CSS personalizado inyectado a través de `st.markdown` para:

- Crear un fondo con degradados (Azul Océano).
- Estilizar las tarjetas de métricas (KPIs) con efectos de cristal (glassmorphism).
- Asegurar que los textos y títulos resalten con colores neón/brillantes.

### 3. Filtros Interactivos (Sidebar)

La barra lateral permite filtrar la data en tiempo real por:

- **Clase (Pclass)**: 1ra, 2da, 3ra.
- **Género (Sex)**: Hombre, Mujer.
- **Puerto de Embarque**: Cherbourg, Queenstown, Southampton.
- **Rango de Edad**: Slider para ajustar el rango de interés.

### 4. Visualizaciones Avanzadas (Plotly)

- **Sunburst Chart**: Un gráfico jerárquico que muestra la proporción de supervivientes desglosada por clase y sexo de una sola vez. Interactúa haciendo clic en los sectores.
- **Scatter 3D**: Exploración multidimensional de `Edad` vs `Tarifa` vs `Clase`. Permite rotar y hacer zoom para encontrar patrones ocultos (ej. ¿pagaron más los que sobrevivieron?).
- **Histograma**: Distribución de edades comparando supervivientes vs fallecidos.

## 🛠️ Tecnologías Usadas

- **Streamlit**: Framework principal para la web app.
- **Pandas**: Manipulación de datos.
- **Plotly Express**: Gráficos interactivos y 3D.
- **Streamlit-Lottie**: Integración de animaciones.
- **Requests**: Para cargar la animación Lottie desde una URL.

## 🚀 Cómo Ejecutarlo

Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
streamlit run 06_Titanic_Dashboard.py
```

Esto abrirá automáticamente una pestaña en tu navegador con el dashboard funcionando. ¡Disfruta explorando los datos!
