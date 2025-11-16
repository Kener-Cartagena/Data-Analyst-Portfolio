# scripts/dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# --- Configuración y Carga de Datos ---

# Usaremos la misma ruta del archivo limpio
CLEANED_DATA_PATH = Path("data/cleaned/cafe_sales_cleaned.csv")

@st.cache_data
def load_data():
    """Carga los datos limpios y realiza conversiones necesarias."""
    try:
        df = pd.read_csv(CLEANED_DATA_PATH)
        df['date'] = pd.to_datetime(df['date'])
        # Aseguramos que la columna 'hour' exista (aunque no la usemos para el filtro)
        # La creamos a partir de 'transaction_date' que la limpiamos en clean_data.py
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['hour'] = df['transaction_date'].dt.hour
        return df
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo de datos limpio en {CLEANED_DATA_PATH}")
        return pd.DataFrame()

# -----------------------------------------------------------
# --- Título y Configuración Inicial del Dashboard ---
# -----------------------------------------------------------

st.set_page_config(
    page_title="Dashboard de Ventas de Cafetería",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("☕ Dashboard de Análisis de Ventas de Cafetería")
st.markdown("Explora las métricas clave del negocio y el rendimiento de ventas.")

data = load_data()

if data.empty:
    st.stop()

# -----------------------------------------------------------
# --- Barra Lateral de Filtros ---
# -----------------------------------------------------------

st.sidebar.header("Filtros de Exploración")

# 1. Filtro de Fechas - Mejora: Manejar selección de una sola fecha como rango de un día
min_date = data['date'].min().date()
max_date = data['date'].max().date()

date_range = st.sidebar.date_input(
    "Seleccionar Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Manejo robusto del rango de fechas
if isinstance(date_range, datetime.date):  # Caso de selección de una sola fecha
    start_date = pd.to_datetime(date_range)
    end_date = pd.to_datetime(date_range)
elif len(date_range) == 1:  # Tuple con una sola fecha
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[0])
elif len(date_range) == 2:  # Rango completo
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:  # Ninguna selección (raro, pero por seguridad)
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# 2. Filtro de Ubicación - Excluir 'Unknown' y 'Error' si aparecen, pero mantener en datos
locations = filtered_data['location'].unique().tolist()
clean_locations = [loc for loc in locations if loc not in ['Unknown', 'Error']]

selected_location = st.sidebar.multiselect(
    "Filtrar por Ubicación:",
    options=locations,
    default=clean_locations if clean_locations else locations
)

filtered_data = filtered_data[filtered_data['location'].isin(selected_location)]

# 3. Nuevo Filtro: Métodos de Pago - Para excluir 'Unknown' y 'Error' en visualizaciones si se desea
payments = filtered_data['payment_method'].unique().tolist()
clean_payments = [pm for pm in payments if pm not in ['Unknown', 'Error']]

selected_payments = st.sidebar.multiselect(
    "Filtrar por Método de Pago:",
    options=payments,
    default=clean_payments if clean_payments else payments
)

filtered_data = filtered_data[filtered_data['payment_method'].isin(selected_payments)]


# -----------------------------------------------------------
# --- 1. Key Performance Indicators (KPIs) ---
# -----------------------------------------------------------

st.header("Métricas Clave (KPIs)")

if filtered_data.empty:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
    st.stop()

# Cálculo de KPIs
total_sales = filtered_data['total_sale'].sum()
total_transactions = filtered_data['id'].nunique()
avg_transaction_value = total_sales / total_transactions if total_transactions > 0 else 0

# Mostrar los KPIs en columnas con deltas (ejemplo: comparación con total general, pero simplificado)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Ventas Totales ($)", 
        value=f"${total_sales:,.2f}"
    )
    
with col2:
    st.metric(
        label="Total de Transacciones", 
        value=f"{total_transactions:,}"
    )

with col3:
    st.metric(
        label="Valor Promedio de Transacción ($)", 
        value=f"${avg_transaction_value:,.2f}"
    )

