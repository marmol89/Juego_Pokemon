from src.database.db import db

class movementCS:
    def __init__(self):
        self.dbp = db().get_connection()
        
    def insertMovement(self, room_id, pokemon_id, nombre, efecto="ninguno"):
        if not self.dbp: return False
        data = {
            "room_id": room_id,
            "pokemon_id": pokemon_id,
            "nombre": nombre,
            "efecto": efecto
        }
        res = self.dbp.table("movements").insert(data).execute()
        return len(res.data) > 0
        
    def getMovement(self, room_id, pokemon_id):
        if not self.dbp: return None
        res = self.dbp.table("movements").select("*").eq("room_id", room_id).eq("pokemon_id", pokemon_id).execute()
        if len(res.data) > 0:
            return res.data[0]
        return None
        
    def deleteMovement(self, movement_id):
        if not self.dbp: return False
        res = self.dbp.table("movements").delete().eq("id", movement_id).execute()
        return len(res.data) > 0
