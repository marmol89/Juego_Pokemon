from src.database.db import db
import time
import os

dbp = db().get_connection()

def borrarTablas():
    if not dbp:
        print("Error: No se pudo conectar a Supabase.")
        return
        
    try:
        # El orden es importante por las claves foráneas
        dbp.table("user_items").delete().gte("id", 0).execute()
        dbp.table("items").delete().gte("id", 0).execute()
        dbp.table("movements").delete().gte("id", 0).execute()
        dbp.table("battles").delete().gte("id", 0).execute()
        dbp.table("teams").delete().gte("id", 0).execute()
        dbp.table("rooms").delete().gte("id", 0).execute()
        dbp.table("pokemons").delete().gte("id", 0).execute()
        dbp.table("users").delete().gte("id", 0).execute()
        print("✅ Base de datos vaciada correctamente.")
    except Exception as e:
        print("\n❌ Error borrando tablas:", e)

def borrarSalas():
    if not dbp: return
    try:
        dbp.table("movements").delete().gte("id", 0).execute()
        dbp.table("battles").delete().gte("id", 0).execute()
        dbp.table("teams").delete().gte("id", 0).execute()
        dbp.table("rooms").delete().gte("id", 0).execute()
        print("✅ Salas e historiales de batalla borrados.")
    except Exception as e:
        print("❌ Error borrando salas:", e)

print("="*50)
print(f"{'GESTOR DE BASE DE DATOS POKÉMON':^50}")
print("="*50)
print("  [1] Reset Total (Borrar todo y re-sembrar Pokémones/Tienda)")
print("  [2] Limpiar Salas (Borrar partidas activas)")
print("  [0] Salir")
print("="*50)

from src.utils.visuals import get_key
opcion = get_key()

if opcion == "1":
    borrarTablas()
    
    print("\n[+] Iniciando carga de datos...")
    # Importar y ejecutar seeders
    try:
        from src.scripts.seed_pokemons import main as seed_pokemons
        seed_pokemons()
        from src.scripts.seed_items import seed_items
        seed_items()
        print("\n✅ ¡Inicialización completa!")
    except Exception as e:
        print(f"\n❌ Error durante la siembra de datos: {e}")

elif opcion == "2":
    borrarSalas()
elif opcion == "0":
    print("Saliendo...")
else:
    print("Opción no válida.")