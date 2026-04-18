from src.database.db import db
from src.models.user import user
from src.models.pokemon import pokemon

class battles:
    def __init__(self):
        self.dbp = db().get_connection()
    
    def createBattle(self, room_id):
        if not self.dbp: return None
        val = {"room_id": room_id}
        res = self.dbp.table("battles").insert(val).execute()
        return res.data[0]['id'] if res.data else None
    
    def updateBattle(self, b):
        if not self.dbp: return None
        val = {
            "winner_id": b.winner_id,
            "loser_id": b.loser_id,
            "user_team_ids": b.user_team_ids,
            "enemy_team_ids": b.enemy_team_ids
        }
        self.dbp.table("battles").update(val).eq("room_id", b.room_id).execute()
    
    def getUser(self, battle_id):
        if not self.dbp: return None
        data = self.dbp.table("battles").select("rooms!inner(user_id)").eq("id", battle_id).execute()
        if not data.data or not data.data[0].get('rooms'): return None
        uid = data.data[0]['rooms']['user_id']
        u_data = self.dbp.table("users").select("*").eq("id", uid).execute()
        if not u_data.data: return None
        usr = u_data.data[0]
        return user(usr['id'], usr['username'], usr['password'])
        
    def getEnemy(self, battle_id):
        if not self.dbp: return None
        data = self.dbp.table("battles").select("rooms!inner(enemigo_id)").eq("id", battle_id).execute()
        if not data.data or not data.data[0].get('rooms'): return None
        enemy_id = data.data[0]['rooms']['enemigo_id']
        u_data = self.dbp.table("users").select("*").eq("id", enemy_id).execute()
        if not u_data.data: return None
        usr = u_data.data[0]
        return user(usr['id'], usr['username'], usr['password'])
        
    def updateBattleUserTeam(self, b):
        if not self.dbp: return None
        val = {"user_team_ids": b.user_team_ids}
        self.dbp.table("battles").update(val).eq("room_id", b.room_id).execute()
    
    def updateBattleEnemyTeam(self, b):
        if not self.dbp: return None
        val = {"enemy_team_ids": b.enemy_team_ids}
        self.dbp.table("battles").update(val).eq("room_id", b.room_id).execute()