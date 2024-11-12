import random 
from faker import Faker
import streamlit as st 
import pandas as pd  
import seaborn as sns
import matplotlib.pyplot as plt
import firebase_admin  
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Configurar la página
st.set_page_config(layout="wide")


if not firebase_admin._apps:    
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"]
    secrets_dict = firebase_credentials.to_dict()
    cred = credentials.Certificate(secrets_dict)
    app = firebase_admin.initialize_app(cred)
db = firestore.client()

tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(
    ["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtro Final Dinámico"]
)

#----------------------------------------------------------
#Descripciòn del sitio.// nuevos cambios
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''   

    ## Introducción

    -   Que somos:
        Chronos Manager es una solución integral diseñada para optimizar la gestión de horarios, el control de accesos, y el registro de horas extras y ausencias en entornos laborales y educativos. Utiliza tecnología avanzada para facilitar la planificación de horarios, garantizar la seguridad mediante control de accesos, y proporcionar un seguimiento efectivo de la asistencia y el tiempo trabajado. Esta plataforma centralizada permite a los administradores gestionar fácilmente la ocupación de espacios y supervisar el rendimiento de los empleados o estudiantes.
    
    -   Obejtivo:  Nuestro objetivo principal de Chronos Manager es proporcionar una herramienta eficiente y fácil de usar que permita a las organizaciones gestionar sus horarios y accesos de manera efectiva. Esto incluye la planificación de turnos, el registro de horas trabajadas, la gestión de ausencias y horas extras, y la implementación de controles de acceso seguros. Al hacerlo, se busca mejorar la productividad, optimizar los recursos, y asegurar un entorno de trabajo o aprendizaje organizado y seguro.
    
    -   Por qué es importante: La importancia de Chronos Manager radica en la creciente necesidad de las organizaciones de adaptarse a un entorno laboral y educativo dinámico y en constante cambio. Con la evolución de las prácticas laborales y las exigencias de seguridad, es fundamental contar con herramientas que faciliten la gestión eficiente del tiempo y los accesos. Este proyecto no solo ayuda a minimizar el riesgo de acceso no autorizado, sino que también proporciona a los líderes información valiosa sobre la asistencia y el rendimiento, lo que a su vez permite la toma de decisiones informadas y la implementación de mejoras continuas en la gestión de recursos humanos.

    ## Desarrollo

    -   Explicación detallada del proyecto : Somos un software diseñado para gestionar controles de acceso, horas extras y ausencias en áreas administrativas de cualquier tipo de empresa. Facilita el monitoreo de asistencia, la validación de ausentismos y el seguimiento del tiempo extra trabajado, optimizando la eficiencia operativa.
    
    -   Procedimiento utilizado :  Para implementar Chronos Manager, se integran dispositivos de control de acceso con una plataforma central que registra horarios, ausencias y horas extras. Los datos se procesan y visualizan en un panel intuitivo para los administradores.
        Tambien se pueden adaptar a sistemas operativos actualizados.
    
    -   Resultados obtenidos:  Los resultados incluyen una mejora significativa en la organización de los horarios, un aumento en la seguridad del acceso, y una reducción del tiempo dedicado a gestionar ausencias y horas extras, lo cual contribuye a una mayor productividad empresarial.

    ## Conclusión

    -   Resumen de los   Chronos Manager ha mejorado la gestión de horarios, el control de accesos y la validación de ausencias en áreas administrativas, optimizando el flujo de trabajo y garantizando la seguridad.
    
    -   Logros alcanzados: Se logró una administración centralizada y automatizada de los horarios, con un control preciso de accesos, horas extras y ausencias, reduciendo los errores y aumentando la productividad.
    
    -   Dificultades encontradas: Se presentaron desafíos en la integración con sistemas de control de acceso preexistentes y en la adaptación a las necesidades específicas de cada empresa.

    -   Aportes personales: Nuestras contribuciónes se centran en el desarrollo de funcionalidades de validación de ausencias y en la personalización de la interfaz de usuario, buscando mejorar la experiencia del administrador en el manejo de datos y control de accesos.
    ''')
    
#----------------------------------------------------------
# Generación de registros de empleados
#----------------------------------------------------------

def generate_employee_records(n):
    empleados = [
        {'ID': '001', 'Nombre': 'Juan Pérez'},
        {'ID': '002', 'Nombre': 'Ana Gómez'},
        {'ID': '003', 'Nombre': 'Carlos Ruiz'},
        {'ID': '004', 'Nombre': 'Laura Díaz'},
        {'ID': '005', 'Nombre': 'Sofía Castillo'},
        {'ID': '007', 'Nombre': 'Manuel Longas'},
        {'ID': '008', 'Nombre': 'Dario Gomez'},
        {'ID': '009', 'Nombre': 'Donal Trump'},
        {'ID': '010', 'Nombre': 'James Rodriguez'},
        {'ID': '011', 'Nombre': 'Esperanza Gomez'},
        {'ID': '012', 'Nombre': 'Megan Fox'},
    ]

    registros = []
    fecha_inicio = datetime(2023, 1, 1)
    for _ in range(n):
        fecha = (fecha_inicio + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        empleado = random.choice(empleados)
        hora_entrada = random.choice(['08:00', '08:15', '09:00', ''])
        hora_salida = '' if hora_entrada == '' else random.choice(['17:00', '17:30', '18:00', '18:30'])
        horas_trabajadas = 0 if hora_entrada == '' else round(random.uniform(7, 9), 1)
        horas_extras = max(0, horas_trabajadas - 8)
        ausente = 'Sí' if hora_entrada == '' else 'No'

        registros.append([fecha, empleado['ID'], empleado['Nombre'], hora_entrada, hora_salida,
                          horas_trabajadas, horas_extras, ausente])

    return pd.DataFrame(registros, columns=[
        'Fecha', 'ID', 'Nombre', 'Hora Entrada', 'Hora Salida',
        'Horas Trabajadas', 'Horas Extras', 'Ausente'
    ])

#----------------------------------------------------------
# Generador de datos
#----------------------------------------------------------

with tab_Generador:
    st.write('Esta función genera datos ficticios de empleados y sus registros de acceso.')
    st.subheader('Registros de Empleados')
    num_records = st.number_input('Número de registros a generar', min_value=1, max_value=5000, value=5000)
    
    if st.button('Generar Registros de Empleados'):
        
        df = generate_employee_records(num_records)
        st.dataframe(df)
        st.session_state.df = df  # Guardar los datos en el estado de sesión
        df.to_csv('registro_accesos.csv', index=False, encoding='utf-8')
        st.success(f'Archivo CSV generado exitosamente con {num_records} registros.')

#----------------------------------------------------------
# Mostrar los datos y aplicar filtros
#----------------------------------------------------------

with tab_datos:
    st.write('Muestra los registros almacenados y permite aplicar filtros.')

    if 'df' in st.session_state:  # Usar los datos guardados en el estado de sesión
        df = st.session_state.df
        
        tab_fecha, tab_empleado, tab_extras, tab_registros = st.tabs(["Fecha", "Empleados", "Extras", "Registros de Empleados"])
        
        with tab_fecha:
            st.write('Filtro de fechas y horas trabajadas')
            column_order = ['Fecha', 'ID', 'Hora Entrada', 'Hora Salida', 'Horas Trabajadas', 'Horas Extras']
            df_tab_fecha = df.reindex(columns=column_order)
            st.dataframe(df_tab_fecha)

        with tab_empleado:
            st.write('Filtro de ID y empleados')
            column_order = ['ID', 'Nombre']
            df_tab_empleado = df.reindex(columns=column_order)
            st.dataframe(df_tab_empleado)

        with tab_extras:
            st.write('Filtro de ID, horas extras y ausencias')
            column_order = ["ID", 'Horas Extras', 'Ausente']
            df_tab_extras = df.reindex(columns=column_order)
            st.dataframe(df_tab_extras)

        with tab_registros:
            st.write('Todos los registros de empleados.')
            st.dataframe(df)
            st.subheader('Filtrar registros por fecha')

            fecha_inicio = st.date_input('Fecha de inicio', datetime(2022, 1, 1))
            fecha_fin = st.date_input('Fecha de fin', datetime(2024, 12, 31))

            df['Fecha'] = pd.to_datetime(df['Fecha'])

            if fecha_inicio <= fecha_fin:
                df_filtrado = df[(df['Fecha'] >= pd.to_datetime(fecha_inicio)) & (df['Fecha'] <= pd.to_datetime(fecha_fin))]
                st.dataframe(df_filtrado)
            else:
                st.error("La fecha de inicio debe ser anterior o igual a la fecha fin.")

#----------------------------------------------------------
# Análisis Exploratorio
#----------------------------------------------------------

with tab_Análisis_Exploratorio:
    if 'df' in st.session_state:
        df = st.session_state.df  # Usar los datos guardados en el estado de sesión
        st.title("Análisis de Horarios")
        st.write(df.head())  # Mostrar las primeras 5 filas

        st.markdown("### Análisis Estadístico:")
        st.write(df.describe())

        st.markdown("### Gráficas:")

        # Crear una figura con dos subgráficas (una al lado de la otra)
        fig, (ax1, ax2) = plt.subplots(figsize=(12, 6), ncols=2)

        # Primera gráfica: Distribución de Horas Trabajadas
        sns.histplot(df['Horas Trabajadas'], kde=True, ax=ax1, color='skyblue')
        ax1.set_title("Distribución de Horas Trabajadas", fontsize=12)
        ax1.set_xlabel("Horas Trabajadas", fontsize=10)
        ax1.set_ylabel("Frecuencia", fontsize=10)

        # Filtrar datos de empleados con horas extras
        df_extras = df[df['Horas Extras'] > 0]  # Filtra los empleados con horas extras mayores a 0

        # Extraer el año de la columna 'Fecha'
        df_extras['Año'] = pd.to_datetime(df_extras['Fecha']).dt.year  # Extrae el año de la fecha

        # Segunda gráfica: Tendencia de Empleados con Horas Extras
        sns.lineplot(
            data=df_extras,
            x="Año",  # Usar el año extraído de la columna 'Fecha'
            y="Horas Extras",  # Mostrar las horas extras
            hue="Nombre",  # Diferenciar por empleado (Nombre)
            palette="coolwarm",
            ax=ax2  # Especificamos el eje para la gráfica
        )
        ax2.set_xlabel("Año", fontsize=10)
        ax2.set_ylabel("Horas Extras", fontsize=10)
        ax2.set_title("Tendencia de Horas Extras por Empleado y Año", fontsize=12)

        # Ajuste del layout para que no se superpongan
        plt.tight_layout()

        # Mostrar las gráficas
        st.pyplot(fig)
        
#----------------------------------------------------------
# Filtro Final Dinámico
#----------------------------------------------------------

with tab_Filtro_Final_Dinámico:
    st.title("Filtro Final Dinámico")
    if 'df' in st.session_state:
        df = st.session_state.df  # Usar los datos guardados en el estado de sesión

        columna_seleccionada = st.selectbox('Selecciona una columna para filtrar', df.columns)

        if df[columna_seleccionada].dtype == 'object':
            valor_filtro = st.selectbox(f'Selecciona un valor para "{columna_seleccionada}"', df[columna_seleccionada].unique())
            df_filtrado = df[df[columna_seleccionada] == valor_filtro]
            st.dataframe(df_filtrado)
        else:
            valor_filtro = st.slider(f'Selecciona un rango para "{columna_seleccionada}"', min_value=int(df[columna_seleccionada].min()), max_value=int(df[columna_seleccionada].max()))
            df_filtrado = df[df[columna_seleccionada] == valor_filtro]
            st.dataframe(df_filtrado)
