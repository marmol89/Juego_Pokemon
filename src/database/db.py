import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
class db:

    mydb = any

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host=os.getenv('HOST_MYSQL'),
                    user=os.getenv('USER_MYSQL'),
                    password=os.getenv('PASS_MYSQL'),
                    database=os.getenv('DATABASE_MYSQL')
            )
        
    def mydb(self):
        return self.mydb
    
    def close(self):
        if self.mydb != any:
            self.mydb.close()