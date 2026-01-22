import streamlit as st
import re
from collections import Counter
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Conteo de Palabras", page_icon="📊")

# --- FUNCIONES DE AUTENTICACIÓN ---
def check_password():
    """Retorna True si el usuario/contraseña son correctos."""
    def password_entered():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "1234":
            st.session_state["authenticated"] = True
            st.session_state["login_error"] = False 
        else:
            # Fallo en login: marcamos el error para mostrar mensaje al usuario
            st.session_state["authenticated"] = False
            st.session_state["login_error"] = True
            
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Iniciar Sesión")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        
        if st.session_state.get("login_error", False):
            st.error("Coloque el usuario correcto.")
            
        return False
    else:
        return True

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.session_state["password"] = ""
    st.rerun()

# --- CONFIGURACIÓN DE STOPWORDS ---
STOPWORDS_ES = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])

STOPWORDS_EN = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
])

# --- APP PRINCIPAL ---
if check_password():
    # Sidebar con configuración y navegación
    with st.sidebar:
        st.header("🎮 Navegación")
        seccion = st.radio("Seleccione una opción", ["Conteo palabras", "Limpieza texto/palabra"])
        
        st.markdown("---")
        st.header("⚙️ Configuración")
        st.write(f"Usuario: {st.session_state.get('username', 'admin')}")
        
        idioma = st.selectbox("Idioma del texto", ["Español", "Inglés"])
        
        if seccion == "Limpieza texto/palabra":
            min_len = st.slider("Longitud mínima de palabra", 1, 10, 3)
            limpiar_stopwords = st.checkbox("Eliminar Stopwords", value=True)
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            logout()

    # Título Principal
    st.markdown("<h1>¡Bienvenido al conteo y limpieza de palabras!</h1>", unsafe_allow_html=True)
    st.markdown(f"### Sección: {seccion}")
    st.markdown("---")

    # Instrucciones según sección
    if seccion == "Conteo palabras":
        st.info("📊 Esta sección analiza la frecuencia de las palabras tal cual aparecen en el texto.")
    else:
        st.info("🧹 Esta sección compara el texto original frente al texto limpio (sin ruido).")

    # Área de texto
    corpus_input = st.text_area(
        "Ingrese el texto aquí:",
        height=200,
        placeholder="Escribe o pega tu texto aquí..."
    )

    # Contador de caracteres
    char_count = len(corpus_input)
    st.caption(f"Caracteres actuales: {char_count} / 1200")

    if char_count > 1200:
        st.warning("⚠️ El texto excede los 1200 caracteres sugeridos.")

    # Botón de Análisis
    if st.button("🚀 Iniciar Análisis"):
        if not corpus_input.strip():
            st.error("Por favor, ingrese algún texto para analizar.")
        else:
            # --- PROCESAMIENTO ---
            text_lower = corpus_input.lower()
            words_raw = re.findall(r'\b\w+\b', text_lower)
            
            if seccion == "Conteo palabras":
                # Análisis Básico
                word_counts = Counter(words_raw)
                total_words = len(words_raw)
                unique_words = len(word_counts)
                
                # Métricas
                col1, col2 = st.columns(2)
                st.metric("Total de Palabras", total_words)
                st.metric("Palabras Únicas", unique_words)
                
                # Visualización
                top_10 = word_counts.most_common(10)
                if not top_10:
                    st.warning("No se encontraron palabras.")
                else:
                    df_top = pd.DataFrame(top_10, columns=["Palabra", "Frecuencia"])
                    st.subheader("Top 10 Palabras Más Frecuentes")
                    st.bar_chart(df_top.set_index("Palabra"))
                    
                    st.subheader("Distribución Proporcional")
                    fig = px.pie(df_top, values='Frecuencia', names='Palabra', hole=0.4)
                    st.plotly_chart(fig)
            
            else:
                # Análisis con Limpieza (Lógica de Ejercicio 2)
                stopwords_sel = STOPWORDS_ES if idioma == "Español" else STOPWORDS_EN
                
                # 1. Sin limpieza (para comparar)
                word_counts_raw = Counter(words_raw)
                
                # 2. Con limpieza: Aplicamos los filtros de forma secuencial
                words_clean = [w for w in words_raw if len(w) >= min_len]
                if limpiar_stopwords:
                    # Solo guardamos palabras que NO estén en el conjunto de stopwords
                    words_clean = [w for w in words_clean if w not in stopwords_sel]
                
                word_counts_clean = Counter(words_clean)
                
                # Métricas de Eficiencia
                total_raw = len(words_raw)
                total_clean = len(words_clean)
                ruido_eliminado = total_raw - total_clean
                porc_ruido = (ruido_eliminado / total_raw * 100) if total_raw > 0 else 0
                
                st.subheader("✨ Métricas de Limpieza")
                m1, m2, m3 = st.columns(3)
                m1.metric("Palabras Originales", total_raw)
                m2.metric("Palabras Limpias", total_clean)
                m3.metric("% Ruido Eliminado", f"{porc_ruido:.1f}%")
                
                # Visualización Comparativa
                st.markdown("---")
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.subheader("Antes de Limpiar")
                    top_raw = word_counts_raw.most_common(10)
                    if top_raw:
                        df_raw = pd.DataFrame(top_raw, columns=["Palabra", "Frecuencia"])
                        st.bar_chart(df_raw.set_index("Palabra"), color="#ff9999")
                
                with col_right:
                    st.subheader("Después de Limpiar")
                    top_clean = word_counts_clean.most_common(10)
                    if top_clean:
                        df_clean = pd.DataFrame(top_clean, columns=["Palabra", "Frecuencia"])
                        st.bar_chart(df_clean.set_index("Palabra"), color="#99ff99")
                
                # Plotly comparativo (Pie Chart del texto limpio)
                if top_clean:
                    st.subheader("Composición del Texto con Significado")
                    fig_pie = px.pie(pd.DataFrame(top_clean, columns=["Palabra", "Frecuencia"]), 
                                     values='Frecuencia', names='Palabra', hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Alphabet)
                    st.plotly_chart(fig_pie)

                # --- NUBE DE PALABRAS (WORDCLOUD) ---
                if words_clean:
                    st.markdown("---")
                    st.subheader("☁️ Nube de Palabras (Texto Limpio)")
                    
                    # Generar la nube
                    wc = WordCloud(width=800, height=400, background_color='white', 
                                  colormap='viridis').generate(' '.join(words_clean))
                    
                    # Mostrar usando matplotlib
                    fig_wc, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig_wc)

                # --- LISTADO DE STOPWORDS ---
                st.markdown("---")
                with st.expander(f"📚 Ver lista de Stopwords ({idioma})"):
                    st.write(f"Estas son las palabras que el sistema considera 'ruido' en {idioma} y que han sido filtradas (si la opción estaba activa):")
                    # Ordenamos alfabéticamente para que sea fácil de leer
                    sorted_stopwords = sorted(list(stopwords_sel))
                    st.write(", ".join(sorted_stopwords))

