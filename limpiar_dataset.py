import os
from PIL import Image

def limpiar_imagenes(directorio_base):
    print(f"🔍 Analizando imágenes en: {directorio_base}")
    eliminadas = 0
    analizadas = 0

    for root, dirs, files in os.walk(directorio_base):
        for file in files:
            ruta_archivo = os.path.join(root, file)
            analizadas += 1
            try:
                with Image.open(ruta_archivo) as img:
                    img.verify() # Verifica que el archivo no esté corrupto
            except Exception:
                print(f"❌ Imagen corrupta eliminada: {ruta_archivo}")
                os.remove(ruta_archivo)
                eliminadas += 1

    print(f"\n✅ Limpieza terminada.")
    print(f"📊 Analizadas: {analizadas}")
    print(f"🗑️ Eliminadas: {eliminadas}")

if __name__ == "__main__":
    # Usamos la ruta que ya confirmamos que funciona
    PATH_TRAIN = r"C:\Documentos\bio_amazonia\bio_amazonia\dataset\train"
    limpiar_imagenes(PATH_TRAIN)