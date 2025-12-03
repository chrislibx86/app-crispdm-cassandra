import streamlit as st
from data_loader import cargar_dataset
from fases import (
    fase_comprension_negocio,
    fase_comprension_datos,
    fase_preparacion_datos,
    fase_modelado,
    fase_evaluacion
)
from dashboard import fase_despliegue_y_novedad
from database import db_manager


st.set_page_config(
    page_title="CRISP-DM StackOverflow",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'df_raw' not in st.session_state:
    st.session_state['df_raw'] = cargar_dataset()

# Sidebar - Menú Hamburguesa
st.sidebar.title("CRISP-DM Workflow")
opcion = st.sidebar.radio(
    "Selecciona una fase:",
    [
        "1. Comprensión del Negocio",
        "2. Comprensión de los Datos",
        "3. Preparación de los Datos",
        "4. Modelado",
        "5. Evaluación",
        "6. Despliegue & Dashboard"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Autor:** Eduardo Mendieta")
st.sidebar.info("Conectado a Cassandra (Docker)")

st.title("Análisis de StackOverflow con Metodología CRISP-DM")

if opcion == "1. Comprensión del Negocio":
    fase_comprension_negocio()

elif opcion == "2. Comprensión de los Datos":
    fase_comprension_datos()

elif opcion == "3. Preparación de los Datos":
    fase_preparacion_datos()

elif opcion == "4. Modelado":
    fase_modelado()

elif opcion == "5. Evaluación":
    fase_evaluacion()

elif opcion == "6. Despliegue & Dashboard":
    fase_despliegue_y_novedad()


st.markdown("---")
st.caption("Proyecto desarrollado en Python con Streamlit y Apache Cassandra.")