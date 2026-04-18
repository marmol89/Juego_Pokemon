from PIL import Image
import os

def convert():
    input_png = "icon.png"
    if not os.path.exists(input_png):
        print("Error: icon.png no encontrado.")
        return

    img = Image.open(input_png)
    
    # Generar ICO (Windows)
    print("Generando icon.ico...")
    img.save("icon.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
    
    # Generar ICNS (Mac) - Solo si el sistema lo soporta o mediante emulación básica
    try:
        print("Generando icon.icns...")
        img.save("icon.icns", format="ICNS")
    except Exception as e:
        print(f"Nota: No se pudo generar .icns directamente (omitido): {e}")

    print("Conversión completada.")

if __name__ == "__main__":
    convert()
