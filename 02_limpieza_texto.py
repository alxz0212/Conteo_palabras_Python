# --- EJERCICIO 2: LIMPIEZA DE RUIDO Y EL IMPACTO VISUAL ---

# --- CONTEXTO ---
# Objetivo: Aprender a limpiar texto eliminando "stopwords" (palabras comunes sin significado semántico)
# y visualizar de forma impactante cómo esta limpieza cambia el análisis de frecuencia, haciendo que
# las palabras verdaderamente importantes emerjan.
#
# ¿Qué son las Stopwords? Son palabras como 'el', 'y', 'o', 'de', que son extremadamente frecuentes
# pero no nos dicen nada sobre el tema o el sentimiento de un texto. Son el "ruido" del lenguaje.

# --- IMPORTACIONES ---
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --- CORPUS Y STOPWORDS ---
# ... (corpus y stopwords_es se mantienen igual) ...
corpus = [
    "Me encanta este producto, es fantástico y muy útil.",
    "El servicio al cliente fue terrible, muy decepcionante.",
    "El precio es adecuado, ni caro ni barato.",
    "No volvería a comprar, la calidad es pésima.",
    "Una experiencia increíble, lo recomiendo totalmente.",
    "El envío tardó más de lo esperado.",
    "Fantástico, simplemente fantástico.",
    "No está mal, pero podría mejorar en algunos aspectos.",
    "La batería dura poquísimo, un desastre."
]

stopwords_es = set([
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'las', 'un', 'por', 'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'sin', 'sobre', 'este', 'ya', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'hasta', 'desde', 'mucho', 'hacia', 'mi', 'se', 'ni', 'ese', 'yo', 'qué', 'e', 'o', 'u', 'algunos', 'aspectos'
])

# 3. MEJORA: Diccionarios de Sentimiento para el ejercicio
positivas = {'encanta', 'fantástico', 'útil', 'adecuado', 'increíble', 'recomiendo', 'totalmente', 'mejorar'}
negativas = {'terrible', 'decepcionante', 'caro', 'pésima', 'mal', 'desastre', 'poquísimo'}

# --- PROCESAMIENTO ---

# 2. MEJORA: Filtrado por longitud (ignorar palabras muy cortas)
def procesar_y_contar(text, stopwords=None, min_len=1):
    """Toma un bloque de texto, lo normaliza, tokeniza y opcionalmente elimina stopwords y palabras cortas."""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Aplicamos filtros
    if stopwords:
        words = [word for word in words if word not in stopwords]
    
    if min_len > 1:
        words = [word for word in words if len(word) >= min_len]
        
    return words, Counter(words)

# 1. Análisis SIN limpieza
print("Paso 1: Analizando frecuencias SIN limpiar el texto...")
all_text = ' '.join(corpus)
words_sin, word_counts_sin_limpieza = procesar_y_contar(all_text)
top_10_sin_limpieza = word_counts_sin_limpieza.most_common(10)

# 2. Análisis CON limpieza (Opción 1 y 2 integradas)
print("\nPaso 2: Analizando frecuencias CON limpieza (Stopwords + Longitud >= 3)...")
words_con, word_counts_con_limpieza = procesar_y_contar(all_text, stopwords=stopwords_es, min_len=3)
top_10_con_limpieza = word_counts_con_limpieza.most_common(10)

# 1. MEJORA: Cálculo de métricas de eficiencia (Porcentaje de Ruido)
total_sin = len(words_sin)
total_con = len(words_con)
ruido_eliminado = total_sin - total_con
porcentaje_ruido = (ruido_eliminado / total_sin) * 100

print(f"Total de palabras tras limpieza: {total_con}")
print(f"MÉTRICA 1: Se ha eliminado un {porcentaje_ruido:.1f}% de texto considerado 'ruido'.")
print("Top 10 palabras (con limpieza):", top_10_con_limpieza)

# 4. MEJORA: Análisis de Sentimiento Básico
pos_count = sum(1 for w in words_con if w in positivas)
neg_count = sum(1 for w in words_con if w in negativas)
neu_count = total_con - (pos_count + neg_count)

# --- VISUALIZACIÓN MULTI-PANEL REFINADA ---

print("\nGenerando visualizaciones refinadas...")

# Creamos una figura con una cuadrícula de 2x2 y mejor espaciado
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('#f0f2f6') # Color de fondo suave

# 1. Gráfico de Barras - Explicación: "Muestra la frecuencia absoluta de términos clave"
ax1 = fig.add_subplot(2, 2, 1)
words_plot, counts_plot = zip(*top_10_con_limpieza)
ax1.bar(words_plot, counts_plot, color='#3498db', edgecolor='navy', alpha=0.7)
ax1.set_title('1. Frecuencia de Palabras Clave', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Repeticiones')
ax1.tick_params(axis='x', rotation=40)
ax1.grid(axis='y', linestyle='--', alpha=0.6)
ax1.text(0.5, -0.42, "Muestra los términos más frecuentes tras eliminar\nel 'ruido' (stopwords) y filtrar por longitud.", 
         transform=ax1.transAxes, ha='center', fontsize=9, style='italic', color='#555')

# 2. Nube de Palabras - Explicación: "Visión artística de los temas dominantes"
ax2 = fig.add_subplot(2, 2, 2)
wordcloud = WordCloud(width=800, height=500, background_color='#f0f2f6', 
                      colormap='magma', max_words=50).generate(' '.join(words_con))
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis('off')
ax2.set_title('2. Mapa Interactivo de Conceptos', fontsize=14, fontweight='bold', pad=15)
ax2.text(0.5, -0.20, "El tamaño de cada palabra indica su importancia relativa.\nA mayor tamaño, más presencia en el corpus analizado.", 
         transform=ax2.transAxes, ha='center', fontsize=10, style='italic', color='#555')

# 3. Análisis de Sentimiento - Explicación: "Tono emocional de los mensajes"
ax3 = fig.add_subplot(2, 2, 3)
labels = ['Positivo', 'Negativo', 'Neutro']
sizes = [pos_count, neg_count, neu_count]
colors = ['#2ecc71', '#e74c3c', '#bdc3c7']
ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, 
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}, pctdistance=0.8)
center_circle = plt.Circle((0,0), 0.60, fc='#f0f2f6')
fig.gca().add_artist(center_circle) # Convertir a Donut
ax3.set_title('3. Perfil Emocional (Sentimiento)', fontsize=14, fontweight='bold', pad=15)
ax3.text(0.5, -0.15, "Detecta el sentimiento comparando palabras con un\ndiccionario predefinido de términos positivos/negativos.", 
         transform=ax3.transAxes, ha='center', fontsize=10, style='italic', color='#555')

