# consultar.py

import os
import faiss
import torch
import pickle
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Rutas
ruta_index = "D:\\2025A\\RI\\RAG MULTIMODAL\\embeddings\\image_index.faiss"
ruta_mapping = "D:\\2025A\\RI\\RAG MULTIMODAL\\embeddings\\mapping.pkl"
ruta_corpus = "D:\\2025A\\RI\\RAG MULTIMODAL\\corpus"

# Cargar modelo
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Cargar índice y metadatos
index = faiss.read_index(ruta_index)
with open(ruta_mapping, "rb") as f:
    metadata = pickle.load(f)

# Función para búsqueda por texto
def buscar_por_texto(texto, k=5):
    inputs = processor(text=[texto], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        embedding = model.get_text_features(**inputs).cpu().numpy().astype("float32")
    D, I = index.search(embedding, k)
    resultados = [metadata[i] for i in I[0]]
    return resultados

# Función para búsqueda por imagen
def buscar_por_imagen(path_imagen, k=5):
    image = Image.open(path_imagen).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs).cpu().numpy().astype("float32")
    D, I = index.search(embedding, k)
    resultados = [metadata[i] for i in I[0]]
    return resultados

# ==========================
# EJEMPLOS DE PRUEBA
# ==========================

# Buscar por texto
print("🔍 Búsqueda por texto:")
texto = "A girl in a red dress walking on the beach"
res = buscar_por_texto(texto)
for nombre, desc in res:
    print(f"- {nombre} → {desc}")

# Buscar por imagen (modifica la ruta con una de tu corpus)
print("\n🔍 Búsqueda por imagen:")
ruta_imagen = os.path.join(ruta_corpus, "12830823_87d2654e31.jpg")  # ejemplo real
res = buscar_por_imagen(ruta_imagen)
for nombre, desc in res:
    print(f"- {nombre} → {desc}")
    
from consultas.rag import generar_respuesta

descripciones = [desc for _, desc in res]
texto_usuario = "Una niña caminando por la playa"
#texto_traducido = traducir_es_a_en(texto_usuario)

#res = buscar_por_texto(texto_traducido)
for nombre, desc in res:
    print(f"- {nombre} → {desc}")

# Generar narrativa
descripciones = [desc for _, desc in res]
narrativa = generar_respuesta(descripciones, pregunta_usuario=texto_usuario)
print("\n📝 Narrativa generada:")
print(narrativa)

