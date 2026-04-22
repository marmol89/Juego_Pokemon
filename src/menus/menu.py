import os
import time
from src.database.users import users
from src.utils.clear_screen import clear_screen

class menu:
    logout = False
    user = None

    def __init__(self):
        clear_screen()

    def inicio(self):
        print(f"{'='*50}")
        print(f"{'POKÉMON ONLINE':^50}")
        print(f"{'='*50}\n")
        print("  Opciones:")
        print("    [1] Iniciar Sesión")
        print("    [2] Registrarse")
        print("    [0] Salir\n")
        from src.utils.visuals import get_key
        print(f"{'='*50}")
        option = get_key()
        
        if option == '1':
            clear_screen()
            self.login()
            

        if option == '2':
            clear_screen()
            self.register()
         
        if option == '0':
            self.logout = True

        clear_screen()

    def login(self):
        usersdb = users()
        print(f"{'='*50}")
        print(f"{'INICIAR SESIÓN':^50}")
        print(f"{'='*50}\n")
        username = input("  USUARIO: ")
        password = input("  CONTRASEÑA: ")
        data = usersdb.login(username, password)
        if data == False:
            print("\n  [!] Usuario o contraseña incorrectos")
            time.sleep(2)
            self.user = None
            return None
        self.user = data
        return self.user
        
    def register(self):
        usersdb = users()
        print(f"{'='*50}")
        print(f"{'REGISTRO':^50}")
        print(f"{'='*50}\n")
        username = input("  NUEVO USUARIO: ")
        password = input("  NUEVA CONTRASEÑA: ")

        if usersdb.verificarUser(username) == False:
            clear_screen()
            print("\n  [!] El usuario ya está registrado")
            time.sleep(2)
            clear_screen()
            return
        if usersdb.createUser(username, password):
            clear_screen()
            print("\n  [+] Usuario registrado con éxito")
            time.sleep(2)
            clear_screen()

        self.user = usersdb.login(username, password)
        clear_screen()
