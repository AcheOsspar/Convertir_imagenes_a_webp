from PIL import Image  # Importa la librería Pillow para trabajar con imágenes
import tkinter as tk  # Importa tkinter para la GUI
from tkinter import filedialog  # Importa filedialog para seleccionar el archivo

def convertir_a_webp(imagen_jpeg):
    try:
        # Abrir la imagen en formato JPEG
        imagen = Image.open(imagen_jpeg)

        # Definir el nombre del archivo de salida (con formato .webp)
        nombre_salida = imagen_jpeg.split('.')[0] + '.webp'

        # Convertir la imagen a WEBP y guardarla
        imagen.save(nombre_salida, 'WEBP')
        print(f"Imagen convertida y guardada como {nombre_salida}")
    except Exception as e:
        print(f"Error al convertir la imagen: {e}")

# Función para seleccionar el archivo de imagen
def seleccionar_imagen():
    # Crear una ventana de Tkinter (no se mostrará)
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    # Abrir el cuadro de diálogo para seleccionar un archivo
    archivo_imagen = filedialog.askopenfilename(
        title="Selecciona una imagen JPEG",  # Título del cuadro de diálogo
        filetypes=[("Archivos JPEG", "*.jpg;*.jpeg"), ("Todos los archivos", "*.*")]
    )

    return archivo_imagen

# Función para convertir varias imágenes
def convertir_varias_imagenes():
    # Mensaje de bienvenida al programa
    print("Bienvenido al programa para convertir imágenes a WebP.")
    
    # Preguntar si el usuario quiere comenzar la conversión
    empezar = input("¿Quieres comenzar la conversión? (si/no): ").strip().lower()

    if empezar != "si":
        print("¡No hay problema! ¡Hasta la próxima!")
        return

    while True:
        # Seleccionar la imagen a convertir
        imagen_jpeg = seleccionar_imagen()

        if imagen_jpeg:
            # Convertir la imagen seleccionada
            convertir_a_webp(imagen_jpeg)
        else:
            print("No se seleccionó ningún archivo.")

        # Preguntar al usuario si quiere convertir otra imagen
        respuesta = input("¿Quieres convertir otra imagen? (si/no): ").strip().lower()
        if respuesta != "si":
            print("Gracias por usar el convertidor. ¡Sigue programando y feliz día!")
            break

# Llamar a la función para convertir varias imágenes
convertir_varias_imagenes()
