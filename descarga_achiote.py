import os
import requests
from duckduckgo_search import DDGS
import time

def descargar_achiote():
    path = "bio_amazonia/dataset/train/planta_achiote"
    os.makedirs(path, exist_ok=True)
    
    print("🌿 Buscando imágenes de Achiote (Bixa orellana)...")
    
    with DDGS() as ddgs:
        try:
            # Pedimos solo 25 imágenes para no levantar sospechas
            results = ddgs.images("Bixa orellana plant achiote amazon", max_results=25)
            
            headers = {"User-Agent": "BioAmazoniaBot/1.0 (andrea.nunez@example.com)"}
            count = 0
            for i, res in enumerate(results):
                try:
                    img_data = requests.get(res['image'], timeout=10, headers=headers).content
                    with open(f"{path}/achiote_{i}.jpg", "wb") as f:
                        f.write(img_data)
                    count += 1
                    print(f"✅ Imagen {count} descargada")
                    time.sleep(1) # Un segundo entre fotos
                except:
                    continue
            print(f"✨ ¡Listo! Se descargaron {count} imágenes de Achiote.")
        except Exception as e:
            print(f"❌ El bloqueo persiste: {e}")
            print("💡 Sugerencia: Descarga 15 fotos de Google Imágenes y ponlas en la carpeta.")

if __name__ == "__main__":
    descargar_achiote()