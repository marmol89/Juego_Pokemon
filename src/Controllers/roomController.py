from src.database.rooms import rooms
from src.menus.menuRoom import menuRoom
from src.Controllers.teamController import teamController
import time

class roomController:
    user = None
    def __init__(self):
        self.menuRoom = menuRoom()
        self.roomsdb = rooms()
    
    def combrobarRoomEspera(self , room):
        while True:
            room = self.roomsdb.getRoom(room.id)
            print(f"  [DEBUG combrobar] estado={room.estado}, user_id={room.user_id}, enemigo_id={room.enemigo_id}")
            if room.enemigo_id == None:
                self.menuRoom.esperaRoom(1)

            if room.enemigo_id != None and room.estado == 1:
                self.menuRoom.esperaRoom(2)
                time.sleep(2)
                room.estado = 2
                self.roomsdb.updateRoom(room)

            if room.enemigo_id != None and room.estado == 2:
                self.menuRoom.esperaRoom(3)
                print(f"  [DEBUG combrobar] Room ready for combat, calling teamController.inicio()")
                # Ambos jugadores esperan la selección de equipo del otro
                teamController(room, self.user).inicio()
                print(f"  [DEBUG combrobar] teamController.inicio() returned, combat should be done")
                break

            time.sleep(2)
    
    def joinRoom(self, room):
        room.estado = 2
        self.roomsdb.updateRoom(room)