from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_cors import CORS
import os
from consultas.consultar import buscar_por_texto, buscar_por_imagen
from consultas.rag import generar_respuesta   # ← la función que arma la narrativa

app = Flask(__name__)
CORS(app)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def texto():
    txt = request.form.get("texto") or request.json.get("texto")
    if not txt:
        # Si es request JSON, devolver JSON para API
        if request.is_json:
            return jsonify({"error": "Texto vacío"}), 400
        # Si es form, mostrar página de error
        return render_template("results.html", 
                             query=txt or "Error",
                             narrativa="Error: Texto vacío. Por favor ingresa una consulta válida.",
                             imagenes=[])

    try:
        resultados = buscar_por_texto(txt)               # lista (nombre, desc)
        nombres   = [n for n, _ in resultados]
        textos    = [d for _, d in resultados]
        narrativa = generar_respuesta(textos, pregunta_usuario=txt)

        # Si es request JSON (para API), devolver JSON
        if request.is_json:
            return jsonify({"imagenes": nombres, "narrativa": narrativa})
        
        # Si es form (desde la interfaz web), renderizar template
        return render_template("results.html",
                             query=txt,
                             narrativa=narrativa,
                             imagenes=nombres)
    
    except Exception as e:
        # Manejo de errores
        error_msg = f"Error al procesar la consulta: {str(e)}"
        if request.is_json:
            return jsonify({"error": error_msg}), 500
        return render_template("results.html",
                             query=txt,
                             narrativa=error_msg,
                             imagenes=[])

@app.route("/upload", methods=["POST"])
def imagen():
    if "image" not in request.files:
        return render_template("results.html",
                             query="Error: Sin imagen",
                             narrativa="Por favor selecciona una imagen válida.",
                             imagenes=[])
    
    archivo = request.files["image"]
    if archivo.filename == '':
        return render_template("results.html",
                             query="Error: Archivo vacío",
                             narrativa="Por favor selecciona una imagen válida.",
                             imagenes=[])

    try:
        # Crear directorio data si no existe
        os.makedirs("data", exist_ok=True)
        
        ruta_temp = os.path.join("data", archivo.filename)
        archivo.save(ruta_temp)

        # 1) Recuperar imágenes + descripciones
        resultados = buscar_por_imagen(ruta_temp)        # ← lista de (nombre, descripcion)

        # 2) Separar nombres y descripciones
        nombres   = [n for n, _ in resultados]
        captions    = [d for _, d in resultados]

        # 3) Generar narrativa con RAG
        #narrativa = generar_respuesta(textos, pregunta_usuario="búsqueda por imagen")
        caption_top1 = captions[0] if captions else ""
        narrativa = generar_respuesta(captions), #pregunta_usuario=caption_top1)

        # Limpiar archivo temporal
        try:
            os.remove(ruta_temp)
        except:
            pass  # No importa si no se puede eliminar

        return render_template("results.html",
                             query=f"Búsqueda por imagen: {archivo.filename}",
                             narrativa=narrativa,
                             imagenes=nombres)
    
    except Exception as e:
        error_msg = f"Error al procesar la imagen: {str(e)}"
        return render_template("results.html",
                             query=f"Error con imagen: {archivo.filename if archivo else 'desconocida'}",
                             narrativa=error_msg,
                             imagenes=[])

@app.route("/media/<path:filename>")
def serve_corpus_image(filename):
    return send_from_directory("corpus", filename)

# Ruta adicional para servir imágenes desde static/uploads si las necesitas
@app.route("/static/uploads/<path:filename>")
def serve_uploaded_image(filename):
    return send_from_directory("static/uploads", filename)

# API endpoints adicionales (mantienen la funcionalidad JSON original)
@app.route("/api/query", methods=["POST"])
def api_texto():
    """Endpoint API que siempre devuelve JSON"""
    txt = request.json.get("texto") if request.is_json else request.form.get("texto")
    if not txt:
        return jsonify({"error": "Texto vacío"}), 400

    try:
        resultados = buscar_por_texto(txt)
        nombres   = [n for n, _ in resultados]
        textos    = [d for _, d in resultados]
        narrativa = generar_respuesta(textos, pregunta_usuario=txt)
        return jsonify({"imagenes": nombres, "narrativa": narrativa})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/upload", methods=["POST"])
def api_imagen():
    """Endpoint API que siempre devuelve JSON"""
    if "image" not in request.files:
        return jsonify({"error": "No se encontró imagen"}), 400
    
    archivo = request.files["image"]
    if archivo.filename == '':
        return jsonify({"error": "Archivo vacío"}), 400

    try:
        os.makedirs("data", exist_ok=True)
        ruta_temp = os.path.join("data", archivo.filename)
        archivo.save(ruta_temp)

        resultados = buscar_por_imagen(ruta_temp)
        nombres   = [n for n, _ in resultados]
        textos    = [d for _, d in resultados]
        narrativa = generar_respuesta(textos, pregunta_usuario="búsqueda por imagen")

        try:
            os.remove(ruta_temp)
        except:
            pass

        return jsonify({"imagenes": nombres, "narrativa": narrativa})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Crear directorios necesarios
    app.run(debug=True)