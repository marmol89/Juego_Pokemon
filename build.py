import os
import sys
import subprocess
import platform

def build():
    print(f"--- Iniciando construcción para {platform.system()} ---")
    
    # Nombre del ejecutable
    output_name = "JuegoPokemon"
    
    # Archivo principal
    main_script = "app.py"
    
    # Comando base de PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        f"--name={output_name}",
        "--clean",
        main_script
    ]
    
    # En Windows, PyInstaller suele necesitar extension .exe (se añade sola)
    # No ocultamos la consola (--noconsole) porque el juego es de terminal
    
    try:
        print(f"Ejecutando: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print(f"¡CONSTRUCCIÓN COMPLETADA CON ÉXITO!")
        print(f"El archivo se encuentra en la carpeta: {os.path.join(os.getcwd(), 'dist')}")
        print("="*50)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error durante la construcción: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n[!] Error: PyInstaller no encontrado. Asegúrate de haber ejecutado 'pip install -r requirements.txt'")
        sys.exit(1)

if __name__ == "__main__":
    build()
