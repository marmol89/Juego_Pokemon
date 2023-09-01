import os
import time
from src.database.users import users

class menu:
    logut = False
    user = any

    def __init__(self):
        os.system('cls')

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
            os.system('cls')
            self.login()
            

        if option == '2':
            os.system('cls')
            self.register()
         
        if option == '0':
            self.logut = True

        os.system('cls')

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
        
    def register(self):
        usersdb = users()
        print("-----POKEMONE MENU LOGIN-----")
        print("")
        username = input("USERNAME: ")
        password = input("PASSWORD: ")

        if usersdb.verificarUser(username) == False:
            os.system('cls')
            print("El usuario ya esta registrado")
            time.sleep(3)
            os.system('cls')
            return
        if usersdb.createUser(username, password):
            os.system('cls')
            print("Usuario registrado")
            time.sleep(3)
            os.system('cls')
        
        self.user = usersdb.login(username, password)
        os.system('cls')
