from src.menus.menu import menu
from src.database.pokemonsDB import pokemonDB
from src.menus.menuLogin import menuLogin

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