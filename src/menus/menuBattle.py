import os
import time

class menuBattle:
    def __init__(self , room):
        self.room = room
        os.system('cls')
    
    def inicio(self, user, enemy):
        print("Inicio battalla")
        print(user.username + " vs " + enemy.username)
        time.sleep(5)
    

    def combate(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print("------------------------")
        time.sleep(5)
    

    def vida(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print("------------------------")
        time.sleep(5)