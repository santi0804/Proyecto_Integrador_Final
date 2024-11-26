import streamlit as st
import pandas as pd
import numpy as np  # Asegúrate de importar numpy
from googleapiclient.discovery import build
from google.oauth2 import service_account

st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Sheet1", los procesa con Pandas y actualiza una segunda hoja llamada "Sheet2" con nuevos datos. La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo y visualizar los datos procesados.            
""")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = st.text_input("ID  hoja de cálculo")
RANGE1 = "Hoja 1!A:G"  # Los datos están en las columnas A, B, C y D
RANGE2 = "Hoja 2!A:G"

google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]  
secrets_dict = google_sheet_credentials.to_dict()     
creds = None
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


def read_sheet():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    if not values:
        st.error("La Hoja 1 está vacía o no contiene datos válidos.")
        return pd.DataFrame()

    # Asignar nombres de columnas manualmente
    df = pd.DataFrame(values, columns=['Columna1', 'Columna2', 'Columna3', 'Columna4', 'Columna5', 'Columna6', 'Columna7'])
    return df


def update_sheet(df):
    # Reemplazar NaN por ceros o algún valor adecuado antes de actualizar
    df = df.fillna(0)  # Puedes reemplazar los NaN por 0, o 'No disponible', etc.
    body = {'values': df.values.tolist()}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result


def realizar_operaciones(df):
    """Realiza las operaciones de suma, resta, multiplicación y división."""
    try:
        # Convertir las columnas a valores numéricos
        df['Columna1'] = pd.to_numeric(df['Columna1'], errors='coerce')
        df['Columna2'] = pd.to_numeric(df['Columna2'], errors='coerce')
        df['Columna3'] = pd.to_numeric(df['Columna3'], errors='coerce')
        df['Columna4'] = pd.to_numeric(df['Columna4'], errors='coerce')
        df['Columna5'] = pd.to_numeric(df['Columna5'], errors='coerce')
        df['Columna6'] = pd.to_numeric(df['Columna6'], errors='coerce')
        df['Columna7'] = pd.to_numeric(df['Columna7'], errors='coerce')

        # Rellenar NaN con ceros antes de las operaciones
        df.fillna(0, inplace=True)

        # Realizar operaciones
        df['Suma'] = df['Columna1'] + df['Columna2']
        df['Resta'] = df['Columna1'] - df['Columna2']
        df['Multiplicación'] = df['Columna1'] * df['Columna2']
        df['División'] = df['Columna1'] / df['Columna2'].replace(0, np.nan)  # Evitar división por cero

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
    return df


if st.button("Analizar datos de Google Sheet"):
    # Leer los datos de la Hoja 1
    df = read_sheet()
    if df.empty:
        st.stop()

    st.header("Datos de Hoja 1")
    st.dataframe(df)

    # Realizar las operaciones
    df_resultados = realizar_operaciones(df)

    # Mostrar resultados
    st.header("Resultados de operaciones")
    st.dataframe(df_resultados[['Suma', 'Resta', 'Multiplicación', 'División']])

    # Actualizar la Hoja 2 con los resultados
    result = update_sheet(df_resultados[['Suma', 'Resta', 'Multiplicación', 'División']])
    st.success(f"Hoja 2 actualizada con {result.get('updatedCells')} celdas actualizadas.")
