import streamlit as st
from google.cloud import aiplatform

# Configurar Vertex AI
PROJECT_ID = "tu-proyecto-id"  # Reemplaza con el ID de tu proyecto de Google Cloud
LOCATION = "us-central1"  # Ubicación del modelo
MODEL_NAME = "tu-modelo-id"  # ID del modelo en Google AI Studio
ENDPOINT_ID = "tu-endpoint-id"  # Endpoint configurado en Google AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def obtener_respuesta_google(pregunta, contexto):
    """
    Enviar pregunta y contexto a un modelo de Vertex AI y obtener la respuesta.
    """
    try:
        # Crear cliente de endpoint
        endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}")

        # Enviar solicitud al modelo
        instances = [{"input": f"{contexto}\nPregunta: {pregunta}"}]
        response = endpoint.predict(instances=instances)

        # Procesar la respuesta
        return response.predictions[0] if response.predictions else "No se recibió respuesta."
    except Exception as e:
        return f"Error al procesar la solicitud: {e}"

# Streamlit: Configuración de la interfaz
st.title("CHRONOS MANAGER - Dashboard")

st.write("### Asistente Gemini IA")
pregunta_usuario = st.text_input("Haz una pregunta sobre el proyecto o los datos:")

contexto = """
Este proyecto se llama 'CHRONOS MANAGER'. La información del componente principal incluye datos relacionados con horas trabajadas, ausentismo y productividad en diversas áreas.
"""

if st.button("Preguntar"):
    if pregunta_usuario.strip():
        respuesta = obtener_respuesta_google(pregunta_usuario, contexto)
        st.write("### Respuesta")
        st.write(respuesta)
    else:
        st.warning("Por favor, ingresa una pregunta.")
