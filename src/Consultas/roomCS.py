from src.database.db import db
from src.models.battle import battle
from src.models.team import team
import json
class roomCS:

    def __init__(self):
        self.dbp = db().mydb
    
    def getBattle(self, room_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM battles where room_id=%s"
        mycursor.execute(sql, (room_id,))
        data = mycursor.fetchone()
        if data != None:
            data = battle(data[0], data[1], data[2], data[3], data[4], data[5])

        self.dbp.commit()
        return data
    
    def getUserTeam(self, room_id , user_id):
        self.dbp.commit()
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM teams where room_id=%s AND user_id=%s"
        mycursor.execute(sql, (room_id, user_id))
        data = mycursor.fetchall()
        teams = []

        if teams != None:
            for row in data:
                teams.append(team(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        self.dbp.commit()
        return teams
    