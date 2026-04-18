from src.database.db import db
from src.models.pokemon import pokemon

class teamCS:

    def __init__(self):
        self.dbp = db().get_connection()

    def getPokemon(self, id):
        if not self.dbp: return None
        data = self.dbp.table("pokemons").select("*").eq("id", id).execute()
        if len(data.data) == 0: return None
        row = data.data[0]
        return pokemon(int(row['id']), row['nombre'], row['tipos'], row['movimientos'], row['EVs'], int(row['puntos_de_salud']))

    def updateVida(self, team_id, nueva_vida):
        if not self.dbp: return False
        res = self.dbp.table("teams").update({"vida": nueva_vida}).eq("id", team_id).execute()
        return len(res.data) > 0

    def changeActive(self, old_id, new_id):
        if not self.dbp: return False
        self.dbp.table("teams").update({"active": False}).eq("id", old_id).execute()
        self.dbp.table("teams").update({"active": True}).eq("id", new_id).execute()
        return True