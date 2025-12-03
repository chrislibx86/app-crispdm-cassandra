import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import db_manager

def fase_despliegue_y_novedad():
    st.header("6. Despliegue (Deployment) - Dashboard Final")
    
    st.subheader("Simulador de Predicción de Puntaje")
    
    if 'model' in st.session_state:
        model = st.session_state['model']
        
        c1, c2 = st.columns(2)
        vistas = c1.number_input("Vistas", min_value=0, value=100)
        respuestas = c2.number_input("Respuestas", min_value=0, value=2)
        comentarios = c1.number_input("Comentarios", min_value=0, value=1)
        bloques_codigo = c2.number_input("Bloques de Código", min_value=0, value=3)
        palabras_cuerpo = c1.number_input("Palabras en el Cuerpo", min_value=0, value=150)
        caracteres_titulo = c2.number_input("Caracteres en Título", min_value=0, value=50)
        dificultad = st.slider("Nivel de Dificultad (Estimado)", 0.0, 1.0, 0.5)
        
        input_data = pd.DataFrame([[vistas, respuestas, comentarios, bloques_codigo, 
                                    palabras_cuerpo, caracteres_titulo, dificultad]],
                                  columns=['conteo_vistas', 'conteo_respuestas', 'conteo_comentarios', 
                                           'conteo_bloques_codigo', 'conteo_palabras_cuerpo', 
                                           'conteo_caracteres_titulo', 'puntaje_dificultad'])
        
        if st.button("Predecir Puntaje"):
            prediccion = model.predict(input_data)[0]
            st.success(f"El puntaje predicho para esta pregunta es: **{prediccion:.2f}**")
            
            db_manager.registrar_metadata("Despliegue", {"accion": "prediccion_usuario", "resultado": prediccion})
            
    else:
        st.info("Entrena el modelo en la Fase 4 para habilitar el simulador.")

    st.markdown("---")

    st.subheader("Auditoría de Procesos de Ciencia de Datos")
    st.markdown("""
    Este tablero analiza la interacción con la metodología CRISP-DM en tiempo real, 
    extrayendo los logs almacenados en **Apache Cassandra**.
    """)
    
    historial = db_manager.obtener_historial()
    
    if historial:
        df_log = pd.DataFrame(historial, columns=['fase', 'timestamp', 'detalles'])
        
        st.markdown("#### Frecuencia de Ejecución por Fase")
        conteo_fases = df_log['fase'].value_counts()
        st.bar_chart(conteo_fases)

        st.markdown("#### Últimos Eventos Registrados en Cassandra")
        st.dataframe(df_log.sort_values(by='timestamp', ascending=False).head(5))
        
        st.caption("Estos datos provienen directamente de la tabla 'registro_fases' desde el contenedor de Docker.")
    else:
        st.warning("No hay datos en Cassandra aún. Navega por las fases para generar historial.")