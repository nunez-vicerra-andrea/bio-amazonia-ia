import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# 1. Configuración de rutas y parámetros
# Cambia la línea 7 por esta:
PATH = r"C:\Documentos\bio_amazonia\bio_amazonia\dataset\train"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# 2. Preprocesamiento de imágenes (Aumento de datos)
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2, # 20% para probar que aprendió bien
    rotation_range=20,
    horizontal_flip=True
)

# 3. Carga automática de todas las carpetas
train_data = datagen.flow_from_directory(
    PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Detectamos el número de especies automáticamente
num_clases = len(train_data.class_indices)
print(f"✅ Se detectaron {num_clases} especies: {list(train_data.class_indices.keys())}")

# 4. Crear el Modelo (Transfer Learning con MobileNetV2)
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False # Usamos el conocimiento previo de Google

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(num_clases, activation='softmax') # Se ajusta a tus nuevas carpetas
])

model.compile(optimizer='adam', 
loss='categorical_crossentropy' if num_clases > 2 else 'binary_crossentropy', 
metrics=['accuracy'])
# Nota: Si te da error 'categorical_with_crossentropy' cámbialo a 'categorical_crossentropy'

# 5. ¡A entrenar!
print("🚀 Iniciando entrenamiento del Cerebro Amazónico v2...")
model.fit(train_data, validation_data=val_data, epochs=10)

# 6. Guardar el nuevo modelo
os.makedirs("models", exist_ok=True)
model.save("models/modelo_amazonia_v2.h5")
print("⭐ ¡Modelo v2 guardado con éxito en la carpeta models!")