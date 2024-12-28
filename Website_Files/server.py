from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import views
from database import ItemDatabase, NPCDatabase
from elements import Item, NPC
from db import get_db, close_db


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    
    # Add these session configurations
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    # Configure secret key for session management
    app.secret_key = 'your-secret-key-here'  # Replace with a secure secret key
    
    app.teardown_appcontext(close_db)

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
    app.add_url_rule("/items", view_func=views.items_page)
    app.add_url_rule("/items/<int:item_key>", view_func=views.item_page)
    app.add_url_rule("/npcs", view_func=views.npcs_page, methods=["GET", "POST"])
    app.add_url_rule("/add_npc", view_func=views.add_npc)
    app.add_url_rule("/add_new_npc", view_func=views.add_new_npc, methods=["GET", "POST"])
    app.add_url_rule("/npcs/<int:npc_key>", view_func=views.npc_page)
    app.add_url_rule("/weapons", view_func=views.weapons_page)
    app.add_url_rule("/armors", view_func=views.armors_page)
    app.add_url_rule("/npcs/<int:npc_id>", view_func=views.npc_detail_page)
    app.add_url_rule("/items/<int:item_id>", view_func=views.item_detail_page)
    app.add_url_rule("/weapons/<int:weapon_id>", view_func=views.weapon_detail_page)
    app.add_url_rule("/armors/<int:armor_id>", view_func=views.armor_detail_page)
    app.add_url_rule("/talismans", view_func=views.talismans_page)
    app.add_url_rule("/magic", view_func=views.magic_page)
    app.add_url_rule("/spirits", view_func=views.spirits_page)
    app.add_url_rule("/keys", view_func=views.keys_page)
    app.add_url_rule("/bolstering", view_func=views.bolstering_page)

    db_item = ItemDatabase()
    db_item.add_item(Item("Slaughterhouse-Five", year=1972))
    db_item.add_item(Item("The Shining"))
    app.config["db_items"] = db_item

    db_npc = NPCDatabase()
    db_npc.add_npc(NPC("AlihaSN", 10, False, 13, False))
    db_npc.add_npc(NPC("AlihanSN", 100, True, 123, False))
    db_npc.add_npc(NPC("AlihaSN", 10, False, 13, True))
    db_npc.add_npc(NPC("AlihanSN", 100, True, 123, True))
    app.config["db_npcs"] = db_npc



    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)