from src.database.db import db
from src.models.room import room

class rooms:
    def __init__(self):
        self.dbp = db().get_connection()
    
    def getRooms(self):
        if not self.dbp: return []
        data = self.dbp.table("rooms").select("*").execute()
        return [room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado']) for row in data.data]
    
    def getRoomActivos(self):
        if not self.dbp: return []
        data = self.dbp.table("rooms").select("*").eq("estado", 1).execute()
        return [room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado']) for row in data.data]
    
    def getRoomCerrados(self):
        if not self.dbp: return []
        data = self.dbp.table("rooms").select("*").eq("estado", 2).execute()
        return [room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado']) for row in data.data]
    
    def getRoomFinalizados(self):
        if not self.dbp: return []
        data = self.dbp.table("rooms").select("*").eq("estado", 3).execute()
        return [room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado']) for row in data.data]
    
    def getRoomUser(self, user_id):
        if not self.dbp: return []
        data = self.dbp.table("rooms").select("*").or_(f"user_id.eq.{user_id},enemigo_id.eq.{user_id}").execute()
        return [room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado']) for row in data.data]
    
    def getRoomUserActiva(self, user_id):
        if not self.dbp: return None
        # Eq estado=1 y el OR para el ID de usuario u oponente
        data = self.dbp.table("rooms").select("*").eq("estado", 1).or_(f"user_id.eq.{user_id},enemigo_id.eq.{user_id}").execute()
        if len(data.data) == 0: return None
        row = data.data[0]
        return room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado'])
    
    def createRoom(self, user_id, name):
        if not self.dbp: return None
        val = {"user_id": user_id, "nombre": name, "estado": 1}
        self.dbp.table("rooms").insert(val).execute()
    
    def getRoom(self, id):
        if not self.dbp: return None
        data = self.dbp.table("rooms").select("*").eq("id", id).execute()
        if len(data.data) == 0: return None
        row = data.data[0]
        return room(row['id'], row['user_id'], row['enemigo_id'], row['nombre'], row['estado'])
    
    def updateRoom(self, r):
        if not self.dbp: return None
        val = {
            "user_id": r.user_id,
            "enemigo_id": r.enemigo_id,
            "nombre": r.nombre,
            "estado": r.estado
        }
        self.dbp.table("rooms").update(val).eq("id", r.id).execute()