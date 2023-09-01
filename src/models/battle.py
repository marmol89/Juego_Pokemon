# from src.database.rooms import rooms
from src.database.teams import teams
from src.database.battles import battles
import json
class battle:

    def __init__(self, id, room_id, winner_id, loser_id, user_team_ids, enemy_team_ids):
        self.id = id
        self.room_id = room_id
        self.winner_id = winner_id
        self.loser_id = loser_id
        self.user_team_ids = user_team_ids
        self.enemy_team_ids = enemy_team_ids
    
    def userTeam(self):
        teamdb = teams()
        ids = json.loads(self.user_team_ids)
        teams = []
        for id in ids:
            teams.append(teamdb.getTeam(id))
        return teams
    
    def enemyTeam(self):
        teamdb = teams()
        ids = json.loads(self.enemy_team_ids)
        teams = []
        for id in ids:
            teams.append(teamdb.getTeam(id))
        return teams
    
    def getUser(self):
        battlesdb = battles()
        return battlesdb.getUser()
    
    def getEnemy(self):
        battlesdb = battles()
        return battlesdb.getEnemy()
        