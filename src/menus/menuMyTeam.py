from src.database.pokemonsDB import pokemonDB
from src.database.teams import teams as TeamsDB
from src.models.team import team as Team
from src.utils.clear_screen import clear_screen
import os

class menuMyTeam:
    def __init__(self, user):
        self.user = user
        clear_screen()

    def manage(self):
        """Main entry point for managing user's global team."""
        while True:
            clear_screen()
            current_team = self._get_current_team()

            print(f"{'='*50}")
            print(f"{'MI EQUIPO':^50}")
            print(f"{'='*50}\n")

            if current_team:
                print("  Tu equipo actual:")
                for i, pokemon in enumerate(current_team, 1):
                    poke_info = pokemon.pokemon()
                    print(f"    [{i}] {poke_info.nombre.upper()} - {poke_info.puntos_de_salud} HP")
            else:
                print("  No tienes un equipo configurado.\n")

            print(f"\n{'='*50}")
            print("  Opciones:")
            if len(current_team) < 2:
                print("    [1] Crear equipo")
            else:
                print("    [1] Modificar equipo")
            print("    [0] Volver al menú")
            print(f"{'='*50}")

            from src.utils.visuals import get_key
            opcion = get_key()

            if opcion == '0':
                return
            elif opcion == '1':
                if len(current_team) >= 2:
                    self._modify_team(current_team)
                else:
                    self._create_team()

    def _get_current_team(self):
        """Get user's current global team (room_id = 0)."""
        from src.database.db import db
        try:
            dbp = db().get_connection()
            data = dbp.table("teams").select("*").eq("user_id", self.user.id).eq("room_id", 0).execute()
            return [Team(r['id'], r['room_id'], r['user_id'], r['pokemon_id'], r['active'], r['vida'], r['efecto']) for r in data.data]
        except:
            return []

    def _clear_team(self):
        """Delete all global team entries for the user."""
        from src.database.db import db
        dbp = db().get_connection()
        dbp.table("teams").delete().eq("user_id", self.user.id).eq("room_id", 0).execute()

    def _create_team(self):
        """Create a new global team for the user."""
        import time
        from src.utils.visuals import get_key
        from src.utils.visuals import type_text

        all_pokemons = pokemonDB().getPokemons()
        selected = []

        page = 0
        page_size = 15
        search_query = ""

        while len(selected) < 2:
            clear_screen()
            filtered = [p for p in all_pokemons if search_query.lower() in p.nombre.lower()]

            total_pages = (len(filtered) - 1) // page_size + 1 if filtered else 1
            if page >= total_pages: page = total_pages - 1
            if page < 0: page = 0

            start_idx = page * page_size
            end_idx = start_idx + page_size
            current_page_pokes = filtered[start_idx:end_idx]

            print(f"{'='*70}")
            header = f"SELECCIONA TU EQUIPO ({len(selected)+1}/2)"
            if search_query:
                header += f" - Buscando: '{search_query}'"
            print(f"{header:^70}")
            print(f"{'Página ' + str(page+1) + '/' + str(total_pages):^70}")
            print(f"{'='*70}\n")

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
                        if any(t.pokemon_id == pokemon.id for t in selected):
                            print("  [!] Ya has seleccionado a este Pokémon.")
                            time.sleep(1)
                            continue
                        team_entry = Team(None, 0, self.user.id, pokemon.id, 1 if len(selected) == 0 else 0, pokemon.puntos_de_salud, None)
                        selected.append(team_entry)
                        print(f"\n  [+] ¡{pokemon.nombre.upper()} se ha unido a tu equipo!")
                        time.sleep(1)
                except:
                    pass

        # Save team to DB
        teamsdb = TeamsDB()
        for entry in selected:
            teamsdb.createTeam(entry)

        print("\n  ¡Equipo creado! Presiona cualquier tecla para volver...")
        get_key()

    def _modify_team(self, current_team):
        """Modify or clear the user's global team."""
        import time
        from src.utils.visuals import get_key

        clear_screen()
        print(f"{'='*50}")
        print(f"{'MODIFICAR EQUIPO':^50}")
        print(f"{'='*50}\n")

        print("  Tu equipo actual:")
        for i, pokemon in enumerate(current_team, 1):
            poke_info = pokemon.pokemon()
            print(f"    [{i}] {poke_info.nombre.upper()}")

        print("\n  Opciones:")
        print("    [1] Recrear equipo (borrar y crear nuevo)")
        print("    [0] Volver")

        opcion = get_key()

        if opcion == '1':
            self._clear_team()
            self._create_team()
        elif opcion == '0':
            return
