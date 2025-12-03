import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from database import db_manager

# --- Fase 1: Comprensión del Negocio ---
def fase_comprension_negocio():
    st.header("1. Comprensión del Negocio")
    
    st.write("""
    **Objetivo del Proyecto:**
    El objetivo principal es predecir la popularidad o calidad de una pregunta de StackOverflow, 
    representada por su **'Puntaje' (Score)**.
    
    **Preguntas Clave:**
    1. ¿Qué factores influyen más en que una pregunta reciba votos positivos?
    2. ¿La longitud del título o del cuerpo afecta la puntuación?
    3. ¿La cantidad de etiquetas está correlacionada con la visibilidad?
    
    **Metas de Minería de Datos:**
    - Identificar variables correlacionadas con 'puntaje'.
    - Entrenar un modelo de regresión para estimar el puntaje basado en metadatos técnicos.
    """)
    
    if st.button("Registrar Fase de Negocio en BD"):
        db_manager.registrar_metadata("Comprensión del Negocio", {"estado": "completado", "objetivo": "prediccion_puntaje"})
        st.success("Fase registrada en Cassandra.")

# --- Fase 2: Comprensión de los Datos ---
def fase_comprension_datos():
    st.header("2. Comprensión de los Datos")
    
    if 'df_raw' not in st.session_state:
        st.error("Por favor carga los datos primero (esto debería ser automático).")
        return

    df = st.session_state['df_raw']
    
    st.subheader("Vista Preliminar del Dataset")
    st.dataframe(df.head())
    
    st.subheader("Estadísticas Descriptivas")
    st.write(df.describe())
    
    st.subheader("Análisis de Distribución")
    fig, ax = plt.subplots()
    sns.histplot(df['puntaje'], kde=True, ax=ax)
    ax.set_title("Distribución del Puntaje")
    st.pyplot(fig)

    db_manager.registrar_metadata("Comprensión de Datos", {
        "filas": len(df), 
        "columnas": len(df.columns),
        "variable_objetivo": "puntaje"
    })

# --- Fase 3: Preparación de los Datos ---
def fase_preparacion_datos():
    st.header("3. Preparación de los Datos")
    
    if 'df_raw' not in st.session_state:
        return

    df = st.session_state['df_raw'].copy()
    
    st.markdown("### Limpieza y Selección de Características")
    
    st.write("Manejo de valores nulos: Rellenando numéricos con la mediana.")
    cols_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    for col in cols_numericas:
        df[col] = df[col].fillna(df[col].median())
        
    features = ['conteo_vistas', 'conteo_respuestas', 'conteo_comentarios', 
                'conteo_bloques_codigo', 'conteo_palabras_cuerpo', 
                'conteo_caracteres_titulo', 'puntaje_dificultad']
    target = 'puntaje'
    
    st.write(f"**Variables Predictoras (X):** {', '.join(features)}")
    st.write(f"**Variable Objetivo (y):** {target}")
    
    X = df[features]
    y = df[target]
    
    st.session_state['X'] = X
    st.session_state['y'] = y
    st.session_state['df_clean'] = df
    
    st.success("Datos preparados y listos para modelado.")
    
    db_manager.registrar_metadata("Preparación de Datos", {
        "features_seleccionados": features,
        "nulos_tratados": True
    })

# --- Fase 4: Modelado ---
def fase_modelado():
    st.header("4. Modelado")
    
    if 'X' not in st.session_state:
        st.warning("Debes completar la fase de Preparación de Datos primero.")
        return

    X = st.session_state['X']
    y = st.session_state['y']
    
    st.markdown("### Configuración del Modelo")
    split_size = st.slider("Porcentaje de prueba (Test Size)", 0.1, 0.5, 0.2)
    n_estimators = st.slider("Número de árboles (Random Forest)", 10, 200, 100)
    
    if st.button("Entrenar Modelo"):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_size, random_state=42)
        
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
        model.fit(X_train, y_train)
        
        st.session_state['model'] = model
        st.session_state['X_test'] = X_test
        st.session_state['y_test'] = y_test
        
        st.success("Modelo Random Forest entrenado exitosamente.")
        
        db_manager.registrar_metadata("Modelado", {
            "algoritmo": "RandomForestRegressor",
            "n_estimators": n_estimators,
            "test_size": split_size
        })

# --- Fase 5: Evaluación ---
def fase_evaluacion():
    st.header("5. Evaluación")
    
    if 'model' not in st.session_state:
        st.warning("Debes entrenar el modelo primero.")
        return

    model = st.session_state['model']
    X_test = st.session_state['X_test']
    y_test = st.session_state['y_test']
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    col1, col2 = st.columns(2)
    col1.metric("Error Cuadrático Medio (MSE)", f"{mse:.2f}")
    col2.metric("Coeficiente R2", f"{r2:.2f}")
    
    st.markdown("### Gráfico Real vs Predicho")
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.7)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    ax.set_xlabel("Real")
    ax.set_ylabel("Predicho")
    st.pyplot(fig)
    
    db_manager.registrar_metadata("Evaluación", {"mse": mse, "r2": r2})