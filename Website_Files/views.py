from datetime import datetime

from flask import abort, current_app, render_template
from db import get_db


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def items_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template("items.html", items=items)


def item_page(item_key):
    db_items = current_app.config["db_items"]
    item = db_items.get_item(item_key)
    if item is None:
        abort(404)
    return render_template("item.html", item=item)


def npcs_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM npcs")
    npcs = cursor.fetchall()
    return render_template("npcs.html", npcs=npcs)


def npc_page(npc_key):
    db_npcs = current_app.config["db_npcs"]
    npc = db_npcs.get_npc(npc_key)
    if npc is None:
        abort(404)
    return render_template("npc.html", npc=npc)

def weapons_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM weapons")
    weapons = cursor.fetchall()
    return render_template("weapons.html", weapons=weapons)


def armors_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM armors")
    armors = cursor.fetchall()
    return render_template("armors.html", armors=armors)
