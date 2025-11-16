import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Rutas de Archivos ---
CLEANED_DATA_PATH = Path("data/cleaned/cafe_sales_cleaned.csv")
FIGURES_PATH = Path("output/figures/")
FIGURES_PATH.mkdir(parents=True, exist_ok=True) # Asegura que la carpeta de figuras exista

def load_cleaned_data(path: Path) -> pd.DataFrame:
    """Carga los datos limpios."""
    print(f"Cargando datos limpios desde: {path}")
    # Aseguramos que 'date' sea un objeto datetime para el análisis de tiempo
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_daily_sales_trend(df: pd.DataFrame):
    """Genera y guarda el gráfico de tendencia de ventas diarias."""
    
    # Agrupamos las ventas totales por día
    sales_trend = df.groupby('date')['total_sale'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    # Usamos Seaborn para una visualización más atractiva
    sns.lineplot(data=sales_trend, x='date', y='total_sale', marker='o')
    
    plt.title('Tendencia de Ventas Totales Diarias', fontsize=16)
    plt.xlabel('Fecha de Transacción', fontsize=12)
    plt.ylabel('Ventas Totales ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Guardar la figura
    plt.savefig(FIGURES_PATH / 'daily_sales_trend.png')
    plt.close() # Cierra la figura para liberar memoria
    print("Gráfico de Tendencia de Ventas Diarias guardado.")

def plot_top_3_items(df: pd.DataFrame):
    """Genera y guarda el gráfico de los 3 artículos más vendidos (por ingresos)."""
    
    df = df[(df['item'] != 'Error') & (df['item'] != 'Unknown')]
    # Agrupamos por artículo y sumamos las ventas
    top_items = df.groupby('item')['total_sale'].sum().nlargest(3).reset_index()
    
    plt.figure(figsize=(10, 7))
    # Creamos un gráfico de barras
    sns.barplot(data=top_items, x='total_sale', y='item', palette='viridis')
    
    plt.title('Top 3 Artículos por Ingresos Totales', fontsize=16)
    plt.xlabel('Ingresos Totales ($)', fontsize=12)
    plt.ylabel('Artículo', fontsize=12)
    plt.tight_layout()
    
    plt.savefig(FIGURES_PATH / 'top_3_items.png')
    plt.close()
    print("Gráfico de Top 10 Artículos guardado.")
    
def plot_sales_by_location(df: pd.DataFrame):
    """Genera y guarda un gráfico de ventas totales por tipo de ubicación."""
    
    # Filtramos valores no deseados
    df = df[(df['location'] != 'Unknown') & (df['location'] != 'Error')] 
    
    # Agrupamos por ubicación y sumamos las ventas
    sales_by_location = df.groupby('location')['total_sale'].sum().reset_index()
    
    plt.figure(figsize=(8, 6))
    sns.barplot(data=sales_by_location, x='location', y='total_sale', palette='Set2')
    
    plt.title('Ventas Totales por Ubicación', fontsize=16)
    plt.xlabel('Ubicación')
    plt.ylabel('Ventas Totales ($)')
    plt.tight_layout()
    
    plt.savefig(FIGURES_PATH / 'sales_by_location.png')
    plt.close()
    print("Gráfico de Ventas por Ubicación guardado.")


def plot_payment_distribution(df: pd.DataFrame):
    """Genera y guarda un gráfico de distribución de métodos de pago,
       agrupando los métodos menos frecuentes en 'Otros'."""
    # --- FILTRO DE VALORES NO DESEADOS ---
    df = df[~df['payment_method'].isin(['Unknown', 'Error'])]

    # 1. Calcular las frecuencias relativas
    payment_counts = df['payment_method'].value_counts(normalize=True).reset_index()
    payment_counts.columns = ['payment_method', 'percentage']
    
    # 2. Definir un umbral (ej. 2% de las transacciones)
    THRESHOLD = 0.02 
    
    # 3. Agrupar categorías pequeñas
    # Creamos una máscara para categorías con porcentaje menor al umbral (y que no sean 'Unknown')
    mask_to_group = (payment_counts['percentage'] < THRESHOLD) & (payment_counts['payment_method'] != 'Unknown')
    
    # Calculamos el porcentaje total de estas categorías pequeñas
    other_percentage = payment_counts[mask_to_group]['percentage'].sum()
    
    # Filtramos solo las categorías grandes y 'Unknown'
    payment_data = payment_counts[~mask_to_group].copy()
    
    # Añadimos la categoría 'Otros' solo si hay datos para agrupar
    if other_percentage > 0:
        payment_data.loc[len(payment_data)] = ['Otros', other_percentage]

    # Convertir el porcentaje a conteo (para el etiquetado)
    payment_data['count'] = payment_data['percentage'] * len(df)
    
    plt.figure(figsize=(9, 9))
    # Creamos el gráfico de torta con los datos agrupados
    plt.pie(payment_data['percentage'], labels=payment_data['payment_method'], 
            autopct=lambda p: f'{p:.1f}%' if p >= 1.0 else '', # Muestra el porcentaje solo si es >= 1.0%
            startangle=90, colors=sns.color_palette('pastel'))
    
    plt.title('Distribución de Métodos de Pago', fontsize=16)
    plt.tight_layout()
    
    plt.savefig(FIGURES_PATH / 'payment_distribution_grouped.png')
    plt.close()
    print("Gráfico de Distribución de Pago (Agrupado) guardado.")

if __name__ == '__main__':
    # 1. Cargar el dataset limpio
    data_clean = load_cleaned_data(CLEANED_DATA_PATH)
    
    # 2. Generar y guardar visualizaciones
    plot_daily_sales_trend(data_clean)
    plot_top_3_items(data_clean)
    plot_sales_by_location(data_clean)
    plot_payment_distribution(data_clean)
    
    print("\n¡Proceso de Análisis y Visualización completado con éxito!")