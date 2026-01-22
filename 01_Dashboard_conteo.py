import streamlit as st
import re
from collections import Counter
import pandas as pd
import plotly.express as px

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

# --- APP PRINCIPAL ---
if check_password():
    # Sidebar con botón de logout
    with st.sidebar:
        st.write(f"Usuario: {st.session_state.get('username', 'admin')}")
        if st.button("Cerrar Sesión"):
            logout()

    # Título Principal
    st.markdown("<h1>¡Bienvenido al conteo de palabras!</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Instrucciones
    st.info("Por favor, ingrese su corpus (Novela, cuento, canciones o discurso).")

    # Área de texto
    corpus_input = st.text_area(
        "Ingrese el texto aquí:",
        height=200,
        placeholder="Escribe o pega tu texto aquí..."
    )

    # Contador de caracteres
    char_count = len(corpus_input)
    st.caption(f"Caracteres actuales: {char_count} / 800")

    if char_count > 800:
        st.warning("⚠️ El texto excede los 800 caracteres sugeridos.")

    # Botón de Análisis
    if st.button("📊 Generar Gráfica Top 10"):
        if not corpus_input.strip():
            st.error("Por favor, ingrese algún texto para analizar.")
        else:
            # --- PROCESAMIENTO ---
            # 1. Normalización
            text_lower = corpus_input.lower()
            
            # 2. Tokenización
            words = re.findall(r'\b\w+\b', text_lower)
            
            # 3. Conteo
            word_counts = Counter(words)
            top_10 = word_counts.most_common(10)
            
            if not top_10:
                st.warning("No se encontraron palabras válidas.")
            else:
                # --- VISUALIZACIÓN ---
                st.subheader("Top 10 Palabras Más Frecuentes")
                
                # Crear DataFrame para la gráfica
                df_top = pd.DataFrame(top_10, columns=["Palabra", "Frecuencia"])
                df_top = df_top.set_index("Palabra") 
                
                # Gráfica de barras
                st.bar_chart(df_top)

                # Gráfica de Donut (Pie Chart)
                st.subheader("Distribución Proporcional")
                fig = px.pie(df_top.reset_index(), values='Frecuencia', names='Palabra', title='Distribución de Palabras (Top 10)', hole=0.4)
                st.plotly_chart(fig)
