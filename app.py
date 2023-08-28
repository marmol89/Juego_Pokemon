from src.menus.menu import menu
from src.models.pokemon import pokemon
from src.database.pokemonsDB import pokemonDB
from src.menus.menuLogin import menuLogin


#pokemon = pokemon('Charizard' , ['Fuego', 'Volador'], ['Cola Ala'], {'ataque' : 84, 'defensa' : 78}, 78)
pokemonDB = pokemonDB()
menu = menu()
menuLogin = menuLogin()

menu.inicio()

equipoA = []

equipoE = []

pokemons = pokemonDB.getPokemons()

while True:
    if menu.logut:
        break

    if menu.user != None and menu.user != any:
        if menuLogin.user == any:
            menuLogin.user = menu.user
        menuLogin.inicio()
        menu.user = menuLogin.user
    
    else:
        menu.inicio()




pokemonDB.dbp.close()