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
        ids = self.user_team_ids
        if isinstance(ids, str):
            ids = json.loads(ids)
        teams_list = []
        for id in ids:
            teams_list.append(teamdb.getTeam(id))
        return teams_list
    
    def enemyTeam(self):
        teamdb = teams()
        ids = self.enemy_team_ids
        if isinstance(ids, str):
            ids = json.loads(ids)
        teams_list = []
        for id in ids:
            teams_list.append(teamdb.getTeam(id))
        return teams_list
    
    def getUser(self):
        battlesdb = battles()
        return battlesdb.getUser()
    
    def getEnemy(self):
        battlesdb = battles()
        return battlesdb.getEnemy()
        