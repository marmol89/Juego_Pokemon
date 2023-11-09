from src.database.db import db
from src.models.pokemon import pokemon
import json
class teamCS:

    def __init__(self):
        self.dbp = db().mydb

    def getPokemon(self, id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM pokemons where id=%s"
        mycursor.execute(sql, (id,))
        data = mycursor.fetchone()

        prokemon = pokemon(int(data[0]), data[1], eval(data[2]), eval(data[3]), json.loads(data[4]), int(data[5]))

        self.dbp.commit()
        return prokemon
        