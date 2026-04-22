import time
from src.database.rooms import rooms
from src.Controllers.roomController import roomController
from src.database.battles import battles
from src.utils.clear_screen import clear_screen
from src.Controllers.matchmakingController import MatchmakingController

class menuLogin:

    user = None

    def __init__(self):
        self.roomsdb = rooms()
        self.roomcr = roomController()
        self.battlesdb = battles()
        self.matchmaking = MatchmakingController()
        clear_screen()

    def inicio(self):
        clear_screen()
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
        print("    [3] Buscar Partida")
        print("    [4] Tienda")
        print("    [5] Mi Equipo")
        print("    [0] Cerrar Sesión\n")
        from src.utils.visuals import get_key
        print(f"{'='*50}")
        optionI = get_key()

        if optionI == '0':
            clear_screen()
            self.logout()

        if optionI == '1':
            clear_screen()
            self.createRoom()
        if optionI == '2':
            clear_screen()
            self.joinRoom()
        if optionI == '3':
            clear_screen()
            self.searchMatch()
        if optionI == '4':
            clear_screen()
            self.openShop()
        if optionI == '5':
            clear_screen()
            self.openMyTeam()

    def openShop(self):
        from src.menus.menuShop import menuShop
        menuShop(self.user).mostrar()

    def openMyTeam(self):
        from src.menus.menuMyTeam import menuMyTeam
        menuMyTeam(self.user).manage()

    def logout(self):
        self.user = None
        clear_screen()

    def createRoom(self):
        self.roomcr.user = self.user
        print(f"{'='*50}")
        print(f"{'CREAR SALA':^50}")
        print(f"{'='*50}\n")
        while True:
            name = input("  Nombre de la Sala (VACÍO para volver): ").strip()
            if not name:
                clear_screen()
                return
            if len(name) > 20:
                print("  [!] El nombre es demasiado largo (máx 20 caracteres)")
                continue
            break
        self.roomsdb.createRoom(self.user.id, name)
        # Crear la batalla
        clear_screen()
        print("\n  [+] Sala creada con éxito")
        time.sleep(2)
        room = self.roomsdb.getRoomUserActiva(self.user.id)
        self.battlesdb.createBattle(room.id)
        self.roomcr.combrobarRoomEspera(room)
        clear_screen()

        self.joinRoom()

    def joinRoom(self):
        from src.utils.visuals import get_key
        self.roomcr.user = self.user
        salas = self.roomsdb.getRoomActivos()
        while True:
            clear_screen()
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
        clear_screen()

    def searchMatch(self):
        """Handle matchmaking queue entry."""
        from src.utils.visuals import get_key
        from src.utils.clear_screen import clear_screen
        import time

        print(f"{'='*50}")
        print(f"{'BUSCAR PARTIDA':^50}")
        print(f"{'='*50}\n")

        success, message, entry_id = self.matchmaking.join_queue(self.user)

        if not success:
            print(f"  [!] {message}\n")
            print("  Presiona cualquier tecla para volver...")
            get_key()
            return

        print(f"  [+] {message}")
        print("  Timer: 0s\n")
        print("  Opciones:")
        print("    [C] Cancelar\n")
        print(f"{'='*50}")

        start_time = time.time()
        while True:
            elapsed = int(time.time() - start_time)
            # Re-print with updated timer
            print(f"\r  Buscando... {elapsed}s", end="", flush=True)

            # Try to find a match for this entry (Python-side matching instead of Edge Function)
            rating = getattr(self.user, 'puntos', 0)
            match_result = self.matchmaking.try_match(entry_id, str(self.user.id), rating)

            if match_result:
                room_id = match_result
                print(f"\n\n  [!] ¡Partida encontrada! Room ID: {room_id}")
                print("  Presiona cualquier tecla para continuar...")
                get_key()
                # Transition to combat
                self._enter_match_combat(room_id)
                return

            # Also check if we were already matched by another player's try_match
            # (our queue entry might have room_id set by another player's find_match)
            status = self.matchmaking.get_status(self.user)
            if status and status.room_id:
                room_id = int(status.room_id)
                print(f"\n\n  [!] ¡Partida encontrada! Room ID: {room_id}")
                print("  Presiona cualquier tecla para continuar...")
                get_key()
                # Transition to combat
                self._enter_match_combat(room_id)
                return

            # Check if there's a room waiting for us where we are the enemy
            pending_room = self.matchmaking.get_pending_room_for_user(self.user.id)
            if pending_room:
                room_id = int(pending_room.id)
                print(f"\n\n  [!] ¡Partida encontrada! Room ID: {room_id}")
                print("  Presiona cualquier tecla para continuar...")
                get_key()
                # Transition to combat
                self._enter_match_combat(room_id)
                return

            # Check for key press (non-blocking)
            from src.utils.visuals import get_key_timeout
            key = get_key_timeout(timeout=1)
            if key and key.lower() == 'c':
                self.matchmaking.leave_queue(self.user)
                print("\n  [-] Búsqueda cancelada")
                time.sleep(1)
                return

            # Check timeout
            if elapsed >= 60:
                self.matchmaking.leave_queue(self.user)
                print("\n\n  [!] No se encontró rival. Intenta crear una sala.")
                time.sleep(2)
                return
        
        # If we exit loop without match, just return
        print()
    
    def _enter_match_combat(self, room_id):
        """Transition to combat after a match is found."""
        from src.Controllers.roomController import roomController
        from src.utils.visuals import get_key
        print(f"\n  [DEBUG] Entering match combat, room_id={room_id}")
        room = self.roomsdb.getRoom(room_id)
        if room:
            print(f"  [DEBUG] Room found: estado={room.estado}, user_id={room.user_id}, enemigo_id={room.enemigo_id}")
            self.roomcr.user = self.user
            self.roomcr.combrobarRoomEspera(room)
        else:
            print(f"  [DEBUG] Room not found for room_id={room_id}")
        print("  [DEBUG] Presiona tecla para volver al menu...")
        get_key()
        clear_screen()