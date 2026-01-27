import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Titanic Super Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS Personalizados ---
st.markdown("""
    <style>
    /* Fondo General de la App */
    .stApp {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%); /* 'Deep Sea' gradient */
        color: white;
    }
    
    /* Fondo del Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b161c;
        border-right: 1px solid #1f3a46;
    }
    
    /* Títulos y Encabezados */
    h1, h2, h3, h4, h5, h6 {
        color: #6dd5fa !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Textos en Sidebar */
    .css-17lntkn, .css-16idsys, p, label {
        color: #e0f7fa !important;
    }
    
    /* Métricas (KPIs) */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        backdrop-filter: blur(5px);
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: scale(1.02);
        background-color: rgba(255, 255, 255, 0.1);
    }
    .stMetric-value {
        color: #00d2ff !important;
    }
    
    /* Gráficos Plotly */
    .js-plotly-plot .plotly .modebar {
        orientation: v; /* Hace la barra de herramientas vertical para que moleste menos */
    }
    </style>
    """, unsafe_allow_html=True)

# --- Función para Cargar Lottie ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- Cargar Datos ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

data = load_data()

# --- Barra Lateral (Sidebar) ---
st.sidebar.header("🎛️ Filtros del Tablero")

# Animación Lottie en Sidebar
# URL Alternativa: Un barco en el mar (animación más simple y fiable)
lottie_url = "https://lottie.host/5a70498a-5309-4ffc-a335-512cb5954605/5G7e8M5g2L.json" 
# Si falla, usaremos un emoji gigante como fallback
lottie_ship = load_lottieurl(lottie_url)

with st.sidebar:
    if lottie_ship:
        st_lottie(lottie_ship, height=150, key="ship_sidebar")
    else:
        st.markdown("<div style='text-align: center; font-size: 60px;'>🚢</div>", unsafe_allow_html=True)

pclass = st.sidebar.multiselect(
    "Clase del Pasajero (Pclass)",
    options=sorted(data['Pclass'].unique()),
    default=sorted(data['Pclass'].unique())
)

sex = st.sidebar.multiselect(
    "Género (Sex)",
    options=data['Sex'].unique(),
    default=data['Sex'].unique()
)

embarked = st.sidebar.multiselect(
    "Puerto de Embarque",
    options=data['Embarked'].unique(),
    default=data['Embarked'].dropna().unique()
)

age_range = st.sidebar.slider(
    "Rango de Edad",
    min_value=int(data['Age'].min()),
    max_value=int(data['Age'].max()),
    value=(0, 80)
)

# Aplicar Filtros
df_selection = data.query(
    "Pclass == @pclass & Sex == @sex & Embarked == @embarked & Age >= @age_range[0] & Age <= @age_range[1]"
)

# --- Contenido Principal ---

col1, col2 = st.columns([1, 5])
with col1:
    # Reutilizamos la animación visualmente si cargó, sino icono
    if lottie_ship:
        st_lottie(lottie_ship, height=80, key="ship_title")
    else:
         st.markdown("# ⚓")

with col2:
    st.title("Análisis del Titanic")
    st.markdown("*Explora los misterios del océano con datos interactivos.*")

st.markdown("---")

# --- KPIs (Key Performance Indicators) ---
try:
    total_passengers = df_selection.shape[0]
    survival_rate = (df_selection['Survived'].mean() * 100)
    avg_age = df_selection['Age'].mean()
    avg_fare = df_selection['Fare'].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(label="👥 Pasajeros", value=f"{total_passengers}")
    kpi2.metric(label="🛟 Supervivencia", value=f"{survival_rate:.1f}%")
    kpi3.metric(label="🎂 Edad Media", value=f"{avg_age:.1f} años")
    kpi4.metric(label="💵 Precio Medio", value=f"${avg_fare:.1f}")

except Exception as e:
    st.error("Selecciona filtros para ver los datos.")

st.markdown("---")

# --- Visualizaciones Gráficas ---

# Fila 1: Sunburst y Barras
col_charts_1, col_charts_2 = st.columns(2)

