import os
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO

def descargar_imagenes(animal, carpeta_destino, cantidad=60):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    print(f"🔍 Buscando fotos de: {animal}...")
    
    with DDGS() as ddgs:
        # Añadimos "photo" y "nature" para evitar dibujos animados
        keywords = f"{animal} amazon nature photo"
        busqueda = ddgs.images(keywords, max_results=cantidad)
        
        headers = {"User-Agent": "BioAmazoniaBot/1.0 (andrea.nunez@example.com)"}
        count = 0
        for i, res in enumerate(busqueda):
            try:
                url = res['image']
                response = requests.get(url, timeout=10, headers=headers)
                img = Image.open(BytesIO(response.content))
                
                # Convertir a RGB (evita errores con PNGs o formatos raros)
                img = img.convert('RGB')
                
                nombre_archivo = f"{animal.replace(' ', '_')}_{count}.jpg"
                img.save(os.path.join(carpeta_destino, nombre_archivo), "JPEG")
                
                count += 1
                if count % 10 == 0:
                    print(f"✅ {count} imágenes guardadas...")
                    
            except Exception:
                continue # Si una imagen falla, pasa a la siguiente

    print(f"✨ ¡Listo! Se descargaron {count} fotos en {carpeta_destino}\n")

# --- CONFIGURACIÓN DE LAS NUEVAS ESPECIES ---
base_path = r"C:\Documentos\bio_amazonia\bio_amazonia\dataset\train"

nuevos_animales = {
    "Otorongo": "mamifero_otorongo",
    "Sajino": "mamifero_sajino",
    "Tapir": "mamifero_tapir",
    "Anaconda": "reptil_anaconda",
    "Delfin Rosado": "acuatico_delfin_rosado"
}

for nombre_busqueda, nombre_carpeta in nuevos_animales.items():
    ruta = os.path.join(base_path, nombre_carpeta)
    descargar_imagenes(nombre_busqueda, ruta, cantidad=50) # Bajamos 80 de cada uno