from src.database.db import db
from src.models.pokemon import pokemon

class pokemonDB:

    def __init__(self):
        self.dbp = db().get_connection()
    
    def getPokemons(self):
        if not self.dbp: return []
        data = self.dbp.table("pokemons").select("*").execute()
        datas = []
        for row in data.data:
            pokemon_obj = pokemon(int(row['id']), row['nombre'], row['tipos'], row['movimientos'], row['EVs'], int(row['puntos_de_salud']))
            datas.append(pokemon_obj)
        return datas

    def emptyTable(self):
        if not self.dbp: return
        self.dbp.table("pokemons").delete().neq("id", -1).execute()

    def insertPokemons(self, data_list):
        if not self.dbp: return
        self.dbp.table("pokemons").insert(data_list).execute()