# 4. Panel de Métricas y Conclusión
ax4 = fig.add_subplot(2, 2, 4)
ax4.axis('off')
# Ajustamos el cuadro para que sea un poco más grande y centrado
rect = plt.Rectangle((0.05, 0.05), 0.9, 0.9, facecolor='white', edgecolor='#34495e', alpha=0.9, transform=ax4.transAxes, linewidth=1.5)
ax4.add_patch(rect)

# Usamos texto sin emojis para evitar advertencias de fuentes (Glyph missing)
info_text = (
    f"  RESUMEN TÉCNICO\n"
    f"  --------------------------\n"
    f"  * Palabras Iniciales: {total_sin}\n"
    f"  * Palabras Finales: {total_con}\n"
    f"  * Longitud Mínima:   3 letras\n"
    f"  * Ruido Eliminado:   {porcentaje_ruido:.1f}%\n"
    f"  * Términos Únicos:   {len(word_counts_con_limpieza)}\n\n"
    f"  CONCLUSIÓN:\n"
    f"  El análisis revela un tono {('positivo' if pos_count > neg_count else 'negativo')}\n"
    f"  donde la palabra '{top_10_con_limpieza[0][0]}'\n"
    f"  es el eje central del mensaje."
)
ax4.text(0.12, 0.5, info_text, fontsize=11, fontweight='medium', va='center', fontfamily='monospace', color='#2c3e50', transform=ax4.transAxes)

plt.suptitle('Sistema Avanzado de Análisis de Texto (Exercise 2: NLP)', fontsize=22, fontweight='bold', y=0.98, color='#2c3e50')
plt.subplots_adjust(wspace=0.3, hspace=0.7) # Ajuste manual de espacios: hspace aumentado para dar aire

# --- NUEVA VISUALIZACIÓN: COMPARATIVA (FIGURA 2) ---

print("Generando comparativa directa (Rojo vs Verde)...")

# Creamos una segunda figura independiente
fig2, (ax_red, ax_green) = plt.subplots(1, 2, figsize=(18, 9))
fig2.patch.set_facecolor('#fdfdfd')

# Gráfico Rojo: Sin Limpieza
words_sin_p2, counts_sin_p2 = zip(*top_10_sin_limpieza)
bars_red = ax_red.bar(words_sin_p2, counts_sin_p2, color='#e74c3c', alpha=0.8, edgecolor='darkred')
ax_red.bar_label(bars_red, padding=3, fontsize=10, fontweight='bold') # AÑADIR VALORES
ax_red.set_title('ANTES de limpiar (Ruido innecesario)', fontsize=15, color='darkred', fontweight='bold', pad=20)
ax_red.tick_params(axis='x', rotation=45)
ax_red.set_ylabel('Frecuencia')
ax_red.grid(axis='y', linestyle='--', alpha=0.3)

# Gráfico Verde: Con Limpieza
words_con_p2, counts_con_p2 = zip(*top_10_con_limpieza)
bars_green = ax_green.bar(words_con_p2, counts_con_p2, color='#27ae60', alpha=0.8, edgecolor='darkgreen')
ax_green.bar_label(bars_green, padding=3, fontsize=10, fontweight='bold') # AÑADIR VALORES
ax_green.set_title('DESPUÉS de limpiar (Palabras con valor)', fontsize=15, color='darkgreen', fontweight='bold', pad=20)
ax_green.tick_params(axis='x', rotation=45)
ax_green.grid(axis='y', linestyle='--', alpha=0.3)

# Añadir conclusión a la Figura 2
conclusion_fig2 = (
    "CONCLUSION: La limpieza elimina las palabras funcionales (el, la, que) para que emerjan las palabras\n"
    "con contenido real (fantastico, producto, servicio). Sin este paso, el analisis estaria sesgado por el lenguaje común."
)
fig2.text(0.5, 0.02, conclusion_fig2, ha='center', fontsize=12, style='italic', weight='medium', 
          bbox=dict(facecolor='#27ae60', alpha=0.1, boxstyle='round,pad=1'))

fig2.suptitle('Impacto Visual de la Limpieza de Texto (NLP)', fontsize=20, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0.08, 1, 0.95]) # Ajuste para dejar espacio al texto de abajo

# Mostrar ambas figuras
plt.show()

print("\n--- FIN DEL EJERCICIO 2 (VERSIÓN OPTIMIZADA) ---")
print("Observación: ¡El cambio es drástico! El gráfico de la derecha revela las palabras que realmente aportan significado:")
print("'fantástico', 'producto', 'calidad', 'terrible'. Ahora sí podemos empezar a pensar en el sentimiento.")
