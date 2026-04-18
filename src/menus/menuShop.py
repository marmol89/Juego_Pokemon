import os
import time
from src.database.items import items

class menuShop:
    def __init__(self, user):
        self.user = user
        self.itemsdb = items()
        os.system('cls')
    
    def mostrar(self):
        while True:
            os.system('cls')
            # Recargar usuario para ver puntos actuales
            from src.database.users import users
            self.user = users().getUser(self.user.id)
            
            catalog = self.itemsdb.getItemsShop()
            inventory = self.itemsdb.getUserItems(self.user.id)
            
            print(f"{'='*70}")
            print(f"{'TIENDA POKÉMON':^70}")
            print(f"{'='*70}")
            print(f"{'Saldo: ' + str(self.user.puntos) + ' puntos':^70}\n")
            
            print(f"  {'ID':<4} {'OBJETO':<20} {'PRECIO':<10} {'DESCRIPCIÓN'}")
            print(f"  {'-'*66}")
            
            for item in catalog:
                print(f"  [{item.id:<2}] {item.nombre:<20} {str(item.precio) + ' pts':<10} {item.descripcion}")
            
            print(f"\n  {'-'*66}")
            print("\n  Tu Inventario:")
            if not inventory:
                print("    (Vacío)")
            else:
                for inv in inventory:
                    print(f"    - {inv['item'].nombre} x{inv['cantidad']}")
            
            print(f"\n{'='*70}")
            print("  [ID] Comprar objeto  [0] Salir")
            print(f"{'='*70}")
            
            from src.utils.visuals import get_key
            choice = get_key()
            
            if choice == "0":
                break
            
            selected = next((i for i in catalog if str(i.id) == choice), None)
            if selected:
                if self.itemsdb.buyItem(self.user, selected):
                    print(f"\n  [+] ¡Has comprado {selected.nombre.upper()}!")
                else:
                    print("\n  [!] No tienes suficientes puntos.")
                time.sleep(1.5)
            else:
                pass
