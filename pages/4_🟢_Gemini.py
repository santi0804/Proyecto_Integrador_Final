import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Generar datos simulados
ciudades = ["Bogotá", "Medellín", "Barranquilla", "Cali"]
meses = pd.date_range(start="2024-01-01", end="2024-12-01", freq="MS")
data = []

for ciudad in ciudades:
    for mes in meses:
        horas_trabajadas = np.random.randint(35, 45)
        horas_extras = np.random.randint(2, 10)
        ausentismo = round(np.random.uniform(1, 10), 2)
        productividad = round(horas_trabajadas / (horas_trabajadas + horas_extras) * 100, 2)
        causa = np.random.choice(["Enfermedad", "Licencia", "Accidente"])

        data.append([ciudad, mes, horas_trabajadas, horas_extras, ausentismo, productividad, causa])

# Crear DataFrame
df = pd.DataFrame(data, columns=["Ciudad", "Fecha", "Horas Trabajadas", "Horas Extras", "Tasa de Ausentismo (%)", "Productividad (%)", "Causa"])

# Streamlit UI
st.title("CHRONOS MANAGER - Dashboard")
st.sidebar.header("Filtros")
ciudad_seleccionada = st.sidebar.selectbox("Selecciona una ciudad:", ["Todas"] + ciudades)
mes_seleccionado = st.sidebar.selectbox("Selecciona un mes:", ["Todos"] + meses.strftime("%Y-%m").tolist())

# Filtrar datos
df_filtrado = df.copy()
if ciudad_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Ciudad"] == ciudad_seleccionada]
if mes_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Fecha"].dt.strftime("%Y-%m") == mes_seleccionado]

# Mostrar datos filtrados
st.write("### Datos Filtrados")
st.dataframe(df_filtrado)

# Asegurar que las columnas sean numéricas para el cálculo de la media
numerical_cols = df_filtrado.select_dtypes(include=["number"]).columns

# Manejar valores nulos
df_filtrado = df_filtrado.fillna(0)

# Agrupar y calcular la media
df_grouped = df_filtrado.groupby("Ciudad")[numerical_cols].mean().reset_index()

# Gráficos interactivos
st.write("### Gráficos Interactivos")
fig = px.line(df_filtrado, x="Fecha", y="Tasa de Ausentismo (%)", color="Ciudad", title="Evolución del Ausentismo")
st.plotly_chart(fig)

fig_barras = px.bar(df_filtrado, x="Ciudad", y=["Horas Trabajadas", "Horas Extras"], title="Horas Trabajadas vs Extras", barmode="group")
st.plotly_chart(fig_barras)

# Gráfico de Productividad
fig_radar = px.line_polar(
    df_grouped, 
    r="Productividad (%)", 
    theta="Ciudad", 
    line_close=True, 
    title="Índice de Productividad por Ciudad"
)
st.plotly_chart(fig_radar)

# Botón de exportar datos
if st.button("Exportar datos"):
    df_filtrado.to_csv("datos_chronos_manager.csv", index=False)
    st.success("¡Datos exportados con éxito!")
    
    # Crear un gráfico de barras para comparar la productividad de las ciudades
fig_productividad = px.bar(
    df_grouped, 
    x="Ciudad", 
    y="Productividad (%)", 
    title="Comparación de la Productividad por Ciudad", 
    color="Ciudad",
    labels={"Productividad (%)": "Productividad (%)", "Ciudad": "Ciudad"},
    color_discrete_sequence=px.colors.qualitative.Set2
)

st.plotly_chart(fig_productividad)