import time
class battleController:
    def __init__(self, room):
        self.room = room
        self.battle = room.getBattle()
        self.user = room.getUser()
        self.enemy = room.getEnemigo()
    
    def inicio(self):
        print("inicio battalla")
        time.sleep(10)