import mysql.connector

class db:

    mydb = any

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Juego_Pokemon"
            )
        
    def mydb(self):
        return self.mydb
    
    def close(self):
        if self.mydb != any:
            self.mydb.close()