from src.database.pokemonsDB import pokemonDB
from src.models.team import team as Team
import os

class menuTeam:
    def __init__(self, room):
        self.room = room
        os.system('cls')
    
    def selecionar(self, user):
        import time
        pokemons = pokemonDB().getPokemons()
        teams = []
        while len(teams) == 0 or (len(teams) > 0 and len(teams) < 2):
            print(f"{'='*50}")
            print(f"{'SELECCIONA TUS POKÉMON':^50}")
            print(f"{'='*50}\n")
            
            for i in range(0, len(pokemons), 2):
                p1 = f"[{i+1}] {pokemons[i].nombre.upper()}"
                if i+1 < len(pokemons):
                    p2 = f"[{i+2}] {pokemons[i+1].nombre.upper()}"
                    print(f"  {p1:<20} {p2}")
                else:
                    print(f"  {p1}")
                    
            print(f"\n{'='*50}")
            option = input(f"  Elige a tu compañero ({len(teams)+1}/2): ")
            try:
                pokemon = pokemons[int(option) - 1]
                teams.append(Team(None, self.room.id, user.id, pokemon.id, 1 if len(teams) == 0 else 0,  pokemon.puntos_de_salud, None))
                os.system('cls')
                print(f"\n  [+] Has seleccionado a {pokemon.nombre.upper()}!")
                time.sleep(1)
            except:
                pass
            os.system('cls')
            
        print("\n  Esperando al otro jugador...")
        return teams
