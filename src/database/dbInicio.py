import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="Juego_Pokemon"
)

def borrarTablas():
    mycursor = mydb.cursor()
    mycursor.execute("show tables")
    data = mycursor.fetchall()
    table_array = [table[0] for table in data]
    for table in table_array:
        sql = "DROP TABLE " + table
        mycursor.execute(sql)
    mycursor.close()

def borrarSalas():
    mycursor = mydb.cursor()
    sql = "DROP TABLE movements , battles , teams , rooms"
    mycursor.execute(sql)
    createTableBattle()
    mycursor.close()

def createTables():
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE pokemons (id int NOT NULL AUTO_INCREMENT ,nombre VARCHAR(255), tipos JSON, movimientos JSON, EVs JSON, puntos_de_salud int, PRIMARY KEY (id))")
    mycursor.execute("CREATE TABLE users (id int NOT NULL AUTO_INCREMENT ,username VARCHAR(255), password VARCHAR(600), PRIMARY KEY (id))")
    mycursor.close()

def createTableBattle():
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE rooms (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, enemigo_id INT, nombre VARCHAR(255), estado INT DEFAULT 0, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (enemigo_id) REFERENCES users(id))")
    mycursor.execute("CREATE TABLE teams (id INT AUTO_INCREMENT PRIMARY KEY, room_id INT, user_id INT, pokemon_id INT, active BOOLEAN, vida INT, efecto VARCHAR(255), FOREIGN KEY (room_id) REFERENCES rooms(id), FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (pokemon_id) REFERENCES pokemons(id))")
    mycursor.execute("CREATE TABLE battles (id INT AUTO_INCREMENT PRIMARY KEY, room_id INT UNIQUE, winner_id INT NULL, loser_id INT NULL, user_team_ids JSON, enemy_team_ids JSON, FOREIGN KEY (room_id) REFERENCES rooms(id), FOREIGN KEY (winner_id) REFERENCES users(id), FOREIGN KEY (loser_id) REFERENCES users(id))")
    mycursor.execute("CREATE TABLE movements (id INT AUTO_INCREMENT PRIMARY KEY, room_id INT, pokemon_id INT, nombre VARCHAR(255) NOT NULL, efecto VARCHAR(255) NOT NULL, FOREIGN KEY (room_id) REFERENCES rooms(id), FOREIGN KEY (pokemon_id) REFERENCES pokemons(id))")

def insetarPokemons():
    mycursor = mydb.cursor()
    sql = "INSERT INTO pokemons (nombre, tipos, movimientos, EVs, puntos_de_salud) VALUES (%s, %s, %s, %s, %s)"
    
    #Charizard
    tipos = json.dumps(['FUEGO', 'VOLADOR'])
    movimientos = json.dumps([{'nombre': 'Ascuas', 'tipo': 'FUEGO', 'poder': 25, 'PP': 40, 'Prec': 100}, {'nombre': 'Onda ígnea', 'tipo': 'FUEGO', 'poder': 10, 'PP': 95, 'Prec': 90}])
    EVs = json.dumps({'ataque': 84, 'defensa': 78, 'velocidad': 100})
    val = ("Charizard", tipos, movimientos, EVs, 78)
    mycursor.execute(sql, val)

    #Venusaur
    tipos = json.dumps(['PLANTA', 'VENENO'])
    movimientos = json.dumps([{'nombre': 'Hoja afilada', 'tipo': 'PLANTA', 'poder': 25, 'PP': 55, 'Prec': 95}, {'nombre': 'Placaje', 'tipo': 'NORMAL', 'poder': 35, 'PP': 50, 'Prec': 100}])
    EVs = json.dumps({'ataque': 82, 'defensa': 83, 'velocidad': 80})
    val = ("Venusaur", tipos, movimientos, EVs, 80)
    mycursor.execute(sql, val)

    mycursor.close()
    mydb.commit()


print("Que quieres borrar ?")
print("1 - Todo")
print("2 - Salas")
opcion = input("option: ")

if opcion == "1":
    borrarTablas()
    createTables()
    createTableBattle()
    insetarPokemons()

if opcion == "2":
    borrarSalas()



mydb.close()