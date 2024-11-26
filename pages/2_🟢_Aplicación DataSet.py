import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown('''# Tasa de Criminalidad en E.U 2020 - 2022''')

# Cargar archivo CSV subido por el usuario
uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

# Función para leer el archivo en chunks y concatenarlos en un solo DataFrame
def cargar_archivo_en_chunks(archivo, chunksize=100000):
    chunks = pd.read_csv(archivo, chunksize=chunksize, encoding="latin-1")  # Especifica la codificación aquí
    df = pd.concat(chunks, ignore_index=True)  # Combina todos los chunks en un DataFrame
    return df

# Si el usuario ha subido un archivo, usa ese. Si no, usa el archivo por defecto.
if uploaded_file is not None:
    df = cargar_archivo_en_chunks(uploaded_file)
else:
    df = cargar_archivo_en_chunks('./static/datasets/mortality.csv')

# Tabs para diferentes análisis
tab_descripcion, tab_analisis_exploratorio, tab_filtro_final_dinamico = st.tabs(
    ["Descripción", "Análisis Exploratorio","Filtro Final Dinámico"]
)

#----------------------------------------------------------
# Generador de datos
#----------------------------------------------------------
with tab_descripcion:      
    st.markdown('''
    -------------------------------------------

    ## Introducción
    
    #### Analizador de Criminalidad
    
    ¿Qué es el fenómeno de la criminalidad en EE. UU.?
    La criminalidad en Estados Unidos se refiere a los delitos cometidos dentro del país y su impacto en la sociedad. Abarca una amplia gama de crímenes, desde delitos menores hasta crímenes violentos graves, como homicidios, asaltos y robos. Las tasas de criminalidad se calculan para evaluar la frecuencia y la distribución de los delitos en diferentes regiones, lo que ayuda a las autoridades y a la sociedad en general a entender mejor las dinámicas de la delincuencia y a implementar políticas públicas orientadas a reducirla.
    
    
    #### ¿Cuál es el objetivo del análisis?
    
    El objetivo principal del análisis de la criminalidad en Estados Unidos es proporcionar una comprensión detallada sobre las tendencias y patrones de los crímenes durante los años 2020-2022. Este análisis busca identificar los factores que contribuyen a los aumentos o disminuciones de los delitos, con énfasis en los crímenes violentos y las políticas de seguridad pública implementadas durante ese periodo.


    #### ¿Por qué es importante?
    
    El análisis de la criminalidad en EE. UU. es crucial porque permite a las autoridades, los legisladores y la sociedad en general tomar decisiones informadas sobre cómo abordar la delincuencia. Estudiar la evolución de la criminalidad en los últimos años, especialmente durante la pandemia de COVID-19, permite identificar las áreas de mayor preocupación y aplicar medidas efectivas para mejorar la seguridad pública. Además, comprender las tendencias criminales ayuda a ajustar los recursos destinados a la prevención y a la intervención, mejorando la calidad de vida en las comunidades.
    
    
     ### Desarrollo
     
    Contexto de la Criminalidad en EE. UU. (2020-2022)
    Durante los años 2020-2022, Estados Unidos enfrentó un aumento significativo en varios tipos de delitos, en gran parte impulsados por la pandemia de COVID-19, la crisis económica, y el aumento de tensiones sociales y políticas. La pandemia alteró la vida cotidiana, lo que afectó tanto a la economía como a la seguridad pública. Los confinamientos, las interrupciones en los servicios sociales y la falta de oportunidades laborales fueron factores que contribuyeron al aumento de ciertos tipos de criminalidad, incluidos los crímenes violentos y las agresiones domésticas.
    
    
    ###  Procedimiento utilizado
     
    - Análisis de Datos de Criminalidad: Se recopilaron y analizaron estadísticas sobre crímenes violentos, delitos de odio y tiroteos masivos en EE. UU. entre 2020 y 2022, a partir de fuentes como el FBI y el Bureau of Justice Statistics.

    - Identificación de Factores Sociales y Económicos: Se evaluaron los factores sociales y económicos que influyeron en el aumento de la criminalidad, como el desempleo, la pobreza, la desigualdad racial y el estrés derivado de la pandemia.

    - Estudio de Políticas Públicas: Se revisaron las políticas públicas implementadas para controlar la criminalidad, como las reformas policiales y el fortalecimiento de las leyes sobre control de armas.

    - Análisis de Tendencias Criminales: Se analizaron las tendencias de criminalidad en las principales ciudades de EE. UU. y su relación con los cambios socio-políticos y las respuestas gubernamentales.

    - Generación de Reportes y Recomendaciones: Se elaboraron reportes basados en los datos analizados y se propusieron recomendaciones sobre cómo mejorar la seguridad pública y reducir la criminalidad en el futuro.
     
     
    ##  Resultados obtenidos
     
     - Control de Armas y Tiroteos Masivos
     - Reinserción Social y Programas de Prevención
     - Impacto de la Pandemia en los Delitos
     - Desigualdad Racial y Criminalidad
     - Efectos del Uso de Tecnología en la Seguridad Pública
     - Reforma en el Sistema de Justicia Penal
     
    ## Conclusión

    - Resumen de los resultados:
        El análisis de la criminalidad en EE. UU. entre 2020 y 2022 reveló un aumento en ciertos tipos de delitos, especialmente homicidios y robos, exacerbados por la pandemia, tensiones sociales y desigualdad racial. Las soluciones implementadas incluyeron mejoras en la seguridad pública, el uso de tecnología y reformas en el sistema de justicia penal.
    
    - Logros alcanzados:
        Se lograron avances en la reducción de delitos en áreas específicas mediante el incremento de patrullas policiales y tecnologías de vigilancia. Además, se introdujeron reformas en la policía y políticas para reducir las disparidades raciales y mejorar la rehabilitación de los prisioneros.
    - Dificultades encontradas:
        Las dificultades incluyeron la resistencia a los cambios dentro de las fuerzas policiales, las preocupaciones por la privacidad con el uso de tecnologías de vigilancia y los desafíos para reducir la desigualdad racial y económica, que siguen siendo factores clave en la criminalidad.
    - Aportes personales:
        Contribuir a la reflexión sobre cómo las reformas pueden impactar positivamente en la reducción de delitos, sobre todo en comunidades marginadas, y cómo el uso responsable de la tecnología puede equilibrarse con la protección de derechos individuales.
    
    ''')


