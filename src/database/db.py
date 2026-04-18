import os
import sys
import time
from dotenv import load_dotenv
from supabase import create_client, Client

# Soporte para ejecutables (PyInstaller)
if getattr(sys, 'frozen', False):
    # Si es un ejecutable, el .env puede estar empaquetado
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    load_dotenv(os.path.join(bundle_dir, '.env'))

# También cargamos del directorio actual por si hay uno externo (sobrescribe lo anterior)
load_dotenv()

class db:

    _client = None

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            print("\n" + "!"*50)
            print("  CONFIGURACIÓN DE SUPABASE FALTANTE")
            print("!"*50)
            print("  No se ha encontrado el archivo .env o las claves.")
            print("  Por favor, introduce tus credenciales:")
            url = input("  > SUPABASE_URL: ").strip()
            key = input("  > SUPABASE_KEY: ").strip()
            
            if url and key:
                with open(".env", "w") as f:
                    f.write(f"SUPABASE_URL={url}\n")
                    f.write(f"SUPABASE_KEY={key}\n")
                print("\n  [+] Configuración guardada en .env")
                time.sleep(1.5)
            else:
                print("\n  [!] Error: Las credenciales no pueden estar vacías.")
                time.sleep(2)
                return

        if url and key:
            self._client = create_client(url, key)
        
    def get_connection(self) -> Client:
        return self._client
    
    def close(self):
        pass