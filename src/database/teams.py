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

    def getGlobalTeam(self, user_id):
        """Get user's global team (room_id = 0) and return as Team objects."""
        if not self.dbp: return None
        data = self.dbp.table("teams").select("*").eq("user_id", user_id).eq("room_id", 0).execute()
        if len(data.data) == 0: return None
        return [Team(row['id'], row['room_id'], row['user_id'], row['pokemon_id'], row['active'], row['vida'], row['efecto']) for row in data.data]

    def copyGlobalTeamToRoom(self, user_id, room_id):
        """Copy user's global team to a specific room, creating new team entries."""
        if not self.dbp: return None
        global_team = self.getGlobalTeam(user_id)
        if not global_team: return None
        for entry in global_team:
            new_entry = Team(None, room_id, user_id, entry.pokemon_id, entry.active, entry.vida, entry.efecto)
            self.createTeam(new_entry)
        return True

    def getTeamByRoomAndUser(self, room_id, user_id):
        """Get team entries for a specific room and user."""
        if not self.dbp: return None
        data = self.dbp.table("teams").select("*").eq("room_id", room_id).eq("user_id", user_id).execute()
        if len(data.data) == 0: return None
        return [Team(row['id'], row['room_id'], row['user_id'], row['pokemon_id'], row['active'], row['vida'], row['efecto']) for row in data.data]