# 📊 Proyecto de Conteo de Palabras y Dashboard

Este repositorio contiene herramientas prácticas para introducirse en el Procesamiento de Lenguaje Natural (NLP) usando Python. El proyecto evoluciona desde un script básico de análisis de texto hasta un Dashboard web interactivo y seguro.

![Demostración interactiva del Dashboard](imagenes/dashboard_demo.webp)

## 📁 Contenido del Proyecto

### 1. `01_conteo_palabras.py` (Script Introductorio)
Un script de Python puro que demuestra los fundamentos del análisis de texto:
- **Normalización**: Conversión a minúsculas.
- **Tokenización**: Uso de Expresiones Regulares (`re`) para separar palabras.
- **Conteo**: Uso de `collections.Counter` para calcular frecuencias.
- **Visualización**: Gráfico de barras estático.

### 2. `02_limpieza_texto.py` (Limpieza y Análisis Avanzado)
Evolución técnica enfocada en la calidad del dato:
- **Filtro de Stopwords**: Eliminación de palabras vacías (el, la, de).
- **Filtro de Longitud**: Ignora palabras irrelevantes por su tamaño.
- **Analítica Visual**: Genera una **Nube de Palabras** y un **Perfil Emocional** (Sentimiento).
- **Doble Ventana**: Comparativa directa "Antes vs Después".

### 3. `01_Dashboard_conteo.py` (Aplicación Web)
Una aplicación interactiva construida con **Streamlit** que integra todas las herramientas anteriores.

**Características Principales:**
- **🔐 Acceso Seguro**: Sistema de login protegido.
- **🎮 Navegación Dual**: Pestañas de "Conteo Puro" y "Limpieza Profunda".
- **☁️ Visualización**: Nube de palabras y gráficas comparativas en tiempo real.
- **📚 Diccionario de Ruidos**: Consulta interactiva de Stopwords.

---

## 📖 Guías de Estudio Detalladas
Para entender paso a paso cómo se construyó cada fase, puedes consultar estas guías:
*   [Guía Ejercicio 1 (Fundamentos)](Explicacion_01.md): Explicación del conteo básico.
*   [Guía Ejercicio 2 (Limpieza y Sentimiento)](Explicacion_02.md): Cómo filtrar el ruido y detectar emociones.
*   [Guía del Dashboard](Explicacion_Dashboard.md): Estructura del panel web y seguridad.

## 🚀 Cómo Ejecutar

### 1. Instalación de Requisitos
Asegúrate de instalar las librerías necesarias ejecutando:
```bash
pip install streamlit plotly matplotlib pandas wordcloud
```

### 2. Ejecutar los Scripts de Análisis (Consola)
Para los ejercicios de lógica y fundamentos por consola:

**Ejercicio 1 (Básico):**
```bash
python 01_conteo_palabras.py
```

**Ejercicio 2 (Avanzado - Dos ventanas):**
```bash
python 02_limpieza_texto.py
```

### 3. Ejecutar el Dashboard (Web)
Para lanzar la aplicación web interactiva:
```bash
streamlit run 01_Dashboard_conteo.py
```
> [!TIP]
> Si usas un entorno virtual y tienes problemas con los módulos, ejecuta:
> `python -m streamlit run 01_Dashboard_conteo.py`

---

## 📜 Créditos y Referencias
Este proyecto ha sido desarrollado siguiendo la metodología y el código base de Juan Marcelo Gutierrez Miranda (@TodoEconometria).

**Autor original:** Juan Marcelo Gutierrez Miranda  
**Institución:** @TodoEconometria  
**Hash de Certificación:** `4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c`

### Referencias Bibliográficas:
1. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.
2. Streamlit Documentation. *Build powerful data apps in minutes*. [docs.streamlit.io](https://docs.streamlit.io)
3. Matplotlib Development Team. *Matplotlib: A 2D graphics environment*. [matplotlib.org](https://matplotlib.org)

---

## 👨‍💻 Realizado por
**Daniel Alexis Mendoza Corne**  
*Ingeniero Informático y de sistemas*  
[GitHub Profile](https://github.com/alxz0212)