with col_charts_1:
    st.subheader("🧬 Jerarquía de Supervivencia")
    if not df_selection.empty:
        df_sunburst = df_selection.fillna("Unknown")
        df_sunburst['Survived_Label'] = df_sunburst['Survived'].map({0: 'No Sobrevivió', 1: 'Sobrevivió'})
        
        fig_sun = px.sunburst(
            df_sunburst,
            path=['Pclass', 'Sex', 'Survived_Label'],
            values='PassengerId',
            color='Survived_Label',
            color_discrete_map={'Sobrevivió': '#00F260', 'No Sobrevivió': '#F71735', 'Unknown': '#333'},
            title=""
        )
        fig_sun.update_layout(
            margin=dict(t=0, l=0, r=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=14)
        )
        st.plotly_chart(fig_sun, use_container_width=True)
        
        # --- Resumen Dinámico Sunburst ---
        survivors = df_selection[df_selection['Survived'] == 1]
        if not survivors.empty:
            top_sex = survivors['Sex'].value_counts().idxmax()
            top_class = survivors['Pclass'].value_counts().idxmax()
            st.info(f"💡 **Insight**: En esta selección, la mayor cantidad de supervivientes son **{top_sex}s** de **Clase {top_class}**.")
        else:
            st.info("💡 **Insight**: No hay supervivientes en la selección actual.")

with col_charts_2:
    st.subheader("📊 Distribución de Edades")
    if not df_selection.empty:
        fig_hist = px.histogram(
            df_selection, 
            x='Age', 
            color='Survived', 
            nbins=20,
            barmode='overlay',
            color_discrete_map={0: '#F71735', 1: '#00F260'},
            opacity=0.75
        )
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", 
            font_color="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#333"),
            margin=dict(t=20, l=0, r=0, b=0),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # --- Resumen Dinámico Histograma ---
        avg_age_surv = df_selection[df_selection['Survived']==1]['Age'].mean()
        avg_age_dead = df_selection[df_selection['Survived']==0]['Age'].mean()
        
        msg = "💡 **Insight**: "
        if not pd.isna(avg_age_surv):
            msg += f"Edad media supervivientes: **{avg_age_surv:.1f} años**. "
        if not pd.isna(avg_age_dead):
            msg += f"Fallecidos: **{avg_age_dead:.1f} años**."
        st.info(msg)

# Fila 2: Scatter Plot por CLase
st.subheader("🌌 Análisis Detallado: Edad vs Tarifa por Clase")
st.caption("Cada punto es un pasajero. Observa cómo la clase y la tarifa influyen en la supervivencia.")

if not df_selection.empty:
    # Añadimos columna de texto para el color
    df_selection['Status'] = df_selection['Survived'].map({0: 'Fallecido', 1: 'Sobrevivió'})
    
    fig_scatter = px.scatter(
        df_selection,
        x='Age',
        y='Fare',
        color='Status',
        facet_col='Pclass',
        hover_data=['Name', 'Sex'],
        color_discrete_map={'Sobrevivió': '#00F260', 'Fallecido': '#F71735'},
        opacity=0.6,
        size_max=10
    )
    
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis=dict(gridcolor="#333"),
        xaxis=dict(gridcolor="#333"),
        margin=dict(l=0, r=0, b=0, t=30),
        legend=dict(orientation="h", y=1.1)
    )
    # Ajustar grid lines para cada faceta
    fig_scatter.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    fig_scatter.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # --- Resumen Dinámico Scatter ---
    max_fare = df_selection['Fare'].max()
    rich_surv_rate = df_selection[df_selection['Fare'] > df_selection['Fare'].mean()]['Survived'].mean() * 100
    
    st.info(f"💡 **Insight**: La tarifa más alta mostrada es **${max_fare:.2f}**. Los pasajeros que pagaron más del promedio tienen una tasa de supervivencia del **{rich_surv_rate:.1f}%**.")
else:
    st.warning("No hay datos para mostrar el gráfico.")

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6dd5fa;'>
        <small>🚢 Dashboard Titanic v2.0 | Potenciado por Streamlit Lottie & Plotly</small>
    </div>
""", unsafe_allow_html=True)
