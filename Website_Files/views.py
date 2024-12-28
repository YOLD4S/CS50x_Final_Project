from flask import (
    Flask, 
    render_template,
    request, 
    session, 
    flash, 
    redirect, 
    url_for, 
    abort,
    current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db


def home_page():
    return render_template("home.html")



def login_page():
    # Redirect if user is already logged in
    if session.get('user_id'):
        return redirect(url_for('home_page'))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Add input validation
        if not username or not password:
            flash("Please provide both username and password.", "error")
            return render_template("login.html")
            
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                flash("You have been logged in successfully!", "success")
                return redirect(url_for("home_page"))
            
            flash("Invalid username or password.", "error")
        except Exception as e:
            flash("An error occurred during login. Please try again.", "error")
            print(f"Login error: {str(e)}")  # For debugging
            
    return render_template("login.html")


def logout_page():
    session.clear()
    flash("You have been logged out successfully!", "success")
    return redirect(url_for("home_page"))

def register_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        if not username or not password or not password_confirm:
            flash("All fields are required.", "error")
        elif password != password_confirm:
            flash("Passwords do not match.", "error")
        else:
            db = get_db()
            cursor = db.cursor()
            query = """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """
            cursor.execute(query, (username, generate_password_hash(password)))
            db.commit()
            flash("You have been registered successfully!", "success")
            return redirect(url_for("login_page"))
    return render_template("register.html")

def items_page():
    return render_template("items.html")

def item_detail_page(item_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if not item:
        abort(404)
    return render_template("item_detail.html", item=item)

def item_page(item_key):
    db_items = current_app.config["db_items"]
    item = db_items.get_item(item_key)
    if item is None:
        abort(404)
    return render_template("item.html", item=item)

def add_new_npc():
    if request.method == "POST":
        name = request.form.get("name")
        hp = request.form.get("hp")
        runes = request.form.get("runes")
        location_id = request.form.get("location_id") or 0 
        only_night = request.form.get("only_night") == "on"

        try:
            if not name or not hp or not runes:
                flash("All fields except Location ID are required.", "error")
                return render_template("add_npc.html")

            db = get_db()
            cursor = db.cursor()
            query = """
                INSERT INTO npc_encounters (name, hp, runes, location_id, only_night)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, hp, runes, location_id, only_night))
            db.commit()
            flash("NPC added successfully!", "success")
            return redirect(url_for("npcs_page"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return render_template("add_npc.html")

    return render_template("npcs.html")


def add_npc():

    return render_template("add_npc.html")


def npcs_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM npc_encounters ORDER BY name ASC")
    npcs = cursor.fetchall()
    return render_template("npcs.html", npcs=npcs)

def npc_detail_page(npc_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM npcs WHERE id = %s", (npc_id,))
    npc = cursor.fetchone()
    if not npc:
        abort(404)
    return render_template("npc_detail.html", npc=npc)

def npc_page(npc_key): # may remove this later
    db_npcs = current_app.config["db_npcs"]
    npc = db_npcs.get_npc(npc_key)
    if npc is None:
        abort(404)
    return render_template("npc.html", npc=npc)


def weapons_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM weapons ORDER BY name ASC")
    weapons = cursor.fetchall()
    return render_template("weapons.html", weapons=weapons)

def weapon_detail_page(weapon_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM weapons WHERE id = %s", (weapon_id,))
    weapon = cursor.fetchone()
    if not weapon:
        abort(404)
    return render_template("weapon_detail.html", weapon=weapon)


def armors_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM armors ORDER BY name ASC")
    armors = cursor.fetchall()
    return render_template("armors.html", armors=armors)

def armor_detail_page(armor_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM armors WHERE id = %s", (armor_id,))
    armor = cursor.fetchone()
    if not armor:
        abort(404)
    return render_template("armor_detail.html", armor=armor)

def talismans_page():
    return render_template("talismans.html")

def magic_page():
    return render_template("magic.html")

def spirits_page():
    return render_template("spirits.html")

def keys_page():
    return render_template("keys.html")

def bolstering_page():
    return render_template("bolstering.html")
