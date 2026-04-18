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