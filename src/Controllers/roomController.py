from src.database.rooms import rooms
from src.menus.menuRoom import menuRoom
import time

class roomController:

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

            if room.enemigo_id != None and room.estado == 2:
                self.menuRoom.esperaRoom(3)
            
            time.sleep(2)