from src.database.pokemonsDB import pokemonDB
from src.models.team import team as Team
import os

class menuTeam:
    def __init__(self, room):
        self.room = room
        os.system('clear')
    
    def selecionar(self, user):
        pokemons = pokemonDB().getPokemons()
        teams = []
        while len(teams) == 0 or (len(teams) > 0 and len(teams) < 2):
            print("-----SELECIONA EL POKEMON-----")
            num = 0
            for pokemon in pokemons:
                num += 1
                print(str(num) + " " + pokemon.nombre.upper())
            print('');   
            option = input("Option: ")
            pokemon = pokemons[int(option) - 1]
            teams.append(Team(None, self.room.id, user.id, pokemon.id, 1 if len(teams) == 0 else 0,  pokemon.puntos_de_salud, None))
        
        return teams
