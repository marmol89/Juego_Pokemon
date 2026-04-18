from src.database.pokemonsDB import pokemonDB
from src.models.team import team as Team
import os

class menuTeam:
    def __init__(self, room):
        self.room = room
        os.system('cls')
    
    def selecionar(self, user):
        import time
        from src.utils.visuals import type_text, get_key
        all_pokemons = pokemonDB().getPokemons()
        teams = []
        
        page = 0
        page_size = 15
        search_query = ""
        
        while len(teams) < 2:
            os.system('cls')
            # Filtrar pokémons si hay búsqueda
            filtered = [p for p in all_pokemons if search_query.lower() in p.nombre.lower()]
            
            total_pages = (len(filtered) - 1) // page_size + 1 if filtered else 1
            if page >= total_pages: page = total_pages - 1
            if page < 0: page = 0
            
            start_idx = page * page_size
            end_idx = start_idx + page_size
            current_page_pokes = filtered[start_idx:end_idx]
            
            print(f"{'='*70}")
            header = f"SELECCIONA TU EQUIPO ({len(teams)+1}/2)"
            if search_query:
                header += f" - Buscando: '{search_query}'"
            print(f"{header:^70}")
            print(f"{'Página ' + str(page+1) + '/' + str(total_pages):^70}")
            print(f"{'='*70}\n")
            
            # Mostrar en 3 columnas
            for i in range(0, len(current_page_pokes), 3):
                row = ""
                for j in range(3):
                    if i + j < len(current_page_pokes):
                        p = current_page_pokes[i+j]
                        item_str = f"[{p.id}] {p.nombre.upper()}"
                        row += f"  {item_str:<22}"
                print(row)
            
            print(f"\n{'='*70}")
            print("  [N] Siguiente  [P] Anterior  [S] Buscar  [C] Limpiar  [Enter] Elegir ID")
            print(f"{'='*70}")
            
            opcion = get_key()
            
            if opcion == 'n':
                if page < total_pages - 1: page += 1
            elif opcion == 'p':
                if page > 0: page -= 1
            elif opcion == 's':
                search_query = input("\n  Nombre a buscar: ").strip()
                page = 0
            elif opcion == 'c':
                search_query = ""
                page = 0
            elif opcion in ['\r', '\n', ' ']:
                try:
                    poke_id = int(input("\n  ID del Pokémon: ").strip())
                    pokemon = next((p for p in all_pokemons if p.id == poke_id), None)
                    if pokemon:
                        if any(t.pokemon_id == pokemon.id for t in teams):
                            print("  [!] Ya has seleccionado a este Pokémon.")
                            time.sleep(1)
                            continue
                        teams.append(Team(None, self.room.id, user.id, pokemon.id, 1 if len(teams) == 0 else 0,  pokemon.puntos_de_salud, None))
                        print(f"\n  [+] ¡{pokemon.nombre.upper()} se ha unido a tu equipo!")
                        time.sleep(1)
                except:
                    pass

        print("\n  Esperando al otro jugador...")
        return teams
