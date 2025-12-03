import pandas as pd
import streamlit as st
import os

COLUMNAS_ESPANOL = {
    'question_id': 'id_pregunta',
    'title': 'titulo',
    'body': 'cuerpo',
    'tags': 'etiquetas',
    'tag_count': 'conteo_etiquetas',
    'programming_language': 'lenguaje_programacion',
    'categories': 'categorias',
    'creation_date': 'fecha_creacion',
    'creation_year': 'anio_creacion',
    'creation_month': 'mes_creacion',
    'creation_weekday': 'dia_semana_creacion',
    'last_activity_date': 'fecha_ultima_actividad',
    'view_count': 'conteo_vistas',
    'score': 'puntaje',
    'answer_count': 'conteo_respuestas',
    'comment_count': 'conteo_comentarios',
    'favorite_count': 'conteo_favoritos',
    'is_answered': 'esta_respondida',
    'has_accepted_answer': 'tiene_respuesta_aceptada',
    'accepted_answer_score': 'puntaje_respuesta_aceptada',
    'has_code': 'tiene_codigo',
    'code_block_count': 'conteo_bloques_codigo',
    'title_word_count': 'conteo_palabras_titulo',
    'title_char_count': 'conteo_caracteres_titulo',
    'body_word_count': 'conteo_palabras_cuerpo',
    'body_char_count': 'conteo_caracteres_cuerpo',
    'difficulty_score': 'puntaje_dificultad',
    'quality_score': 'puntaje_calidad',
    'owner_reputation': 'reputacion_propietario',
    'owner_badge_count': 'conteo_insignias_propietario',
    'first_response_time_seconds': 'tiempo_primera_respuesta_seg',
    'first_response_time_hours': 'tiempo_primera_respuesta_horas',
    'top_answer_score': 'puntaje_mejor_respuesta',
    'top_answer_body_length': 'longitud_cuerpo_mejor_respuesta'
}

@st.cache_data
def cargar_dataset():
    archivo = 'stackoverflow_combined.csv'
    
    if not os.path.exists(archivo):
        st.error(f"❌ Error: No se encontró el archivo '{archivo}' en el directorio del proyecto.")
        st.info("Por favor asegúrate de que el archivo CSV esté en la misma carpeta que 'app.py'.")

        return pd.DataFrame()
        
    try:
        df = pd.read_csv(archivo)
        
        cols_existentes = set(df.columns)
        traduccion_valida = {k: v for k, v in COLUMNAS_ESPANOL.items() if k in cols_existentes}
        
        df = df.rename(columns=traduccion_valida)
        
        return df
        
    except Exception as e:
        st.error(f"Error crítico al leer el archivo CSV: {e}")
        return pd.DataFrame()