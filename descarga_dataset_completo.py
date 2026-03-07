import os
import requests
from duckduckgo_search import DDGS
import time

especies_amazonicas = {
    "ave_aguila_harpia": "Harpia harpyja eagle",
    "ave_guacamayo_azul": "Anodorhynchus hyacinthinus macaw",
    "ave_shansho": "Opisthocomus hoazin bird",
    "ave_tucan": "Ramphastos toco toucan",
    "pez_boquichico": "Prochilodus nigricans fish",
    "pez_gamitana": "Colossoma macropomum fish",
    "pez_paco": "Piaractus brachypomus fish",
    "pez_paiche": "Arapaima gigas fish",
    "arbol_lupuna": "Ceiba pentandra tree",
    "arbol_shihuahuaco": "Dipteryx micrantha tree",
    "planta_achiote": "Bixa orellana plant",
    "planta_victoria_regia": "Victoria amazonica plant"
}

def generar_dataset():
    print("🚀 Iniciando descarga con modo anti-bloqueo...")
    base_path = "bio_amazonia/dataset/train"
    
    # Usamos DDGS de forma más robusta
    with DDGS() as ddgs:
        for folder, query in especies_amazonicas.items():
            path = os.path.join(base_path, folder)
            
            # Si ya descargamos esta especie, saltamos a la siguiente para no repetir el error
            if os.path.exists(path) and len(os.listdir(path)) > 20:
                print(f"⏩ Saltando {folder} (ya tiene imágenes).")
                continue

            os.makedirs(path, exist_ok=True)
            print(f"📥 Descargando: {folder}...")
            
            try:
                # Bajamos el número a 30 para ser menos "sospechosos"
                results = ddgs.images(query, max_results=30)
                
                headers = {"User-Agent": "BioAmazoniaBot/1.0 (andrea.nunez@example.com)"}
                count = 0
                for i, res in enumerate(results):
                    try:
                        img_data = requests.get(res['image'], timeout=10, headers=headers).content
                        with open(f"{path}/img_{i}.jpg", "wb") as f:
                            f.write(img_data)
                        count += 1
                    except:
                        continue
                
                print(f"✅ Finalizado: {folder} ({count} imágenes)")
                # PAUSA IMPORTANTE: Esperamos 5 segundos entre cada especie
                print("⏳ Esperando un momento para evitar bloqueos...")
                time.sleep(5) 
                
            except Exception as e:
                print(f"⚠️ Error en {folder}: {e}. Pasando a la siguiente...")
                time.sleep(10) # Si hay error, esperamos más tiempo

if __name__ == "__main__":
    generar_dataset()