import tensorflow as tf
import os

# Ruta donde están tus imágenes
data_dir = "bio_amazonia/dataset/train"

# Cargamos el dataset de entrenamiento
print("Cargando imágenes...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    image_size=(224, 224), # Redimensionamos a un estándar
    batch_size=32
)

# Obtenemos los nombres de las especies (nombres de las carpetas)
class_names = train_ds.class_names
print(f"\nEspecies encontradas: {class_names}")

# Mostramos cuántos 'lotes' de fotos hay
for images, labels in train_ds.take(1):
    print(f"Forma del lote de imágenes: {images.shape}") # Debería ser (32, 224, 224, 3)
    print("¡La IA puede leer las imágenes correctamente!")