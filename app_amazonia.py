import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# 1. Configuración de la interfaz (Esto debe ir primero)
st.set_page_config(page_title="IA Amazonía", page_icon="🌳", layout="centered")

st.title("🌳 Clasificador de Especies Amazónicas")
st.markdown("""
Esta IA ha sido entrenada para identificar 5 especies clave de la Amazonía.
**Paiche, Gamitana, Guacamayo Rojo, Shihuahuaco y Mono Choro.**
""")

# 2. Función para cargar el modelo con manejo de errores
@st.cache_resource
def cargar_modelo():
    modelo_path = "models/modelo_amazonia_v1.h5"
    if not os.path.exists(modelo_path):
        st.error(f"❌ No se encontró el modelo en {modelo_path}. ¡Asegúrate de haber corrido entrenar_ia.py primero!")
        return None
    return tf.keras.models.load_model(modelo_path)

# Intentar cargar el modelo
model = cargar_modelo()
clases = ['Gamitana', 'Guacamayo Rojo', 'Mono Choro', 'Paiche', 'Shihuahuaco']

# 3. Interfaz de subida de archivos
st.write("---")
archivo_subido = st.file_uploader("📤 Sube una foto del animal o planta", type=["jpg", "jpeg", "png"])

if archivo_subido is not None and model is not None:
    # Crear dos columnas para mostrar imagen y resultado
    col1, col2 = st.columns(2)

    with col1:
        imagen = Image.open(archivo_subido)
        st.image(imagen, caption='Imagen seleccionada', use_container_width=True)

    with col2:
        st.write("### 🧠 Procesando...")
        
        # Preprocesamiento de la imagen
        img = imagen.resize((224, 224))
        img_array = np.array(img)
        
        # Corregir si la imagen tiene canal Alfa (PNGs transparentes)
        if img_array.shape[-1] == 4:
            img_array = img_array[:, :, :3]
            
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        # Realizar la predicción
        prediccion = model.predict(img_array)
        indice = np.argmax(prediccion[0])
        confianza = prediccion[0][indice] * 100
        resultado = clases[indice]

        # Mostrar resultado con colores según confianza
        st.write(f"La IA cree que es:")
        if confianza > 70:
            st.success(f"## **{resultado.upper()}**")
        else:
            st.warning(f"## **{resultado.upper()}**")
            
        st.metric(label="Nivel de Confianza", value=f"{confianza:.2f}%")

st.write("---")
st.caption("Desarrollado con TensorFlow y Streamlit - Proyecto Bio Amazonía")