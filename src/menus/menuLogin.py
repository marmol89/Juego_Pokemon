import os
import time
from src.database.rooms import rooms
from src.Controllers.roomController import roomController

class menuLogin:

    user = any

    def __init__(self):
        self.roomsdb = rooms()
        self.roomcr = roomController()
        os.system('clear')
    
    def inicio(self):
        print("-----POKEMONE MENU-----")
        print("-----BIENVENIDO "+ self.user.username.upper() +"-----")
        print("")
        print("Options: ")
        print("1 - Crear Sala")
        print("2 - Unirte a una sala")
        print("0 - Log out")
        print("")
        optionI = input("Option: ")

        if optionI == '0':
            os.system('clear')
            self.logut()

        if optionI == '1':
            os.system('clear')
            self.createRoom()
        if optionI == '2':
            os.system('clear')
            self.joinRoom()
    
    def logut(self):
        self.user = any
        os.system('clear')
    
    def createRoom(self):
        self.roomcr.user = self.user
        print("-----POKEMONE MENU-----")
        print("-----CREACION SALA-----")
        print("")
        name = input("Nombre Sala: ")
        self.roomsdb.createRoom(self.user.id, name)
        os.system('clear')
        print("Sala creada")
        time.sleep(2)
        self.roomcr.combrobarRoomEspera(self.roomsdb.getRoomUserActiva(self.user.id))
        os.system('clear')
    
    def joinRoom(self):
        self.roomcr.user = self.user
        salas = self.roomsdb.getRoomActivos()
        if len(salas) == 0:
            while len(salas) == 0:
                print("-----POKEMONE MENU-----")
                print("-----LISTA SALAS-----")
                print("")
                print("No hay salas disponibles")
                print("")
                print("Options : ")
                print("1 - Refrescar")
                print("2 - salir")
                print("")
                option = input("Option:")
                if option == "2":
                    break
                salas = self.roomsdb.getRoomActivos()
                os.system('clear')
        
        if len(salas) > 0:
            option = "0"
            while option == "0":
                print("-----POKEMONE MENU-----")
                print("-----LISTA SALAS-----")
                print("")
                num = 0
                for sala in salas:
                    num += 1
                    print(str(num) + " - " + sala.nombre)
                
                print("0 - Refrescar")
                print("-1 - salir")
                print("")
                option = input("Option:")

                if option == "-1":
                    break
                
                if str(len(salas)) == option:
                    sala = salas[int(option) - 1]
                    sala.enemigo_id = self.user.id
                    self.roomsdb.updateRoom(sala)
                    self.roomcr.combrobarRoomEspera(sala)
                os.system('clear')
        
        os.system('clear')


            
        


