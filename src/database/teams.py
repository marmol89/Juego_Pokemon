from src.database.db import db
from src.models.team import team as Team

class teams:
    def __init__(self):
        self.dbp = db().get_connection()
    
    def getTeam(self, id):
        if not self.dbp: return None
        data = self.dbp.table("teams").select("*").eq("id", id).execute()
        if len(data.data) == 0: return None
        row = data.data[0]
        return Team(row['id'], row['room_id'], row['user_id'], row['pokemon_id'], row['active'], row['vida'], row['efecto'])
    
    def updateTeam(self, t):
        if not self.dbp: return None
        val = {
            "active": t.active,
            "vida": t.vida,
            "efecto": t.efecto
        }
        self.dbp.table("teams").update(val).eq("id", t.id).execute()

    def createTeam(self, t):
        if not self.dbp: return None
        val = {
            "room_id": t.room_id,
            "user_id": t.user_id,
            "pokemon_id": t.pokemon_id,
            "active": t.active,
            "vida": t.vida,
            "efecto": t.efecto if t.efecto else None
        }
        self.dbp.table("teams").insert(val).execute()
        return True