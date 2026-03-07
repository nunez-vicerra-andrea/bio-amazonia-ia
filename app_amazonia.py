import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import base64
import json

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="BioAmazonía v2", page_icon="🌳", layout="centered")

# --- FUNCIONES DE CARGA ---

def get_base64(bin_file):
    """Convierte imagen local a base64 para el fondo CSS"""
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def cargar_info_json():
    """Carga la base de datos de especies desde la subcarpeta correcta"""
    # Ajustamos la ruta a la subcarpeta que indicaste
    ruta_json = os.path.join("bio_amazonia", "especies.json")
    if os.path.exists(ruta_json):
        with open(ruta_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f"❌ No se encontró el archivo: {ruta_json}")
        return {}

# --- CARGA DE RECURSOS ---
# Intentamos cargar desde la subcarpeta
path_fondo = os.path.join("bio_amazonia", "fondo.jpg")
INFO_ESPECIES = cargar_info_json()
clases = sorted(list(INFO_ESPECIES.keys())) if INFO_ESPECIES else []

bin_str = get_base64(path_fondo)
if bin_str:
    fondo_css = f"""
    <style>
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.15)), 
                      url("data:image/jpg;base64,{bin_str}");
    background-size: 100% 100%;
    background-position: center;
}}
</style>
"""
else:
    fondo_css = "<style>.stApp { background-color: #e8f5e9; }</style>"

# 2. DISEÑO CSS (Glassmorphism y Botón Marrón)
st.markdown(fondo_css, unsafe_allow_html=True)
st.markdown("""
    <style>
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.93);
        padding: 45px;
        border-radius: 25px;
        margin-top: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        backdrop-filter: blur(8px);
    }
    .titulo-principal {
        color: #1b5e20;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        line-height: 1.1;
    }
    div.stButton > button {
        background-color: #a0522d !important;
        color: white !important;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        width: 100%;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MODELO IA
@st.cache_resource
def load_model_ia():
    path = os.path.join("models", "modelo_amazonia_v2.h5")
    return tf.keras.models.load_model(path) if os.path.exists(path) else None

model = load_model_ia()

# --- INTERFAZ ---
st.markdown('<div class="titulo-principal">🌳 Explorador Inteligente:<br>BioAmazonía v2</div>', unsafe_allow_html=True)
st.write("<center><b>Sistema de Identificación con IA</b></center>", unsafe_allow_html=True)

archivo = st.file_uploader("", type=["jpg", "png", "jpeg"])

if archivo and model and INFO_ESPECIES:
    col_img, col_res = st.columns([1, 1], gap="large")
    
    with col_img:
        img = Image.open(archivo)
        st.image(img, use_container_width=True)
    
    with col_res:
        img_res = img.resize((224, 224))
        img_arr = np.array(img_res)
        if img_arr.shape[-1] == 4: img_arr = img_arr[:,:,:3]
        img_arr = np.expand_dims(img_arr / 255.0, axis=0)
        
        res = model.predict(img_arr)
        idx = np.argmax(res[0])
        conf = res[0][idx] * 100
        
        tag = clases[idx]
        info = INFO_ESPECIES.get(tag, {"comun": tag, "latn": "N/A", "nota": ""})

        if conf > 75: # Filtro de seguridad
            st.success(f"### {info['comun'].upper()}")
            st.markdown(f"🔬 *Nombre científico:* **{info['latn']}**")
            st.info(f"💡 {info['nota']}")
            st.write(f"Confianza: **{conf:.2f}%**")
        else:
            st.warning("⚠️ **IDENTIFICACIÓN INCIERTA**")
            st.write(f"Parece un: {info['comun']}")

st.markdown("<br><hr><center><small>🌿 Proyecto BioAmazonía 2026</small></center>", unsafe_allow_html=True)