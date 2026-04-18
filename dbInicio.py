from src.database.db import db
import time

dbp = db().get_connection()

def borrarTablas():
    # En Supabase no podemos ejecutar "DROP TABLE" y "CREATE TABLE" puramente
    # a través de la API básica, ya que esta previene la destrucción de esquemas en producción.
    # Por tanto, vaciamos todas las tablas en lugar de destruirlas y rehacerlas.
    
    if not dbp:
        print("Error: No se pudo conectar a Supabase.")
        return
        
    try:
        dbp.table("movements").delete().gte("id", 0).execute()
        dbp.table("battles").delete().gte("id", 0).execute()
        dbp.table("teams").delete().gte("id", 0).execute()
        dbp.table("rooms").delete().gte("id", 0).execute()
        dbp.table("pokemons").delete().gte("id", 0).execute()
        dbp.table("users").delete().gte("id", 0).execute()
        print("Datos de todas las tablas borrados correctamente.")
    except Exception as e:
        print("\nError borrando tablas.")
        print("¿Asegúrate de que ya has creado las tablas vacías en el Editor SQL de Supabase copiando el código de supabase_schema.sql como indicaban las instrucciones de antes?\n\nDetalles del error:", e)

def borrarSalas():
    if not dbp:
        return
        
    try:
        dbp.table("movements").delete().gte("id", 0).execute()
        dbp.table("battles").delete().gte("id", 0).execute()
        dbp.table("teams").delete().gte("id", 0).execute()
        dbp.table("rooms").delete().gte("id", 0).execute()
        print("Salas e historiales de batalla borrados.")
    except Exception as e:
        print("Error borrando salas:", e)

def insetarPokemons():
    if not dbp: return
    
    # Supabase permite insertar arrays de JSON (listas de diccionarios en Python) directamente
    pokemons = [
        {
            "nombre": "Charizard", 
            "tipos": ["FUEGO", "VOLADOR"], 
            "movimientos": [{'nombre': 'Ascuas', 'tipo': 'FUEGO', 'poder': 25, 'PP': 40, 'Prec': 100}, {'nombre': 'Onda ígnea', 'tipo': 'FUEGO', 'poder': 10, 'PP': 95, 'Prec': 90}],
            "EVs": {'ataque': 84, 'defensa': 78, 'velocidad': 100},
            "puntos_de_salud": 78
        },
        {
            "nombre": "Venusaur", 
            "tipos": ["PLANTA", "VENENO"], 
            "movimientos": [{'nombre': 'Hoja afilada', 'tipo': 'PLANTA', 'poder': 25, 'PP': 55, 'Prec': 95}, {'nombre': 'Placaje', 'tipo': 'NORMAL', 'poder': 35, 'PP': 50, 'Prec': 100}],
            "EVs": {'ataque': 82, 'defensa': 83, 'velocidad': 80},
            "puntos_de_salud": 80
        }
    ]
    
    try:
        dbp.table("pokemons").insert(pokemons).execute()
        print("Pokemons iniciales guardados.")
    except Exception as e:
        print("Error insertando pokemons:", e)


print("Que quieres borrar ?")
print("1 - Todo")
print("2 - Salas")
opcion = input("option: ")

if opcion == "1":
    borrarTablas()
    insetarPokemons()
elif opcion == "2":
    borrarSalas()