#----------------------------------------------------------
# Análisis Exploratorio
#----------------------------------------------------------
with tab_analisis_exploratorio:    
    st.markdown('''## Análisis''')

    # Primeras 5 filas del DF
    st.markdown('''#### Primeras 5 Crimenes''')
    st.dataframe(df.head())

    # Muestra la cantidad de filas y columnas del DataFrame
    st.subheader("Cantidad de Filas y Columnas")
    st.write(df.shape)

    # Muestra los tipos de datos de cada columna
    st.subheader("Tipos de Datos de Cada Columna")
    st.write(df.dtypes)

    # Identifica y muestra las columnas con valores nulos
    st.subheader("Columnas con Valores Nulos")
    st.write(df.isnull().sum())

    # Muestra un resumen estadístico de las columnas numéricas
    st.subheader("Resumen Estadístico de Columnas Numéricas")
    st.write(df.describe())


# ----------------------------------------------------------
# Filtro Final Dinámico con Gráficas Mejoradas
# ----------------------------------------------------------
with tab_filtro_final_dinamico:
    st.markdown(''' ## Filtro Final Dinámico''')
    st.markdown("""
    * Muestra un resumen dinámico del DataFrame filtrado y gráficos analíticos.
    """)

    # Filtro básico por columna y valor
    column = st.selectbox("Selecciona la columna para filtrar", options=df.columns, key="selectbox2")
    value = st.text_input(f"Introduce el valor para filtrar en {column}", key="text_input2")
    
    # Filtrar el DataFrame según la entrada
    filtered_data = df[df[column] == value] if value else df 

    # Rango adicional para limitar los datos (si la columna numérica existe)
    numeric_column = st.selectbox(
        "Selecciona una columna numérica para definir un rango", 
        options=[col for col in filtered_data.columns if pd.api.types.is_numeric_dtype(filtered_data[col])],
        key="numeric_column"
    )
    
    if numeric_column:
        min_val, max_val = st.slider(
            f"Selecciona el rango de {numeric_column}", 
            float(filtered_data[numeric_column].min()), 
            float(filtered_data[numeric_column].max()), 
            (float(filtered_data[numeric_column].min()), float(filtered_data[numeric_column].max())),
            key="range_slider"
        )
        filtered_data = filtered_data[(filtered_data[numeric_column] >= min_val) & (filtered_data[numeric_column] <= max_val)]

    # Mostrar tabla filtrada
    st.subheader("Tabla de Datos")
    st.dataframe(filtered_data.head(10))  # Mostrar solo las primeras 10 filas

    # Verificar si hay datos en el filtro para mostrar gráficos
    if not filtered_data.empty:
        st.subheader("Gráficas Analíticas")

        # Crear y mostrar 6 gráficas con diferentes combinaciones de ejes
        graficas = [
            {"x": filtered_data.columns[0], "y": filtered_data.columns[1], "title": "Gráfico 1: Comparativa"},
            {"x": filtered_data.columns[0], "y": filtered_data.columns[2], "title": "Gráfico 2: Tendencias"},
            {"x": filtered_data.columns[1], "y": filtered_data.columns[3], "title": "Gráfico 3: Relación 1 vs 3"},
            {"x": filtered_data.columns[1], "y": filtered_data.columns[4], "title": "Gráfico 4: Relación 1 vs 4"},
            {"x": filtered_data.columns[2], "y": filtered_data.columns[3], "title": "Gráfico 5: Relación 2 vs 3"},
            {"x": filtered_data.columns[2], "y": filtered_data.columns[4], "title": "Gráfico 6: Relación 2 vs 4"}
        ]

        for grafica in graficas:
            fig = px.bar(
                filtered_data, 
                x=grafica["x"], 
                y=grafica["y"], 
                title=grafica["title"], 
                labels={"x": grafica["x"], "y": grafica["y"]}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No se encontraron datos para los criterios de filtro seleccionados.")