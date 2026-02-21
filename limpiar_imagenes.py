import os
import PIL
from PIL import Image

data_dir = "bio_amazonia/dataset/train"
especies = ['gamitana', 'guacamayo_rojo', 'mono_choro', 'paiche', 'shihuahuaco']

print("Iniciando limpieza de imágenes...")

for especie in especies:
    folder_path = os.path.join(data_dir, especie)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            img = Image.open(file_path) # Intentar abrir
            img.verify() # Verificar que no esté corrupta
        except (IOError, SyntaxError) as e:
            print(f"Borrando archivo corrupto: {file_path}")
            os.remove(file_path)

print("¡Limpieza terminada! Vuelve a ejecutar verificar_ia.py")