import os

# Nombre del proyecto
project_name = "bio_amazonia"

# Lista de especies (Loreto)
species = [
    "paiche",
    "gamitana",
    "guacamayo_rojo",
    "shihuahuaco",
    "mono_choro"
]

# Crear estructura principal
folders = [
    f"{project_name}/dataset/train",
    f"{project_name}/dataset/test",
    f"{project_name}/models",
    f"{project_name}/app"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Carpeta creada: {folder}")

# Crear carpetas de especies en train y test
for sp in species:
    train_path = f"{project_name}/dataset/train/{sp}"
    test_path = f"{project_name}/dataset/test/{sp}"
    
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)
    
    print(f"Carpetas creadas para especie: {sp}")

# Crear archivo main.py
main_file = f"{project_name}/main.py"

with open(main_file, "w") as f:
    f.write("# Proyecto Bio Amazonia ML\n")
    f.write("print('Sistema Bio Amazonia iniciado correctamente ')\n")

print("\nEstructura completa creada correctamente ")
