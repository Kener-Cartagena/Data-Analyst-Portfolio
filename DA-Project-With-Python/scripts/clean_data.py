# scripts/clean_data.py

import pandas as pd
import numpy as np
from pathlib import Path

# --- Rutas de Archivos ---
# Asumimos que el dataset sucio se llama 'cafe_sales_dirty_data.csv'
# ¡Asegúrate de cambiar este nombre si el tuyo es diferente!
RAW_DATA_PATH = Path("data/raw/dirty_cafe_sales.csv")
CLEANED_DATA_PATH = Path("data/cleaned/cafe_sales_cleaned.csv")
CLEANED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True) # Asegura que la carpeta 'cleaned' exista

def load_data(path: Path) -> pd.DataFrame:
    """Carga los datos desde la ruta especificada."""
    print(f"Cargando datos desde: {path}")
    # Usamos low_memory=False para asegurar que Pandas infiera los tipos correctamente
    return pd.read_csv(path, low_memory=False)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza la limpieza y transformación de los datos."""
    print("Iniciando proceso de limpieza...")

    # 1. Renombrar columnas para consistencia (Snake Case)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.rename(columns={'transaction_id': 'id',
                       'price_per_unit': 'unit_price',
                       'total_spent': 'total_sale'}, inplace=True)

    # 2. Conversión de Tipos de Datos
    
    # Columna de Fecha: Convertir a datetime y extraer componentes útiles
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df.dropna(subset=['transaction_date'], inplace=True) # Elimina filas con fechas inválidas
    
    # Crear características de tiempo
    df['date'] = df['transaction_date'].dt.date
    df['weekday'] = df['transaction_date'].dt.day_name()
    df['month'] = df['transaction_date'].dt.month_name()
    

    # Columnas Numéricas: Convertir a tipo numérico (flotante)
    # Algunos valores pueden tener símbolos de moneda que debemos eliminar
    for col in ['unit_price', 'total_sale']:
        # Eliminamos cualquier carácter no numérico excepto el punto/coma decimal
        df[col] = df[col].astype(str).str.replace(r'[$,]', '', regex=True)
        # Convertimos a numérico, forzando los errores a NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 'Quantity' debe ser un entero
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['quantity'] = df['quantity'].fillna(1).astype(int) # Rellenamos NaN con 1 y convertimos a entero
    
    # 3. Manejo de Valores Nulos (NaN)
    
    # Rellenar nulos en categóricas con 'Unknown' (por ejemplo, 'Payment Method', 'Location', 'Item')
    for col in ['item', 'payment_method', 'location']:
        df[col] = df[col].fillna('Unknown')
    
    # Eliminar filas con valores críticos nulos (total_sale, unit_price)
    df.dropna(subset=['total_sale', 'unit_price'], inplace=True)

    # 4. Consistencia de Datos Categóricos
    
    # Estandarizar mayúsculas/minúsculas y eliminar espacios extra en columnas clave
    for col in ['item', 'payment_method', 'location']:
        df[col] = df[col].astype(str).str.strip().str.title()
        
    # 5. Filtrado de Valores Atípicos (Outliers) e Inconsistencias Lógicas
    
    # Eliminar transacciones con precios o ventas negativos o cero (lógicamente incorrecto para una venta)
    df = df[(df['total_sale'] > 0) & (df['unit_price'] > 0)]
    
    # Asegurar que la 'total_sale' sea consistente con la fórmula: Quantity * Unit Price
    # Esto es opcional, pero ayuda a corregir errores en el dataset.
    df['calculated_sale'] = df['quantity'] * df['unit_price']
    
    # Para ser estrictos, podríamos solo usar la 'total_sale' original si no hay mucha discrepancia,
    # o usar la calculada si es un error conocido. Aquí usaremos la 'total_sale' original,
    # pero es bueno tener la columna de chequeo.

    print(f"Limpieza finalizada. Filas restantes: {len(df)}")
    return df

def save_data(df: pd.DataFrame, path: Path):
    """Guarda el DataFrame limpio en un archivo CSV."""
    print(f"Guardando datos limpios en: {path}")
    # Guardamos sin el índice de Pandas, ya que no es necesario
    df.to_csv(path, index=False)
    print("¡Proceso completado con éxito!")

if __name__ == '__main__':
    # 1. Cargar el dataset sucio
    data_dirty = load_data(RAW_DATA_PATH)
    
    # 2. Limpiar y preprocesar
    data_clean = clean_data(data_dirty.copy())
    
    # 3. Guardar el dataset limpio
    save_data(data_clean, CLEANED_DATA_PATH)