st.markdown("---")

# -----------------------------------------------------------
# --- 2. Visualizaciones (Gráficos Interactivos) ---
# -----------------------------------------------------------

st.header("Análisis Detallado")

# Usamos dos columnas para organizar los gráficos
fig_col1, fig_col2 = st.columns(2)
fig_col3, fig_col4 = st.columns(2)

# --- Gráfico 1: Tendencia de Ventas (Línea) - Mejora: Más etiquetas y grid
with fig_col1:
    st.subheader("Tendencia de Ventas Diarias")
    sales_trend = filtered_data.groupby('date')['total_sale'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=sales_trend, x='date', y='total_sale', marker='o', ax=ax)
    
    ax.set_title('Ventas Diarias')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ventas Totales ($)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

# --- Gráfico 2: Ventas por Ubicación - Mejora: Añadir valores en barras
with fig_col2:
    st.subheader("Ventas por Ubicación")
    sales_by_location = filtered_data.groupby('location')['total_sale'].sum().sort_values(ascending=False).reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    # ✅ SOLUCIÓN: Agregar hue='location' y legend=False
    sns.barplot(data=sales_by_location, x='location', y='total_sale', 
                hue='location', palette='Pastel1', legend=False, ax=ax)
    
    # Añadir valores en las barras
    for p in ax.patches:
        ax.annotate(f"${p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 9), textcoords='offset points')
    
    ax.set_title('Ventas por Ubicación (In-store vs. Takeaway)')
    ax.set_xlabel('Ubicación')
    ax.set_ylabel('Ventas Totales ($)')
    st.pyplot(fig)

# --- Gráfico 3: Top 3 Artículos
with fig_col3:
    st.subheader("Top 3 Artículos por Ingresos")
    top_items = filtered_data.groupby('item')['total_sale'].sum().nlargest(3).reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    # ✅ SOLUCIÓN: Agregar hue='item' y legend=False
    sns.barplot(data=top_items, x='total_sale', y='item', 
                hue='item', palette='rocket', legend=False, ax=ax)
    
    # Añadir valores en las barras
    for p in ax.patches:
        ax.annotate(f"${p.get_width():,.0f}", (p.get_width(), p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    
    ax.set_title('Top 3 Artículos')
    ax.set_xlabel('Ingresos Totales ($)')
    ax.set_ylabel('Artículo')
    st.pyplot(fig)

# --- Gráfico 4: Distribución de Métodos de Pago (Pie) - Mejora: Excluir 'Unknown'/'Error' si no seleccionados
with fig_col4:
    st.subheader("Distribución de Pago")
    payment_counts = filtered_data['payment_method'].value_counts(normalize=True).reset_index()
    payment_counts.columns = ['payment_method', 'percentage']
    
    THRESHOLD = 0.02
    mask_to_group = (payment_counts['percentage'] < THRESHOLD) & (~payment_counts['payment_method'].isin(['Unknown', 'Error']))
    other_percentage = payment_counts[mask_to_group]['percentage'].sum()
    payment_data = payment_counts[~mask_to_group].copy()
    
    if other_percentage > 0:
        payment_data = pd.concat([payment_data, pd.DataFrame({'payment_method': ['Otros'], 'percentage': [other_percentage]})], ignore_index=True)
    
    # Filtrar explícitamente 'Unknown' y 'Error' si no están seleccionados (ya filtrado arriba)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(payment_data['percentage'], labels=payment_data['payment_method'], 
           autopct=lambda p: f'{p:.1f}%' if p >= 1.0 else '', 
           startangle=90, colors=sns.color_palette('pastel'))
    
    ax.set_title('Distribución de Métodos de Pago')
    st.pyplot(fig)

st.markdown("---")
st.caption("Proyecto de Análisis de Datos para portfolio. Desarrollado con Python, Pandas, Matplotlib, Seaborn y Streamlit.")