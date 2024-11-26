import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px

# Configuración de la API de Generative AI
genai.configure(api_key='AIzaSyA_y4aB3PUdc5SIUGtH5rnU73vVFlVchd0')
modelo = genai.GenerativeModel("gemini-1.5-flash")

# Definir datos de categorías de horarios
datos_horarios = {
    "trabajo": {
        "color": "#3498db",  # Azul
        "imagen": "https://icons.iconarchive.com/icons/paomedia/small-n-flat/128/alarm-clock-icon.png",
        "icono": "🕒",
        "descripcion": "Horas de trabajo programadas",
        "ejemplos": ["Entrada", "Salida", "Horas Extra"]
    },
    "ausencias": {
        "color": "#e74c3c",  # Rojo
        "imagen": "https://icons.iconarchive.com/icons/paomedia/small-n-flat/128/cancel-icon.png",
        "icono": "❌",
        "descripcion": "Registros de ausencias o permisos",
        "ejemplos": ["Permiso", "Vacaciones", "Licencia"]
    },
    "horas_extra": {
        "color": "#2ecc71",  # Verde
        "imagen": "https://icons.iconarchive.com/icons/paomedia/small-n-flat/128/clock-icon.png",
        "icono": "⏰",
        "descripcion": "Horas trabajadas fuera del horario regular",
        "ejemplos": ["Horas extra en la mañana", "Horas extra en la noche"]
    }
}

# Función para clasificar con explicación
def identificar_categoria_con_explicacion(descripcion_horario):
    prompt = f"""
    Clasifica el siguiente registro: '{descripcion_horario}' en una de estas categorías:
    - trabajo (si es relacionado con horarios regulares o tareas programadas)
    - ausencias (si es un permiso o ausencia de un empleado)
    - horas_extra (si es una tarea realizada fuera del horario regular)
    
    Además, proporciona una breve explicación del porqué el registro pertenece a esa categoría.
    """
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

# Configuración de la página
st.set_page_config(
    page_title="Clasificador de Horarios - Chronos Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .categoria-card {
        background: linear-gradient(135deg, #2ecc71, #3498db);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: #fff;
        padding: 1.5rem;
        border-radius: 10px;
    }
    .categoria-card:hover {
        transform: scale(1.1);
        box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.5);
    }
    .resultado {
        padding: 1rem;
        background-color: #34495e;
        color: white;
        text-align: center;
        border-radius: 10px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado
if 'categoria_seleccionada' not in st.session_state:
    st.session_state.categoria_seleccionada = None

# Layout principal
st.title("⏰ Clasificador de Horarios - Chronos Manager IA")

# Entrada de texto para clasificar
horario = st.text_input("¿Qué registro deseas clasificar?", placeholder="Ejemplo: entrada de 8:00 AM")

if st.button("Buscar"):
    if horario:
        with st.spinner("Analizando..."):
            resultado = identificar_categoria_con_explicacion(horario)
            st.session_state.categoria_seleccionada = resultado
            st.markdown(f"""
                <div class='resultado'>
                    <h3>Resultado:</h3>
                    <p>{resultado}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Por favor, ingresa un registro para clasificar.")

# Mostrar tarjetas de categorías
st.markdown("## Categorías disponibles")
cols = st.columns(3)
for i, (categoria, datos) in enumerate(datos_horarios.items()):
    with cols[i]:
        st.markdown(f"""
            <div class='categoria-card' style="border-left: 5px solid {datos['color']}">
                <div><b>{datos['icono']} {categoria.title()}</b></div>
                <p>{datos['descripcion']}</p>
                <p><i>Ejemplos: {', '.join(datos['ejemplos'])}</i></p>
            </div>
        """, unsafe_allow_html=True)

# Subida de archivo CSV
archivo = st.file_uploader("Sube un archivo CSV para clasificar registros", type=["csv"])
if archivo:
    df = pd.read_csv(archivo)
    st.dataframe(df.head())
    
    if "Registro" in df.columns:
        with st.spinner("Clasificando registros..."):
            df['Categoría'] = df['Registro'].apply(identificar_categoria_con_explicacion)
        st.dataframe(df)
    else:
        st.error("El archivo debe contener una columna llamada 'Registro'.")

# Gráfica de resultados interactiva
if archivo:
    categorias = df['Categoría'].value_counts().reset_index()
    categorias.columns = ['Categoría', 'Conteo']

    fig = px.pie(
        categorias, 
        values='Conteo', 
        names='Categoría', 
        title='Distribución de Categorías de Horarios',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig)

# Función para responder preguntas sobre el controlador de horarios
def responder_pregunta(pregunta):
    prompt = f"""
    Estoy construyendo un proyecto llamado "Controlador de Horarios". Este proyecto gestiona y clasifica registros de horarios de empleados en diferentes categorías como trabajo, ausencias y horas extras.
    
    Aquí está la pregunta: "{pregunta}"
    
    Por favor, proporciona una respuesta detallada y útil.
    """
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip()

# Entrada de texto para preguntas
pregunta = st.text_input("Haz una pregunta sobre el Controlador de Horarios")

if st.button("Responder"):
    if pregunta:
        with st.spinner("Generando respuesta..."):
            respuesta_pregunta = responder_pregunta(pregunta)
            st.markdown(f"""
                <div class='resultado'>
                    <h3>Respuesta:</h3>
                    <p>{respuesta_pregunta}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Por favor, ingresa una pregunta sobre el Controlador de Horarios.")