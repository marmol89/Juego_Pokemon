import os
import time

class menuBattle:
    def __init__(self , room):
        self.room = room
        os.system('cls')
    
    def inicio(self, user, enemy):
        print("Inicio battalla")
        print(user.username + " vs " + enemy.username)
        time.sleep(2)

    def presentacionPokemon(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print("------------------------")
        print(user.username + " vs " + enemy.username)
        print("----"+user.username+"------Pokemon------ENEMIGO------")
        print(userTeam[0].pokemon().nombre + " vs " + enemyTeam[0].pokemon().nombre)
        print(userTeam[1].pokemon().nombre + " vs " + enemyTeam[1].pokemon().nombre)
        time.sleep(5)

    def combate(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print("------------------------")
        time.sleep(5)
    

    def vida(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print("------------------------")
        time.sleep(5)