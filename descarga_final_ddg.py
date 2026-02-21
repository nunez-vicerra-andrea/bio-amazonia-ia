import os
import requests
from duckduckgo_search import DDGS
import time

# Usamos términos en inglés y español para obtener más variedad
especies = {
    "paiche": "Arapaima gigas amazon fish",
    "gamitana": "Colossoma macropomum fish",
    "guacamayo_rojo": "Ara macao scarlet macaw",
    "shihuahuaco": "Dipteryx micrantha tree",
    "mono_choro": "Lagothrix lagotricha yellow-tailed woolly monkey"
}

base_path = "bio_amazonia/dataset/train"

def descargar_imagenes():
    print("🚀 Iniciando descarga de emergencia con DuckDuckGo...")
    
    with DDGS() as ddgs:
        for folder, search_term in especies.items():
            print(f"\nBuscando {folder}...")
            path = os.path.join(base_path, folder)
            os.makedirs(path, exist_ok=True)
            
            # Buscamos 40 imágenes por especie
            results = ddgs.images(search_term, max_results=40)
            
            count = 1
            for res in results:
                try:
                    img_url = res['image']
                    r = requests.get(img_url, timeout=5)
                    if r.status_code == 200:
                        with open(f"{path}/{folder}_{count}.jpg", "wb") as f:
                            f.write(r.content)
                        count += 1
                except:
                    continue
            print(f"✅ {folder}: {count-1} imágenes descargadas.")
            time.sleep(1)

if __name__ == "__main__":
    descargar_imagenes()