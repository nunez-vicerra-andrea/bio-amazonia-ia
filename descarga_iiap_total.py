import requests
import os

BASE_URL = "https://api-amazonia.iiap.gob.pe/api/v1"
TRAIN_PATH = "bio_amazonia/dataset/train"

# Nombres clave para buscar en los resultados
objetivos = ["paiche", "gamitana", "macao", "micrantha", "lagothrix"]

def escaneo_profundo_iiap():
    print("Iniciando escaneo profundo en la base de datos del IIAP...")
    
    try:
        # Pedimos una lista grande de especies a la API
        res = requests.get(f"{BASE_URL}/species?page=1&pageSize=200", timeout=20)
        data = res.json()
        
        # Manejamos si la respuesta es lista o diccionario
        especies_lista = data if isinstance(data, list) else data.get('data', [])
        
        count_total = 0
        for sp in especies_lista:
            # Combinamos nombre común y científico para buscar
            identidad = (str(sp.get('commonName')) + " " + str(sp.get('scientificName'))).lower()
            
            for obj in objetivos:
                if obj in identidad:
                    # Intentamos varios campos de imagen que la API podría usar
                    img_url = sp.get('mainImage') or sp.get('image') or sp.get('thumbnail')
                    
                    if img_url:
                        # Mapeo de carpeta
                        folder = "guacamayo_rojo" if "macao" in obj else \
                                 "shihuahuaco" if "micrantha" in obj else \
                                 "mono_choro" if "lagothrix" in obj else obj
                        
                        target_dir = os.path.join(TRAIN_PATH, folder)
                        os.makedirs(target_dir, exist_ok=True)
                        
                        img_data = requests.get(img_url).content
                        with open(f"{target_dir}/{folder}_iiap_oficial.jpg", "wb") as f:
                            f.write(img_data)
                        
                        print(f"✅ ¡ÉXITO! Encontrada imagen para {folder}")
                        count_total += 1

        if count_total == 0:
            print("❌ La API del IIAP no devolvió URLs de imágenes en los campos conocidos.")
            print("Esto a veces pasa por mantenimiento de sus servidores de imágenes.")

    except Exception as e:
        print(f"🔥 Error en la conexión: {e}")

if __name__ == "__main__":
    escaneo_profundo_iiap()