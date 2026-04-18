import os
import time
from src.database.rooms import rooms
from src.Controllers.roomController import roomController
from src.database.battles import battles

class menuLogin:

    user = None

    def __init__(self):
        self.roomsdb = rooms()
        self.roomcr = roomController()
        self.battlesdb = battles()
        os.system('cls')
    
    def inicio(self):
        # Recargar el usuario para tener los puntos al día
        from src.database.users import users
        self.user = users().getUser(self.user.id)

        print(f"{'='*50}")
        print(f"{'MENÚ PRINCIPAL':^50}")
        print(f"{'='*50}")
        print(f"{'¡Bienvenido, ' + self.user.username.upper() + '!':^50}")
        print(f"{'Puntos de Ranking: ' + str(self.user.puntos):^50}\n")
        print("  Opciones:")
        print("    [1] Crear Sala")
        print("    [2] Unirte a una Sala")
        print("    [3] Tienda")
        print("    [0] Cerrar Sesión\n")
        from src.utils.visuals import get_key
        print(f"{'='*50}")
        optionI = get_key()

        if optionI == '0':
            os.system('cls')
            self.logut()

        if optionI == '1':
            os.system('cls')
            self.createRoom()
        if optionI == '2':
            os.system('cls')
            self.joinRoom()
        if optionI == '3':
            os.system('cls')
            self.openShop()

    def openShop(self):
        from src.menus.menuShop import menuShop
        menuShop(self.user).mostrar()
    
    def logut(self):
        self.user = None
        os.system('cls')
    
    def createRoom(self):
        self.roomcr.user = self.user
        print(f"{'='*50}")
        print(f"{'CREAR SALA':^50}")
        print(f"{'='*50}\n")
        while True:
            name = input("  Nombre de la Sala (VACÍO para volver): ").strip()
            if not name:
                os.system('cls')
                return
            if len(name) > 20:
                print("  [!] El nombre es demasiado largo (máx 20 caracteres)")
                continue
            break
        self.roomsdb.createRoom(self.user.id, name)
        # Crear la batalla
        os.system('cls')
        print("\n  [+] Sala creada con éxito")
        time.sleep(2)
        room = self.roomsdb.getRoomUserActiva(self.user.id)
        self.battlesdb.createBattle(room.id)
        self.roomcr.combrobarRoomEspera(room)
        os.system('cls')
    
        from src.utils.visuals import get_key
        salas = self.roomsdb.getRoomActivos()
        while True:
            os.system('cls')
            if len(salas) == 0:
                print(f"{'='*50}")
                print(f"{'LISTA DE SALAS':^50}")
                print(f"{'='*50}\n")
                print("  [!] No hay salas disponibles\n")
                print("  Opciones:")
                print("    [0] Refrescar")
                print("    [X] Volver\n")
                print(f"{'='*50}")
                option = get_key()
                if option == 'x': break
                if option == '0':
                    salas = self.roomsdb.getRoomActivos()
                    continue
            else:
                print(f"{'='*50}")
                print(f"{'SALAS DISPONIBLES':^50}")
                print(f"{'='*50}\n")
                for i, sala in enumerate(salas):
                    print(f"  [{i+1}] - {sala.nombre}")
                
                print("\n  [0] Refrescar")
                print("  [X] Volver\n")
                print(f"{'='*50}")
                option = get_key()

                if option == 'x': break
                if option == '0':
                    salas = self.roomsdb.getRoomActivos()
                    continue
                
                try:
                    num_opt = int(option)
                    if 1 <= num_opt <= len(salas):
                        sala = salas[num_opt - 1]
                        sala.enemigo_id = self.user.id
                        self.roomsdb.updateRoom(sala)
                        self.roomcr.combrobarRoomEspera(sala)
                        break
                except:
                    pass
        os.system('cls')
        
        os.system('cls')
