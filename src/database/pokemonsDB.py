from src.database.db import db
from src.models.pokemon import pokemon
import json

class pokemonDB:

    def __init__(self):
        self.dbp = db().mydb
    
    def getPokemons(self):
        mycursor = self.dbp.cursor()
        mycursor.execute("SELECT * FROM pokemons")
        pokemons = mycursor.fetchall()
        datas = []
        for data in pokemons:
            prokemon = pokemon(int(data[0]), data[1], eval(data[2]), eval(data[3]), json.loads(data[4]), int(data[5]))
            datas.append(prokemon)
        mycursor.close()
        return datas