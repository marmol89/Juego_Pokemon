import os

class menuLogin:

    user = any

    def __init__(self):
        os.system('clear')
    
    def inicio(self):
        print("-----POKEMONE MENU-----")
        print("-----BIENVENIDO "+ self.user.username.upper() +"-----")
        print("")
        print("Options: ")
        print("1 - Crear Sala")
        print("0 - Log out")
        print("")
        optionI = input("Option: ")

        if optionI == '0':
            self.logut()
    
    def logut(self):
        self.user = any
        os.system('clear')
