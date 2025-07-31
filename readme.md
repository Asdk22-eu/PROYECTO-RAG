#  RAG Multimodal: Recuperación y Generación a partir de Texto o Imagen

Este proyecto implementa un sistema **RAG Multimodal** que permite realizar consultas por texto o imagen y genera una respuesta narrativa basada en resultados recuperados de un corpus imagen-texto (Flickr8k).



##  Funcionalidades principales

 *Codificación e indexación del corpus con CLIP  
 *Indexación con FAISS para búsqueda eficiente  
 *Consulta por texto o por imagen  
 *Recuperación de imágenes y descripciones similares  
 *Generación de respuesta usando modelo de lenguaje (OpenAI GPT)  
 *Interfaz web amigable con Flask  

##  Requisitos

- Python 3.10 o superior  
- Entorno virtual recomendado  
- Acceso a la API de OpenAI
- -Corpus


##  Instalación y Ejecución

1. Clonar el repositorio.
2. Descargar el corpus de flickr 8k, evidentemente por lo grande que és no se puede subir a github, ni tampoco el corpus de 1000 imágenes.
3. Recrear el entorno virtual: python -m venv .venv
.venv\Scripts\activate
4. Instalar todas las dependencias, para esto se ha descrito en requirements.txt todo lo necesario
 pip install -r requirements.txt
5. Cambiar la API KEY en rag.py línea  número #8.
6. Ejecutar /consultas/rag.py
7. Ejecutar /consultas/consultar.py
8. Ejecutar python app.py 
  $env:KMP_DUPLICATE_LIB_OK="TRUE"   # para evitar conflicto FAISS + Torch
 python app.py
  Abrir el navegador en: http://localhost:5000
