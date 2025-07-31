# mini_rag.py
from openai import OpenAI
import os

# Usa tu clave de OpenAI (o desde variable de entorno)
#openai.api_key = os.getenv("OPENAI_API_KEY") or "TU_API_KEY_AQUI"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def generar_respuesta(descripciones, pregunta_usuario: str | None = ""):
    """
    ▸ Si pregunta_usuario es texto real ("caballo"), primero lo define.
    ▸ Si está vacío o es un nombre .jpg/.png, solo describe las imágenes.
    """
    contexto = "\n".join(descripciones)

    # ---- ¿debemos definir? ----
    definir = bool(pregunta_usuario) \
        and not pregunta_usuario.lower().startswith("búsqueda por imagen") \
        and not pregunta_usuario.lower().endswith((".jpg", ".jpeg", ".png"))

    bloque_definicion = (f"Primero da una **definición concisa** de \"{pregunta_usuario}\".\n"
                         if definir else "")

    prompt = f"""
Eres un asistente de búsqueda multimodal.
{bloque_definicion}
Luego describe de forma narrativa (máx. 3 párrafos) lo que muestran las imágenes recuperadas y por qué son relevantes.

=== Contexto recuperado (captions) ===
{contexto}
"""

    

    try:
        rsp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Responde SIEMPRE en español, claro y narrativo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=350
        )
        return rsp.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error al generar respuesta: {e}"