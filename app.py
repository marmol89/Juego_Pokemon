from src.menu import menu
from src.pokemon import pokemon

pokemon = pokemon('Charizard' , ['Fuego', 'Volador'], ['Cola Ala'], {'ataque' : 84, 'defensa' : 78}, 78)
menu = menu()
menu.inicio()

equipoA = []

equipoE = []

pokemons = [
    'Charizard',
    'Venusaur',
    'Blastoise'
    ]

def listToString(s):
 
    # initialize an empty string
    str1 = ", "
 
    # return string
    return (str1.join(s))


while True:
    if menu.optionI == '0':
        break

    if menu.optionI == '1':
        menu.batalla()

        if menu.optionB == '0':
            menu.inicio()

        if menu.optionB == '1':
           for i in range(6):
               selection = menu.selecionarEquipo(pokemons , i)
               if selection == any:
                   break
               equipoA.append(selection)
           print('Equipo', listToString(equipoA))