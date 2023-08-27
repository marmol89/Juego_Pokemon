from src.menu import menu
from src.pokemon import pokemon
from src.database.pokemonsDB import pokemonDB


#pokemon = pokemon('Charizard' , ['Fuego', 'Volador'], ['Cola Ala'], {'ataque' : 84, 'defensa' : 78}, 78)
pokemonDB = pokemonDB()
menu = menu()

menu.inicio()

equipoA = []

equipoE = []

pokemons = pokemonDB.getPokemons()

while True:
    if menu.optionI == '0':
        break

    if menu.optionI == '1':
        menu.batalla()

        if menu.optionB == '0':
            menu.inicio()

        if menu.optionB == '1':
           for i in range(2):
               selection = menu.selecionarEquipo(pokemons , i)
               if selection == any:
                   break
               equipoA.append(selection)

        if menu.optionB == '2':
            menu.online()
            
            if menu.optionO == '1':
                menu.login()
            if menu.optionO == '2':
                menu.register()


pokemonDB.dbp.close()