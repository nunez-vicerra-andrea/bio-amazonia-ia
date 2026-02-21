import os
import random
import shutil

# Configuración de rutas
base_path = "bio_amazonia/dataset"
train_path = os.path.join(base_path, "train")
test_path = os.path.join(base_path, "test")

# Porcentaje de imágenes para test (20%)
split_percent = 0.2

for category in os.listdir(train_path):
    train_category_dir = os.path.join(train_path, category)
    test_category_dir = os.path.join(test_path, category)
    
    # Asegurarse de que sea una carpeta y crear la de test si no existe
    if os.path.isdir(train_category_dir):
        os.makedirs(test_category_dir, exist_ok=True)
        
        # Obtener lista de imágenes
        images = os.listdir(train_category_dir)
        # Mezclarlas para que la selección sea aleatoria
        random.shuffle(images)
        
        # Calcular cuántas mover
        num_test = int(len(images) * split_percent)
        images_to_move = images[:num_test]
        
        for img in images_to_move:
            src = os.path.join(train_category_dir, img)
            dst = os.path.join(test_category_dir, img)
            shutil.move(src, dst)
            
        print(f"✅ {category}: Movidas {num_test} imágenes a test.")

print("\n¡Distribución completada!")