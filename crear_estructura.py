import os

# Nombre del proyecto
project_name = "bio_amazonia"

# Estructura de carpetas
folders = [
    f"{project_name}/dataset/train",
    f"{project_name}/dataset/test",
    f"{project_name}/models",
    f"{project_name}/app"
]

# Crear carpetas
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Carpeta creada: {folder}")

# Crear archivo principal
main_file = f"{project_name}/main.py"

with open(main_file, "w") as f:
    f.write("# Proyecto Bio Amazonia ML\n")
    f.write("print('Proyecto Bio Amazonia iniciado correctamente')\n")

print("\nEstructura del proyecto creada correctamente 🌿")
