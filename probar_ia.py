import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# 1. Cargar el cerebro de la IA
print("Cargando modelo...")
modelo = tf.keras.models.load_model("models/modelo_amazonia_v1.h5")

# TensorFlow ordena las clases alfabéticamente según el nombre de tus carpetas
clases = ['gamitana', 'guacamayo_rojo', 'mono_choro', 'paiche', 'shihuahuaco']

def predecir(ruta_imagen):
    if not os.path.exists(ruta_imagen):
        print(f"❌ Error: No encuentro la imagen en la ruta {ruta_imagen}")
        return

    print(f"\n🔍 Analizando: {ruta_imagen}")
    
    # 2. Preparar la imagen (debe ser de 224x224 igual que en el entrenamiento)
    img = image.load_img(ruta_imagen, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # Añadir una dimensión para el "batch"
    img_array = img_array / 255.0 # Normalizar colores

    # 3. Que la IA haga su predicción
    prediccion = modelo.predict(img_array)
    
    # 4. Traducir los números matemáticos a nuestro idioma
    indice_ganador = np.argmax(prediccion[0])
    confianza = prediccion[0][indice_ganador] * 100
    animal = clases[indice_ganador]

    print(f"✅ ¡Es un(a) {animal.upper()}!")
    print(f"🧠 Seguridad de la IA: {confianza:.2f}%\n")

if __name__ == "__main__":
    # ¡AQUÍ PON LA RUTA DE UNA DE TUS FOTOS DE TEST!
    # Según tus capturas anteriores, tienes fotos como "paiche_7.jpg" en "test/paiche/"
    
    foto_prueba = "bio_amazonia/dataset/test/paiche/paiche_7.jpg" 
    
    predecir(foto_prueba)