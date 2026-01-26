import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

# Inicializar la consola de Rich
console = Console()

# Configuración de estilo de gráficos
sns.set_theme(style="whitegrid")

def df_to_table(pandas_df, title="Data Table"):
    """Convierte un DataFrame de pandas a una Tabla de Rich."""
    table = Table(title=title, box=box.ROUNDED)
    
    # Agregar columnas
    if isinstance(pandas_df, pd.Series):
        pandas_df = pandas_df.to_frame() # Convertir Series a DF para uniformidad
        # Si es serie, ponemos el índice como columna si es relevante
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column(str(pandas_df.columns[0]), style="magenta")
        for index, row in pandas_df.iterrows():
            table.add_row(str(index), str(row.iloc[0]))
    else:
        # Agregar columnas al objeto Table
        for column in pandas_df.columns:
            table.add_column(str(column), justify="center", style="cyan")

        # Agregar filas
        for index, row in pandas_df.iterrows():
            row_data = [str(item) for item in row]
            table.add_row(*row_data)

    return table

# --- 1. CARGA DE DATOS ---
console.print(Panel.fit("1. CARGANDO DATOS", style="bold white on blue"))

with console.status("[bold green]Cargando dataset Titanic...", spinner="dots"):
    df = sns.load_dataset("titanic")

# Ver las primeras filas
console.print("\n[bold]Primeras 5 filas del dataset:[/bold]")
console.print(df_to_table(df.head(), title="Vista Previa"))

# --- 2. ANÁLISIS DE ESTRUCTURA ---
console.print(Panel.fit("2. ESTRUCTURA DEL DATASET", style="bold white on blue"))

console.print(f"Dimensiones de los datos: [bold yellow]{df.shape}[/bold yellow] (Filas, Columnas)")

# Para .info() capturamos el buffer o lo mostramos manual. Haremos una tabla resumen manual.
buffer_info = pd.DataFrame({
    'Tipo de Dato': df.dtypes,
    'No Nulos': df.count(),
    '% Nulos': (df.isnull().sum() / len(df)) * 100
})
console.print("\n[bold]Información Técnica:[/bold]")
console.print(df_to_table(buffer_info, title="Info del Dataframe"))


# --- 3. ANÁLISIS DE VALORES FALTANTES (NULLS) ---
console.print(Panel.fit("3. DETECCIÓN DE VALORES NULOS", style="bold white on blue"))

nulos = df.isnull().sum()
nulos_filtrados = nulos[nulos > 0]

if not nulos_filtrados.empty:
    console.print("[bold red]¡Se encontraron columnas con valores vacíos![/bold red]")
    console.print(df_to_table(nulos_filtrados, title="Conteo de Nulos"))
else:
    console.print("[bold green]No hay valores nulos en el dataset.[/bold green]")

# Visualización
console.print("[dim]Abriendo mapa de calor de nulos...[/dim]")
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
plt.title('Mapa de Calor de Valores Faltantes (Amarillo = Null)')
plt.show()

# --- 4. ESTADÍSTICAS DESCRIPTIVAS ---
console.print(Panel.fit("4. RESUMEN ESTADÍSTICO", style="bold white on blue"))

console.print("\n[bold]Estadísticas de Variables Numéricas:[/bold]")
# .describe() devuelve un DF, así que usamos nuestra función
console.print(df_to_table(df.describe().round(2).T, title="Describe Numérico"))

console.print("\n[bold]Estadísticas de Variables Categóricas:[/bold]")
console.print(df_to_table(df.describe(include=['O']).T, title="Describe Categórico"))

# --- 5. ANÁLISIS UNIVARIADO ---
console.print(Panel.fit("5. VISUALIZACIÓN: ANÁLISIS UNIVARIADO", style="bold white on blue"))
console.print("[dim]Generando gráficos básicos... (Revisa las nuevas ventanas)[/dim]")

# Gráfico 1
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='survived', palette='pastel')
plt.title('Conteo de Supervivientes (0=No, 1=Sí)')
plt.show()

# Gráfico 2
plt.figure(figsize=(8, 5))
sns.histplot(df['age'].dropna(), kde=True, bins=30, color='blue')
plt.title('Distribución de Edades de los Pasajeros')
plt.xlabel('Edad')
plt.show()

# --- 6. ANÁLISIS BIVARIADO ---
console.print(Panel.fit("6. VISUALIZACIÓN: RELACIONES (BIVARIADO)", style="bold white on blue"))

console.print("Analizando: [cyan]Sexo vs Supervivencia[/cyan]")
plt.figure(figsize=(6, 4))
sns.barplot(data=df, x='sex', y='survived', palette='muted')
plt.title('Tasa de Supervivencia por Sexo')
plt.ylabel('Probabilidad de Supervivencia')
plt.show()

console.print("Analizando: [cyan]Clase vs Supervivencia[/cyan]")
plt.figure(figsize=(6, 4))
sns.barplot(data=df, x='class', y='survived', palette='muted', order=['First', 'Second', 'Third'])
plt.title('Tasa de Supervivencia por Clase Social')
plt.show()

console.print("Analizando: [cyan]Edad vs Tarifa (Scatter)[/cyan]")
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='age', y='fare', hue='survived', alpha=0.6)
plt.title('Relación Edad vs Tarifa (Color = Supervivencia)')
plt.ylim(0, 300)
plt.show()

# --- 7. CORRELACIONES ---
console.print(Panel.fit("7. MATRIZ DE CORRELACIÓN", style="bold white on blue"))

corr_matrix = df.select_dtypes(include=['float64', 'int64']).corr()

# Mostrar la matriz en terminal también
console.print(df_to_table(corr_matrix.round(2), title="Matriz de Correlación"))

console.print("[dim]Abriendo mapa de calor final...[/dim]")
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Mapa de Calor de Correlaciones Numéricas')
plt.show()

console.print(Panel("FIN DEL ANÁLISIS EXPLORATORIO", style="bold green", expand=False))
