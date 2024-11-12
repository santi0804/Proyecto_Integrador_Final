import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")


# Título y subtítulo
st.title("CHRONOS MANAGER")
st.subheader("GESTOR DE HORARIOS, CONTROL DE ACCESOS Y ANALIZADOR DE DATOS")
st.subheader("Brindamos soluciones a las gestiones administrativas con nuestro equipo Alpha Developers")

image_path = "./static/control acceso.png"  # Reemplaza con la ruta de la foto
image = Image.open(image_path)  # Imagen de fondo
horizontal_image = image.resize((1100, 350)) 
st.image(horizontal_image) 


st.header("Equipo Alpha Developers")   # Integrantes


col1, col2, col3 = st.columns(3)

with col1:
    st.image("./static/santi.jpeg", width=200)  # Reemplaza con la ruta de la foto..
    st.write("**Santiago Tamayo**")
    st.write("Desarrollador de Software")
    

with col2:
    st.image("./static/anderson.jpeg", width=170)  # Reemplaza con la ruta de la foto
    st.write("**Anderson Alzate**")
    st.write("Desarrollador de Software")
    
    
with col3:
    st.image("./static/jorge.jpeg", width=220)  # Reemplaza con la ruta de la foto
    st.write("**Jorge Uribe**")
    st.write("Desarrollador de Software")


# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
Un Gestor Inteligente de Horarios y Accesos es una solución innovadora creada para optimizar la administración del tiempo y la seguridad en empresas. Con el objetivo principal de simplificar el control de accesos, la gestión de horas extras y la validación de ausencias, este sistema aborda la problemática de la necesidad de nuestros clientes de mejorar la eficiencia y visibilidad en la gestión de personal en áreas administrativas. Chronos Manager utiliza una plataforma centralizada e intuitiva que permite una administración integral y en tiempo real, enlazada con datos relacionados en la nube mediante Firebase, mejorando la productividad y garantizando un entorno laboral seguro y organizado. Con su enfoque adaptable, Chronos Manager es ideal para cualquier empresa que busque modernizar sus procesos y asegurar una gestión precisa y eficiente del recurso humano.
""")

# Más información
st.header("Más Información")

# Puedes añadir secciones como:
# - Tecnología utilizada
# - Resultados esperados
# - Presentación de resultados (fecha y formato)
# - Contacto para preguntas

st.write("""
Chronos Manager es una herramienta innovadora que no solo facilita la gestión de horarios y accesos, sino que también integra tecnologías en la nube, como Firebase, para un almacenamiento seguro y accesible de datos. Esta innovación permite a las empresas acceder a la información en cualquier momento y desde cualquier lugar, proporcionando visibilidad total sobre la asistencia, horas extras y ausencias del personal. Además, la implementación de notificaciones inteligentes ayuda a los administradores a estar al tanto de los eventos importantes, como accesos no autorizados o excesos de horas trabajadas. Con esta capacidad de supervisión y análisis, Chronos Manager no solo optimiza los procesos administrativos, sino que también potencia la toma de decisiones estratégicas para mejorar el ambiente laboral y la eficiencia organizacional.
""")

# Footer con links
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.google.com">Google</a> |
        <a href="https://www.facebook.com">Facebook</a> |
        <a href="https://www.linkedin.com">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)