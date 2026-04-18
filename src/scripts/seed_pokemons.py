import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.pokemonsDB import pokemonDB

def fetch_pokemon_data(poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    print(f"Descargando Pokémon #{poke_id}...")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error HTTP en Pokémon {poke_id}: {e}")
        return None

MOVES = {
    "normal": {"nombre": "Cuchillada", "poder": 70, "tipo": "NORMAL"},
    "fire": {"nombre": "Lanzallamas", "poder": 90, "tipo": "FIRE"},
    "water": {"nombre": "Surf", "poder": 90, "tipo": "WATER"},
    "grass": {"nombre": "Hoja Afilada", "poder": 55, "tipo": "GRASS"},
    "electric": {"nombre": "Rayo", "poder": 90, "tipo": "ELECTRIC"},
    "ice": {"nombre": "Rayo Aurora", "poder": 65, "tipo": "ICE"},
    "fighting": {"nombre": "Golpe Kárate", "poder": 50, "tipo": "FIGHTING"},
    "poison": {"nombre": "Bomba Lodo", "poder": 90, "tipo": "POISON"},
    "ground": {"nombre": "Terremoto", "poder": 100, "tipo": "GROUND"},
    "flying": {"nombre": "Golpe Aéreo", "poder": 60, "tipo": "FLYING"},
    "psychic": {"nombre": "Psíquico", "poder": 90, "tipo": "PSYCHIC"},
    "bug": {"nombre": "Chupavidas", "poder": 40, "tipo": "BUG"},
    "rock": {"nombre": "Avalancha", "poder": 75, "tipo": "ROCK"},
    "ghost": {"nombre": "Tinieblas", "poder": 50, "tipo": "GHOST"},
    "dragon": {"nombre": "Furia Dragón", "poder": 60, "tipo": "DRAGON"},
    "dark": {"nombre": "Mordisco", "poder": 60, "tipo": "DARK"},
    "steel": {"nombre": "Garra Metal", "poder": 50, "tipo": "STEEL"},
    "fairy": {"nombre": "Beso Drenaje", "poder": 50, "tipo": "FAIRY"}
}

def main():
    db = pokemonDB()
    
    print("Vaciando tabla actual de Pokémones en Supabase...")
    db.emptyTable()
    
    all_pokemons = []
    
    for i in range(1, 152):
        data = fetch_pokemon_data(i)
        if not data:
            continue
            
        nombre = data['name'].capitalize()
        tipos_raw = [t['type']['name'] for t in data['types']]
        tipos_str = json.dumps(tipos_raw)
        
        hp = 50; ataque = 50; defensa = 50; velocidad = 50
        for s in data['stats']:
            if s['stat']['name'] == 'hp': hp = s['base_stat']
            if s['stat']['name'] == 'attack': ataque = s['base_stat']
            if s['stat']['name'] == 'defense': defensa = s['base_stat']
            if s['stat']['name'] == 'speed': velocidad = s['base_stat']
            
        evs = {"ataque": ataque, "defensa": defensa, "velocidad": velocidad}
        
        selected_moves = []
        # Asignamos 1 movimiento fuerte de cada uno de sus tipos
        for tr in tipos_raw:
            if tr in MOVES:
                selected_moves.append(MOVES[tr])
        
        # Le rellenamos el resto con ataques estándar
        if {"nombre": "Cuchillada", "poder": 70, "tipo": "NORMAL"} not in selected_moves:
             selected_moves.append({"nombre": "Cuchillada", "poder": 70, "tipo": "NORMAL"})
        selected_moves.append({"nombre": "Placaje", "poder": 40, "tipo": "NORMAL"})
        selected_moves.append({"nombre": "Derribo", "poder": 60, "tipo": "NORMAL"})
        selected_moves = selected_moves[:4]
            
        poke = {
            "id": i,
            "nombre": nombre,
            "tipos": tipos_raw,
            "movimientos": selected_moves,
            "EVs": evs,
            "puntos_de_salud": hp
        }
        all_pokemons.append(poke)
        
    print(f"Insertando {len(all_pokemons)} pokémones en Supabase en bloques de 40...")
    
    import time
    for x in range(0, len(all_pokemons), 40):
        chunk = all_pokemons[x:x+40]
        db.insertPokemons(chunk)
        time.sleep(1)
    
    print("¡Carga finalizada con éxito!")

if __name__ == "__main__":
    main()
