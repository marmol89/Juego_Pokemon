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
        menuBattle(self.room).presentacionPokemons(self.user, self.enemy, self.userTeam, self.enemyTeam)
        self.combate()

    def combate(self):

        while (self.room.isVidaTeamUser() and self.room.isVidaTeamEnemigo()):
            self.updateTeams()
            num = menuBattle(self.room).combate(self.user, self.enemy, self.userTeam, self.enemyTeam)
        
        if (self.room.isVidaTeamEnemigo()):
            self.battle.winner_id = self.enemy.id
            self.battle.loser_id = self.user.id
            self.battle.save()
            menuBattle(self.room).derrata(self.user, self.enemy, self.userTeam, self.enemyTeam)
        
        if (self.room.isVidaTeamUser()):
            self.battle.winner_id = self.user.id
            self.battle.loser_id = self.enemy.id
            self.battle.save()
            menuBattle(self.room).vitoria(self.user, self.enemy, self.userTeam, self.enemyTeam)
            

    def updateTeams(self):
        if (self.user.id == self.room.user_id):
            self.userTeam = self.room.getUserTeam()
            self.enemyTeam = self.room.getEnemigoTeam()
            self.enemy = self.room.getEnemigo()
        if (self.user.id == self.room.enemigo_id):
            self.userTeam = self.room.getEnemigoTeam()
            self.enemyTeam = self.room.getUserTeam()
            self.enemy = self.room.getUser()