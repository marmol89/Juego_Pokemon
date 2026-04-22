from src.menus.menuTeam import menuTeam
from src.database.teams import teams
from src.database.battles import battles
from src.Controllers.battleController import battleController

class teamController:
    user = None
    def __init__(self , room, user):
        self.room = room
        self.user = user
        self.menu = menuTeam(room)
        self.teamdb = teams()
    
    def inicio(self):
        teams = self.menu.selecionar(self.user)

        for team in teams:
            self.teamdb.createTeam(team)
    

        battlesdb = battles()
        battle = self.room.getBattle()

        if (self.user.id == self.room.user_id):
            teamuser = self.room.getUserTeam()
            battle.user_team_ids = [team.id for team in teamuser]
            battlesdb.updateBattleUserTeam(battle)
        
        if (self.user.id == self.room.enemigo_id):
            teamenemy = self.room.getEnemigoTeam()
            battle.enemy_team_ids = [team.id for team in teamenemy]
            battlesdb.updateBattleEnemyTeam(battle)

        while True:
            battle = self.room.getBattle()
            if battle is None:
                break
                
            if(battle.enemy_team_ids and battle.user_team_ids):
                    battleController(self.room, self.user).inicio()
                    # Salir del bucle una vez termina la batalla
                    break
            
            if(battle.winner_id != None and battle.loser_id != None):
                break
            
            import time
            time.sleep(1)






