import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# 1. Configuración de rutas y parámetros
PATH = r"C:\Documentos\bio_amazonia\bio_amazonia\dataset\train"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS_PHASE1 = 10
EPOCHS_PHASE2 = 20

# 2. Preprocesamiento de imágenes (Aumento de datos robusto)
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    brightness_range=[0.8, 1.2]
)

# 3. Carga de datos
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

num_clases = len(train_data.class_indices)
print(f"✅ Se detectaron {num_clases} especies.")

# 4. Crear el Modelo (Transfer Learning con EfficientNetV2B0)
# EfficientNetV2 es más moderno y potente que MobileNetV2
base_model = tf.keras.applications.EfficientNetV2B0(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_clases, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Callbacks para mejorar el entrenamiento
early_stopping = callbacks.EarlyStopping(patience=5, restore_best_weights=True)
reduce_lr = callbacks.ReduceLROnPlateau(factor=0.2, patience=3)
checkpoint = callbacks.ModelCheckpoint('models/mejor_modelo_v3.keras', save_best_only=True)

# 5. Fase 1: Entrenamiento de la cabeza (Transfer Learning)
print("🚀 [Fase 1] Entrenando la cabeza del modelo...")
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_PHASE1,
    callbacks=[early_stopping, reduce_lr, checkpoint]
)

# 6. Fase 2: Ajuste Fino (Fine-tuning)
print("🔧 [Fase 2] Desbloqueando capas para ajuste fino...")
base_model.trainable = True
# Descongelamos solo las últimas 20 capas para no destruir lo aprendido
for layer in base_model.layers[:-20]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), # Tasa muy baja
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("🚀 [Fase 2] Iniciando Fine-tuning...")
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_PHASE2,
    callbacks=[early_stopping, reduce_lr, checkpoint]
)

# 7. Guardar el modelo final
os.makedirs("models", exist_ok=True)
model.save("models/modelo_amazonia_v3.h5")
print("⭐ ¡Modelo v3 (MEJORADO) guardado con éxito!")
