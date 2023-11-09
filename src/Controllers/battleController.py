import time
from src.menus.menuBattle import menuBattle
class battleController:
    def __init__(self, room, user):
        self.room = room
        self.battle = room.getBattle()
        self.user = user
        self.updateTeams()
    
    def inicio(self):
        menuBattle(self.room).inicio(self.user, self.enemy)
        menuBattle(self.room).presentacionPokemon(self.user, self.enemy, self.userTeam, self.enemyTeam)


    def updateTeams(self):
        if (self.user.id == self.room.user_id):
            self.userTeam = self.room.getUserTeam()
            self.enemyTeam = self.room.getEnemigoTeam()
            self.enemy = self.room.getEnemigo()
        if (self.user.id == self.room.enemigo_id):
            self.userTeam = self.room.getEnemigoTeam()
            self.enemyTeam = self.room.getUserTeam()
            self.enemy = self.room.getUser()