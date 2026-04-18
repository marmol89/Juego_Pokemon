import os
import time
from src.database.rooms import rooms
from src.Controllers.roomController import roomController
from src.database.battles import battles

class menuLogin:

    user = None

    def __init__(self):
        self.roomsdb = rooms()
        self.roomcr = roomController()
        self.battlesdb = battles()
        os.system('cls')
    
    def inicio(self):
        # Recargar el usuario para tener los puntos al día
        from src.database.users import users
        self.user = users().getUser(self.user.id)

        print(f"{'='*50}")
        print(f"{'MENÚ PRINCIPAL':^50}")
        print(f"{'='*50}")
        print(f"{'¡Bienvenido, ' + self.user.username.upper() + '!':^50}")
        print(f"{'Puntos de Ranking: ' + str(self.user.puntos):^50}\n")
        print("  Opciones:")
        print("    [1] Crear Sala")
        print("    [2] Unirte a una Sala")
        print("    [0] Cerrar Sesión\n")
        print(f"{'='*50}")
        optionI = input("  Elige una opción: ")

        if optionI == '0':
            os.system('cls')
            self.logut()

        if optionI == '1':
            os.system('cls')
            self.createRoom()
        if optionI == '2':
            os.system('cls')
            self.joinRoom()
    
    def logut(self):
        self.user = None
        os.system('cls')
    
    def createRoom(self):
        self.roomcr.user = self.user
        print(f"{'='*50}")
        print(f"{'CREAR SALA':^50}")
        print(f"{'='*50}\n")
        name = input("  Nombre de la Sala: ")
        self.roomsdb.createRoom(self.user.id, name)
        # Crear la batalla
        os.system('cls')
        print("\n  [+] Sala creada con éxito")
        time.sleep(2)
        room = self.roomsdb.getRoomUserActiva(self.user.id)
        self.battlesdb.createBattle(room.id)
        self.roomcr.combrobarRoomEspera(room)
        os.system('cls')
    
    def joinRoom(self):
        self.roomcr.user = self.user
        salas = self.roomsdb.getRoomActivos()
        if len(salas) == 0:
            while len(salas) == 0:
                print(f"{'='*50}")
                print(f"{'LISTA DE SALAS':^50}")
                print(f"{'='*50}\n")
                print("  [!] No hay salas disponibles\n")
                print("  Opciones:")
                print("    [1] Refrescar")
                print("    [2] Salir\n")
                print(f"{'='*50}")
                option = input("  Elige una opción: ")
                if option == "2":
                    break
                salas = self.roomsdb.getRoomActivos()
                os.system('cls')
        
        if len(salas) > 0:
            option = "0"
            while option == "0":
                print(f"{'='*50}")
                print(f"{'SALAS DISPONIBLES':^50}")
                print(f"{'='*50}\n")
                num = 0
                for sala in salas:
                    num += 1
                    print(f"  [{num}] - {sala.nombre}")
                
                print("\n  [0] Refrescar")
                print("  [-1] Salir\n")
                print(f"{'='*50}")
                option = input("  Elige una sala: ")

                if option == "-1":
                    break
                
                if str(len(salas)) == option:
                    sala = salas[int(option) - 1]
                    sala.enemigo_id = self.user.id
                    self.roomsdb.updateRoom(sala)
                    self.roomcr.combrobarRoomEspera(sala)
                os.system('cls')
        
        os.system('cls')
