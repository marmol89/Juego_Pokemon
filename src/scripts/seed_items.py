import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: No se han encontrado las credenciales de Supabase en el archivo .env")
    exit()

supabase = create_client(url, key)

def seed_items():
    print("Insertando objetos en la tienda...")
    
    items_to_insert = [
        {"nombre": "Poción", "descripcion": "Restaura 50 HP de un Pokémon", "precio": 100, "efecto": {"cura": 50}},
        {"nombre": "Superpoción", "descripcion": "Restaura 100 HP de un Pokémon", "precio": 250, "efecto": {"cura": 100}},
        {"nombre": "Restaurar Todo", "descripcion": "Cura toda la vida del Pokémon", "precio": 600, "efecto": {"cura": 999}}
    ]
    
    try:
        # Primero limpiamos por si acaso
        # supabase.table("items").delete().neq("id", 0).execute()
        
        # Insertamos
        data = supabase.table("items").insert(items_to_insert).execute()
        print(f"✅ ¡Éxito! Se han insertado {len(data.data)} objetos.")
    except Exception as e:
        print(f"❌ Error al insertar objetos: {e}")

if __name__ == "__main__":
    seed_items()
