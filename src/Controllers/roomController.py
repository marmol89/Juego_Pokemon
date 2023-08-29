from src.database.rooms import rooms
from src.menus.menuRoom import menuRoom
from src.Controllers.teamController import teamController
import time

class roomController:
    user = any
    def __init__(self):
        self.menuRoom = menuRoom()
        self.roomsdb = rooms()
    
    def combrobarRoomEspera(self , room):
        while True:
            room = self.roomsdb.getRoom(room.id)
            if room.enemigo_id == None:
                self.menuRoom.esperaRoom(1)

            if room.enemigo_id != None and room.estado == 1:
                self.menuRoom.esperaRoom(2)
                time.sleep(2)
                room.estado = 2
                self.roomsdb.updateRoom(room)

            if room.enemigo_id != None and room.estado == 2:
                self.menuRoom.esperaRoom(3)
                teamController(room, self.user).inicio()
                break
            
            time.sleep(2)
    
    def joinRoom(self, room):
        room.estado = 2
        self.roomsdb.updateRoom(room)