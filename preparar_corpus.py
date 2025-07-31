# preparar_corpus.py

import os
import pandas as pd

ruta_captions = "D:\\2025A\\RI\\RAG MULTIMODAL\\data\\captions.txt"
ruta_imagenes = "D:\\2025A\\RI\\RAG MULTIMODAL\\data\\Images"
output_csv = "D:\\2025A\\RI\\RAG MULTIMODAL\\data\\descripciones.csv"
output_folder = "D:\\2025A\\RI\\RAG MULTIMODAL\\corpus"
os.makedirs("data", exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Leer y procesar captions
pares = []
usadas = set()

with open(ruta_captions, "r", encoding="utf-8") as f:
    next(f)  # saltar cabecera
    for linea in f:
        nombre, descripcion = linea.strip().split(",", 1)
        if nombre not in usadas:
            usadas.add(nombre)
            pares.append((nombre, descripcion))
        if len(pares) == 1000:
            break

# Guardar CSV
df = pd.DataFrame(pares, columns=["filename", "description"])
df.to_csv(output_csv, index=False)

# Copiar imágenes seleccionadas a /corpus
import shutil

for nombre in df["filename"]:
    origen = os.path.join(ruta_imagenes, nombre)
    destino = os.path.join(output_folder, nombre)
    if os.path.exists(origen):
        shutil.copy(origen, destino)

print(f"✅ Corpus reducido creado con {len(df)} pares en '{output_csv}' y carpeta 'corpus/'")
