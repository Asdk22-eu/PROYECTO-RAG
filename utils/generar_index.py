# utils/generar_index.py

import os
import pandas as pd
import torch
import faiss
import pickle
import numpy as np
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel

# === CONFIGURACIÓN DE RUTAS ===
ruta_csv = "D:\\2025A\\RI\\RAG MULTIMODAL\\data\\descripciones.csv"
ruta_corpus = "D:\\2025A\\RI\\RAG MULTIMODAL\\corpus"
ruta_salida = "D:\\2025A\\RI\\RAG MULTIMODAL\\embeddings"
os.makedirs(ruta_salida, exist_ok=True)

# === Cargar modelo CLIP ===
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# === Leer descripciones ===
df = pd.read_csv(ruta_csv)

image_embeddings = []
metadata = []

print("🔄 Generando embeddings de imágenes...")

for _, row in tqdm(df.iterrows(), total=len(df)):
    filename = row["filename"]
    description = row["description"]
    image_path = os.path.join(ruta_corpus, filename)

    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
        embedding = outputs.cpu().numpy().flatten()
        image_embeddings.append(embedding)
        metadata.append((filename, description))
    except Exception as e:
        print(f" Error con {filename}: {e}")

# === Construir índice FAISS ===
embedding_matrix = np.array(image_embeddings).astype("float32")
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

# === Guardar índice y metadatos ===
faiss.write_index(index, os.path.join(ruta_salida, "image_index.faiss"))
with open(os.path.join(ruta_salida, "mapping.pkl"), "wb") as f:
    pickle.dump(metadata, f)

print(" ¡Índice generado y guardado exitosamente!")