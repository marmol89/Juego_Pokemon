import os
import time
from src.database.users import users

class menu:
    logut = False
    user = any

    def __init__(self):
        os.system('clear')

    # def inicio(self):
    #      print("-----POKEMONE MENU-----")
    #      print("Options: ")
    #      print("1 - Batalla")
    #      print("0 - Salir")
    #      self.optionI = input("Option: ")
    #      os.system('clear')

    # def batalla(self):
    #     print("-----POKEMONE MENU BATALLA-----")
    #     print("Options: ")
    #     print("1 - IA")
    #     print("2 - Online")
    #     print("0 - Atras")
    #     self.optionB = input("Option: ")
    #     os.system('clear')
    
    # def selecionarEquipo(self , pokemons, num):
    #     print("-----POKEMONE MENU SELECIONAR EQUIPO-----")
    #     print("-----        Compañero: ",num + 1,"         -----")
    #     print("")
    #     print("Options: ")
    #     print("")
        
    #     i = 0
        
    #     for pokemon in pokemons:
    #         i = i + 1
    #         print(i, pokemon.nombre)
        
    #     print("0 - Atras")
    #     print("")
        
    #     self.optionSE = int(input("Option: "))

    #     os.system('clear')

    #     if self.optionSE > len(pokemons) or self.optionSE < 0:
    #           self.optionSE = 0
    #           os.system('clear')
    #           print("Saliendo")
    #           time.sleep(3)
    #           os.system('clear')
    #           return any
        
    #     if self.optionSE != 0:
    #         return pokemons[self.optionSE - 1]
        
    #     return any
    
    def inicio(self):
        print("-----POKEMONE MENU ONLINE-----")
        print("")
        print("Options: ")
        print("1 - Login")
        print("2 - Register")
        print("0 - salir")
        print("")
        option = input("Option: ")
        
        if option == '1':
            os.system('clear')
            self.login()
            

        if option == '2':
            os.system('clear')
            self.register()
         
        if option == '0':
            self.logut = True

        os.system('clear')

    def login(self):
        usersdb = users()
        print("-----POKEMONE MENU LOGIN-----")
        print("")
        username = input("USERNAME: ")
        password = input("PASSWORD: ")
        data = usersdb.login(username, password)
        if data == False:
            print("Usuario o password incorrecto")
        self.user = data
        return self.user
        os.system('clear')
        
    def register(self):
        usersdb = users()
        print("-----POKEMONE MENU LOGIN-----")
        print("")
        username = input("USERNAME: ")
        password = input("PASSWORD: ")

        if usersdb.verificarUser(username) == False:
            os.system('clear')
            print("El usuario ya esta registrado")
            time.sleep(3)
            os.system('clear')
            return
        if usersdb.createUser(username, password):
            os.system('clear')
            print("Usuario registrado")
            time.sleep(3)
            os.system('clear')
        
        self.user = usersdb.login(username, password)
        os.system('clear')
