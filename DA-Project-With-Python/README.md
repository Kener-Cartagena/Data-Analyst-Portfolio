# ☕ Análisis Interactivo de Ventas de Cafetería (Proyecto EDA con Python)

## 🌟 Descripción del Proyecto

Este proyecto es un **Análisis Exploratorio de Datos (EDA) de extremo a extremo** sobre las ventas de una cafetería, utilizando un *dataset* con datos sucios reales de Kaggle. El objetivo principal fue demostrar habilidades en el flujo de trabajo completo de análisis de datos: desde la limpieza de datos inconsistentes hasta la creación de una aplicación web interactiva para la toma de decisiones.

El entregable final es un **Dashboard Interactivo** que permite a cualquier usuario (gerente, dueño de negocio) explorar las métricas clave de rendimiento (KPIs) y las tendencias de venta sin necesidad de escribir código.

**Tecnologías Clave:**
* **Manipulación de Datos:** Python (Pandas)
* **Visualización Estática:** Matplotlib, Seaborn
* **Dashboard Interactivo:** Streamlit
* **Herramientas:** Visual Studio Code

## 📊 Conclusiones Clave (Insights de Negocio)


1.  **Modelo de Venta Dominante:** La cantidad de ventas es muy similar en ambos modeles: **'In-store' y 'Takeaway']**, con un **[47% - 43%]** de las ventas totales. Esto sugiere que las estrategias de marketing y personal deben centrarse en optimizar ese ambos canales.
2.  **Productos Estrella (Top 3):** Los productos que generan el mayor ingreso son: **Salad**, **Sandwich**, y **Smoothie**. Estos productos son vitales para la rentabilidad.
3.  **Calidad de los Datos:** Un **28.5 %]** de las transacciones tienen un **Método de Pago Desconocido (Unknown)** y uno **3.0** tienen un **Error**. Esta es una oportunidad crítica para mejorar los protocolos de recolección de datos en el punto de venta.
4.  **Tendencia Temporal:** A lo largo del año 2023, las ventas muestran una tendencia estable. Aunque existen picos altos y bajos en diferentes momentos del año, el desempeño general se mantiene dentro de un rango constante, sin evidenciar un crecimiento significativo.

Recomendación:
Para impulsar un crecimiento sostenido, sería útil analizar qué factores generan los picos de ventas y replicar esas estrategias en otros periodos. También se sugiere reforzar campañas en los meses más bajos y evaluar oportunidades como promociones, mejora en la experiencia del cliente o ampliación del catálogo

## 🛠️ Estructura y Flujo de Trabajo

El proyecto sigue una estructura modular y reproducible:

| Script / Directorio | Propósito | Tecnología |
| :--- | :--- | :--- |
| `data/raw/` | Almacena el *dataset* original descargado. | - |
| `scripts/clean_data.py` | Lee los datos brutos, maneja nulos, convierte tipos y estandariza texto. | **Pandas** |
| `scripts/analyze_data.py` | Genera gráficos estáticos para la exploración inicial. | **Matplotlib/Seaborn** |
| `scripts/dashboard.py` | Construye el panel interactivo, consumiendo los datos limpios. | **Streamlit** |
| `output/figures/` | Guarda los gráficos estáticos generados por `analyze_data.py`. | - |

## ⚙️ Guía de Instalación y Ejecución

Sigue estos pasos para replicar el proyecto y ejecutar el Dashboard Interactivo.

### 1. Requisitos e Instalación de Librerías

Asegúrate de tener Python (versión 3.8+) instalado. Todas las dependencias pueden instalarse con el siguiente comando:

```bash
pip install pandas matplotlib seaborn streamlit numpy pathlib