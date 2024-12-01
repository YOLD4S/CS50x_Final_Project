from flask import Flask

import views
from database import ItemDatabase, NPCDatabase
from elements import Item, NPC


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/items", view_func=views.items_page)
    app.add_url_rule("/items/<int:item_key>", view_func=views.item_page)
    app.add_url_rule("/npcs", view_func=views.npcs_page)
    app.add_url_rule("/npcs/<int:npc_key>", view_func=views.npc_page)

    db_item = ItemDatabase()
    db_item.add_item(Item("Slaughterhouse-Five", year=1972))
    db_item.add_item(Item("The Shining"))
    app.config["db_items"] = db_item

    db_npc = NPCDatabase()
    db_npc.add_npc(NPC("AlihanSN", 100, True, 123, "images/SN.png"))
    app.config["db_npcs"] = db_npc



    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)