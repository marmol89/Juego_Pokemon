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
    
    def logut(self):
        self.user = any
        os.system('clear')
    
    def createRoom(self):
        print("-----POKEMONE MENU-----")
        print("-----CREACION SALA-----")
        print("")
        name = input("Nombre Sala: ")
        self.roomsdb.createRoom(self.user.id, name)
        os.system('clear')
        print("Sala creada")
        time.sleep(2)
        self.roomcr.combrobarRoomEspera(self.roomsdb.getRoomUserActiva(self.user.id))


