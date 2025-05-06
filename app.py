from flask import Flask, jsonify, request
from PIL import Image
import os

app = Flask(__name__)

@app.route('/convertir', methods=['POST'])
def convertir_imagen():
    # Asegúrate de que el archivo esté en la solicitud
    if 'imagen' not in request.files:
        return jsonify({'message': 'No se encontró ninguna imagen'}), 400

    imagen = request.files['imagen']  # Obtén la imagen enviada por el frontend
    try:
        # Abre la imagen con Pillow
        img = Image.open(imagen)
        output_filename = 'output.webp'
        img.save(output_filename, 'WEBP')  # Guardar la imagen en formato WEBP
        return jsonify({'message': 'Imagen convertida correctamente', 'output': output_filename}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
