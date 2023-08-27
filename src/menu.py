import os
import time

class menu:
    optionI = 0
    optionB = 0
    optionSE = 0

    def __init__(self):
        os.system('clear')

    def inicio(self):
         print("-----POKEMONE MENU-----")
         print("Options: ")
         print("1 - Batalla")
         print("0 - Salir")
         self.optionI = input("Option: ")
         os.system('clear')

    def batalla(self):
        print("-----POKEMONE MENU BATALLA-----")
        print("Options: ")
        print("1 - IA")
        print("2 - Online")
        print("0 - Atras")
        self.optionB = input("Option: ")
        os.system('clear')
    
    def selecionarEquipo(self , pokemons, num):
        print("-----POKEMONE MENU SELECIONAR EQUIPO-----")
        print("-----        Compañero: ",num + 1,"         -----")
        print("")
        print("Options: ")
        print("")
        
        i = 0
        
        for pokemon in pokemons:
            i = i + 1
            print(i, pokemon)
        
        print("0 - Atras")
        print("")
        
        self.optionSE = int(input("Option: "))

        os.system('clear')

        if self.optionSE > len(pokemons) or self.optionSE < 0:
              self.optionSE = 0
              os.system('clear')
              print("Saliendo")
              time.sleep(3)
              os.system('clear')
              return any
        
        if self.optionSE != 0:
            return pokemons[self.optionSE - 1]
        
        return any
