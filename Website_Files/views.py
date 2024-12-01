from datetime import datetime

from flask import abort, current_app, render_template


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def items_page():
    db_items = current_app.config["db_items"]
    items = db_items.get_items()
    return render_template("items.html", items=sorted(items))


def item_page(item_key):
    db_items = current_app.config["db_items"]
    item = db_items.get_item(item_key)
    if item is None:
        abort(404)
    return render_template("item.html", item=item)


def npcs_page():
    db_npcs = current_app.config["db_npcs"]
    npcs = db_npcs.get_npcs()
    return render_template("npcs.html", npcs=sorted(npcs))


def npc_page(npc_key):
    db_NPC = current_app.config["db_NPC"]
    npc = db_NPC.get_npc(npc_key)
    if npc is None:
        abort(404)
    return render_template("npc.html", npc=npc)