from flask import Flask, jsonify, request, render_template_string, send_file
from PIL import Image
from pathlib import Path
import io
import zipfile

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "index.html"


@app.route("/")
def home():
    if not INDEX_PATH.exists():
        return "No se encontro index.html", 404
    return render_template_string(INDEX_PATH.read_text(encoding="utf-8"))


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/convertir", methods=["POST", "OPTIONS"])
def convertir_imagenes():
    if request.method == "OPTIONS":
        return ("", 204)

    imagenes = request.files.getlist("imagenes")

    if not imagenes:
        return jsonify({"message": "No se encontraron imagenes para convertir"}), 400

    try:
        quality = int(request.form.get("quality", 80))
    except ValueError:
        return jsonify({"message": "El valor de calidad no es valido"}), 400

    quality = max(1, min(100, quality))
    zip_buffer = io.BytesIO()

    try:
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for archivo in imagenes:
                nombre_original = Path(archivo.filename).stem or "imagen"
                nombre_webp = f"{nombre_original}.webp"

                imagen = Image.open(archivo.stream)
                if imagen.mode in ("RGBA", "P"):
                    imagen = imagen.convert("RGBA")
                else:
                    imagen = imagen.convert("RGB")

                salida = io.BytesIO()
                imagen.save(salida, format="WEBP", quality=quality, optimize=True, method=6)
                salida.seek(0)
                zip_file.writestr(nombre_webp, salida.read())
    except Exception as exc:
        return jsonify({"message": f"Error al convertir imagenes: {exc}"}), 500

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="imagenes_convertidas_webp.zip",
        mimetype="application/zip",
    )


if __name__ == "__main__":
    app.run(debug=True)
