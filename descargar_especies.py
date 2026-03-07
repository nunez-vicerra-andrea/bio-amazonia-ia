import requests
import os
import time

species = {
    "paiche": "Arapaima gigas",
    "gamitana": "Colossoma macropomum",
    "guacamayo_rojo": "Ara macao",
    "shihuahuaco": "Dipteryx micrantha",
    "mono_choro": "Lagothrix lagotricha"
}

base_path = "bio_amazonia/dataset/train"
headers = {"User-Agent": "BioAmazoniaBot/1.0"}

for folder, name in species.items():
    print(f"Buscando imágenes de: {name}")
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)
    
    # Buscamos archivos multimedia específicamente
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"File:{name}", "gsrlimit": 40, "prop": "imageinfo", "iiprop": "url"
    }
    
    res = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=headers).json()
    
    if "query" in res:
        count = 1
        for page in res["query"]["pages"].values():
            if "imageinfo" in page:
                img_url = page["imageinfo"][0]["url"]
                # Solo bajar si es JPG o PNG real
                if img_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        img_data = requests.get(img_url, timeout=10, headers=headers).content
                        with open(f"{base_path}/{folder}/{folder}_{count}.jpg", "wb") as f:
                            f.write(img_data)
                        print(f"  > Guardada foto {count}")
                        count += 1
                    except:
                        continue
    time.sleep(1)