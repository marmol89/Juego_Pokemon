from src.menus.menuTeam import menuTeam
from src.database.teams import teams

class teamController:
    user = any
    def __init__(self , room, user):
        self.room = room
        self.user = user
        self.menu = menuTeam(room)
        self.teamdb = teams()
    
    def inicio(self):
        teams = self.menu.selecionar(self.user)

        for team in teams:
            self.teamdb.createTeam(team)





