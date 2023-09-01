from src.database.rooms import rooms
import os
class menuRoom:

    def __init__(self):
        self.roomsdb = rooms()

    def esperaRoom(self, tipo):
        os.system('cls')
        if tipo == 1:
            print("-----POKEMONE SALA-----")
            print("-----ESPERA A QUE SE TE UNA EL RIVAL-----")
        if tipo == 2:
            print("-----POKEMONE SALA-----")
            print("-----UNIENDOTE A LA PARTIDA-----")
        if tipo == 3:
            print("-----POKEMONE SALA-----")
            print("-----CARGANDO DATOS-----")