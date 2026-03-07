import requests
import os
import time
import random

especies_wiki = {
    "acuatico_delfin_rosado": "Inia geoffrensis",
    "arbol_caoba": "Swietenia macrophylla",
    "arbol_cedro": "Cedrela odorata",
    "arbol_lupuna": "Ceiba pentandra",
    "ave_aguila_calva": "Haliaeetus leucocephalus",
    "ave_aguila_harpia": "Harpia harpyja",
    "ave_guacamayo_azul": "Anodorhynchus hyacinthinus",
    "ave_shansho": "Opisthocomus hoazin",
    "ave_tucan": "Ramphastos tucanus",
    "gamitana": "Colossoma macropomum",
    "guacamayo_rojo": "Ara macao",
    "mamifero_otorongo": "Panthera onca",
    "mamifero_sajino": "Pecari tajacu",
    "mamifero_tapir": "Tapirus terrestris",
    "mono_choro": "Lagothrix lagotricha",
    "paiche": "Arapaima gigas",
    "pez_boquichico": "Prochilodus nigricans",
    "pez_gamitana": "Colossoma macropomum",
    "pez_paco": "Piaractus brachypomus",
    "planta_achiote": "Bixa orellana",
    "planta_victoria_regia": "Victoria amazonica",
    "reptil_anaconda": "Eunectes murinus",
    "shihuahuaco": "Dipteryx micrantha"
}

base_path = r"C:\Documentos\bio_amazonia\bio_amazonia\dataset\train"
headers = {"User-Agent": "BioAmazoniaBot/2.0 (andrea.nunez@example.com)"}

def descargar_de_wikimedia():
    print("🚀 Iniciando descarga estable desde WIKIMEDIA COMMONS...")
    
    for folder, scientific_name in especies_wiki.items():
        print(f"\n📂 Procesando: {folder} ({scientific_name})...")
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        
        # Contar fotos nuevas existentes
        existing_files = [f for f in os.listdir(path) if f.startswith(f"wiki_{folder}_")]
        start_num = len(existing_files) + 1
        needed = 50 - len(existing_files)
        
        if needed <= 0:
            print(f"  ✅ Ya tienes suficiente material Wiki para {folder}")
            continue

        print(f"  🔍 Buscando {needed} imágenes en Wikimedia...")
        
        # API de Wikimedia Commons
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"File:{scientific_name}",
            "gsrlimit": 60, # Pedimos más por si acaso
            "prop": "imageinfo",
            "iiprop": "url|mime"
        }
        
        try:
            res = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=headers).json()
            if "query" not in res:
                print(f"  ❌ No se encontraron resultados para {scientific_name}")
                continue
                
            count = 0
            pages = res["query"]["pages"].values()
            for page in pages:
                if count >= needed: break
                
                if "imageinfo" in page:
                    img_info = page["imageinfo"][0]
                    img_url = img_info["url"]
                    mime = img_info.get("mime", "")
                    
                    # Solo bajar si es imagen real
                    if not any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png']):
                        continue
                        
                    try:
                        img_data = requests.get(img_url, timeout=10, headers=headers).content
                        ext = "jpg" if "jpeg" in mime or "jpg" in img_url.lower() else "png"
                        
                        filename = f"wiki_{folder}_{start_num + count}.{ext}"
                        with open(os.path.join(path, filename), "wb") as f:
                            f.write(img_data)
                        
                        count += 1
                        print(f"  ✅ Descargada {count}/{needed}", end="\r")
                    except:
                        continue
            
            print(f"\n✨ {folder}: {count} nuevas imágenes de Wikimedia descargadas.")
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ⚠️ Error procesando {folder}: {e}")
            continue

if __name__ == "__main__":
    descargar_de_wikimedia()
