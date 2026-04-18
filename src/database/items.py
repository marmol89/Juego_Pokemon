from src.database.db import db
from src.models.item import item

class items:
    def __init__(self):
        self.dbp = db().get_connection()

    def getItemsShop(self):
        if not self.dbp: return []
        data = self.dbp.table("items").select("*").execute()
        return [item(r['id'], r['nombre'], r['descripcion'], r['precio'], r['efecto']) for r in data.data]

    def getUserItems(self, user_id):
        if not self.dbp: return []
        # Join con la tabla items para tener los nombres y efectos
        data = self.dbp.table("user_items").select("*, items(*)").eq("user_id", user_id).execute()
        
        inventory = []
        for row in data.data:
            item_data = row['items']
            obj = item(item_data['id'], item_data['nombre'], item_data['descripcion'], item_data['precio'], item_data['efecto'])
            inventory.append({
                "item": obj,
                "cantidad": row['cantidad'],
                "user_item_id": row['id']
            })
        return inventory

    def buyItem(self, user, item_obj):
        if not self.dbp: return False
        if user.puntos < item_obj.precio:
            return False

        # Descontar puntos
        nuevos_puntos = user.puntos - item_obj.precio
        from src.database.users import users
        users().updatePuntos(user.id, nuevos_puntos)

        # Añadir al inventario
        existing = self.dbp.table("user_items").select("*").eq("user_id", user.id).eq("item_id", item_obj.id).execute()
        
        if len(existing.data) > 0:
            current_qty = existing.data[0]['cantidad']
            self.dbp.table("user_items").update({"cantidad": current_qty + 1}).eq("id", existing.data[0]['id']).execute()
        else:
            self.dbp.table("user_items").insert({"user_id": user.id, "item_id": item_obj.id, "cantidad": 1}).execute()
        
        return True

    def consumeItem(self, user_id, item_id):
        if not self.dbp: return
        data = self.dbp.table("user_items").select("*").eq("user_id", user_id).eq("item_id", item_id).execute()
        if len(data.data) > 0:
            qty = data.data[0]['cantidad']
            if qty > 1:
                self.dbp.table("user_items").update({"cantidad": qty - 1}).eq("id", data.data[0]['id']).execute()
            else:
                self.dbp.table("user_items").delete().eq("id", data.data[0]['id']).execute()
