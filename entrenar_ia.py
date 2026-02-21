import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# 1. Configuración de rutas y parámetros
PATH = "bio_amazonia/dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# 2. Preparar los datos con "Data Augmentation"
# Esto crea variaciones de tus fotos (giros, zoom) para que la IA aprenda mejor
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2 # Usamos el 20% de train para validar
)

train_data = datagen.flow_from_directory(
    f"{PATH}/train",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    f"{PATH}/train",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# 3. Crear el modelo (Transfer Learning)
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False # Congelamos el conocimiento previo de Google

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(5, activation='softmax') # 5 porque tienes 5 especies
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 4. ¡A Entrenar!
print("🚀 Empezando el entrenamiento...")
history = model.fit(train_data, validation_data=val_data, epochs=10)

# 5. Guardar el cerebro de la IA
model.save("models/modelo_amazonia_v1.h5")
print("✅ ¡Modelo guardado en la carpeta models!")