"""
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodología: Cursos Avanzados de Big Data, Ciencia de Datos, 
             Desarrollo de aplicaciones con IA & Econometría Aplicada.
Hash ID de Certificación: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADÉMICA:
- McKinney, W. (2012). Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython. O'Reilly Media.
- Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.
-------------------------
"""

# --- EJERCICIO 5: VECTORIZACIÓN Y CLUSTERING DE DOCUMENTOS (DATASET SINTÉTICO MASIVO) ---

# --- CONTEXTO ---
# Objetivo: Demostrar clustering con un volumen considerable de datos.
# Generaremos un corpus sintético de 1200 documentos en español distribuidos en 4 temas 
# para asegurar que el algoritmo de Clustering tenga material suficiente para trabajar.

import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# --- 1. GENERACIÓN DE BIG DATA SINTÉTICO ---
print("Paso 1: Generando dataset sintético de 1200 documentos...")

temas = {
    "Tecnología": ["procesador", "software", "algoritmo", "nube", "datos", "inteligencia artificial", "python", "hardware", "sistema", "redes"],
    "Finanzas": ["mercado", "inversión", "bolsa", "acciones", "economía", "banco", "interés", "crédito", "ahorro", "finanzas"],
    "Salud": ["paciente", "hospital", "médico", "tratamiento", "enfermedad", "diagnóstico", "salud", "vacuna", "terapia", "clínica"],
    "Viajes": ["turismo", "hotel", "vuelo", "playa", "montaña", "vacaciones", "pasaporte", "maleta", "guía", "aventura"]
}

corpus = []
labels_reales = []

for i, (tema, palabras) in enumerate(temas.items()):
    for _ in range(300): # 300 documentos por tema = 1200 total
        # Creamos una "frase" aleatoria usando palabras del tema
        n_palabras = random.randint(5, 15)
        frase = " ".join(random.choices(palabras, k=n_palabras))
        corpus.append(frase)
        labels_reales.append(i)

print(f"Dataset generado con {len(corpus)} documentos.")

# --- 2. VECTORIZACIÓN (TF-IDF) ---
print("\nPaso 2: Vectorizando con TF-IDF...")
# Usamos stop_words=None porque ya son solo palabras clave, pero en un caso real usaríamos 'spanish'
vectorizer = TfidfVectorizer(max_features=500)
tfidf_matrix = vectorizer.fit_transform(corpus)

print(f"Dimensiones de la matriz TF-IDF: {tfidf_matrix.shape}")

# --- 3. CLUSTERING (K-MEANS) ---
num_clusters = 4
print(f"\nPaso 3: Aplicando K-Means (k={num_clusters})...")
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
kmeans.fit(tfidf_matrix)
clusters = kmeans.labels_

# --- 4. REDUCCIÓN DE DIMENSIONALIDAD (PCA) ---
print("\nPaso 4: Reduciendo a 2D para visualización...")
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(tfidf_matrix.toarray())

# --- 5. VISUALIZACIÓN ---
print("\nPaso 5: Generando gráfico premium...")

plt.figure(figsize=(12, 8))
# Usamos una paleta de colores vibrante
scatter = plt.scatter(coords[:, 0], coords[:, 1], c=clusters, cmap='Spectral', alpha=0.7, s=30, edgecolors='k', linewidth=0.5)

plt.colorbar(scatter, label='ID del Cluster')
plt.title('Clustering de Documentos: Análisis de Tópicos Automático\n(1200 documentos en Español)', fontsize=16, fontweight='bold')
plt.xlabel('Componente Principal 1 (PCA)', fontsize=12)
plt.ylabel('Componente Principal 2 (PCA)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Guardar la imagen
save_path = "05_visualizacion_clustering.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Gráfico guardado en: {save_path}")

plt.show()

# --- 6. TOP PALABRAS POR CLUSTER ---
print("\n--- PALABRAS DOMINANTES POR CLUSTER ---")
indices_centros = kmeans.cluster_centers_.argsort()[:, ::-1]
nombres_palabras = vectorizer.get_feature_names_out()

for i in range(num_clusters):
    top_10 = [nombres_palabras[idx] for idx in indices_centros[i, :10]]
    print(f"Cluster {i}: {', '.join(top_10)}")

print("\n--- FIN DEL EJERCICIO 5 ---")
