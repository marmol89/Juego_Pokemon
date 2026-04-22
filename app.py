from src.menus.menu import menu
from src.database.pokemonsDB import pokemonDB
from src.menus.menuLogin import menuLogin
from src.models.game_state import GameState

pokemonDB = pokemonDB()
menu = menu()
menuLogin = menuLogin()
game_state = GameState.get_instance()
game_state.pokemons = pokemonDB.getPokemons()

menu.inicio()

while True:
    if menu.logout:
        break

    if menu.user is not None:
        if menuLogin.user is None:
            menuLogin.user = menu.user
        menuLogin.inicio()
        menu.user = menuLogin.user
    
    else:
        menu.inicio()



