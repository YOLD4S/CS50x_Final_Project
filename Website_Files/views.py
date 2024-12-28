from functools import wraps
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


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function


def is_logged_in():
    return session.get('user_id') is not None


def home_page():
    logged_in = is_logged_in()
    return render_template("home.html", logged_in=logged_in)



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
    
    # Get filter parameters
    location_id = request.args.get('location')
    only_night = request.args.get('only_night')
    
    # Base query
    query = """
        SELECT n.*, l.name as location_name 
        FROM npc_encounters n 
        LEFT JOIN locations l ON n.location_id = l.id 
        WHERE 1=1
    """
    params = []
    
    # Add filters
    if location_id:
        query += " AND n.location_id = %s"
        params.append(location_id)
    if only_night is not None:
        query += " AND n.only_night = %s"
        params.append(only_night == '1')
    
    query += " ORDER BY n.name ASC"
    
    # Execute main query
    cursor.execute(query, params)
    npcs = cursor.fetchall()
    
    # Get locations for filter dropdown
    cursor.execute("SELECT id, name FROM locations ORDER BY name ASC")
    locations = cursor.fetchall()
    
    return render_template("npcs.html", 
                         npcs=npcs,
                         locations=locations,
                         selected_location=location_id,
                         only_night=only_night)

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

    # Fetch weapon groups
    cursor.execute("SELECT id, name FROM weapon_groups")
    groups = cursor.fetchall()

    # Fetch weapons, sorted alphabetically, with group association
    cursor.execute("SELECT id, name, image_url, group_id FROM weapons ORDER BY name ASC")
    weapons = cursor.fetchall()

    # Organize weapons by group
    weapons_by_group = {group['id']: [] for group in groups}
    for weapon in weapons:
        weapons_by_group[weapon['group_id']].append(weapon)

    return render_template("weapons.html", groups=groups, weapons_by_group=weapons_by_group)

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
    
    # Get filter parameters
    set_id = request.args.get('set_id')
    slot_id = request.args.get('slot_id')
    weight_order = request.args.get('weight_order')
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of armors per page
    
    # Base query
    query = """
        SELECT a.*, s.name as set_name, e.equip_slot 
        FROM armors a 
        LEFT JOIN armor_sets s ON a.set_id = s.id 
        LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id 
        WHERE 1=1
    """
    count_query = "SELECT COUNT(*) as total FROM armors WHERE 1=1"
    params = []
    
    # Add filters
    if set_id:
        query += " AND a.set_id = %s"
        count_query += " AND set_id = %s"
        params.append(set_id)
    if slot_id:
        query += " AND a.equip_slot_id = %s"
        count_query += " AND equip_slot_id = %s"
        params.append(slot_id)
    
    # Add ordering
    if weight_order == 'asc':
        query += " ORDER BY a.weight ASC"
    elif weight_order == 'desc':
        query += " ORDER BY a.weight DESC"
    else:
        query += " ORDER BY s.name, e.equip_slot"
    
    # Get total count for pagination
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page
    
    # Add pagination
    query += " LIMIT %s OFFSET %s"
    offset = (page - 1) * per_page
    params.extend([per_page, offset])
    
    # Execute main query
    cursor.execute(query, params)
    armors = cursor.fetchall()
    
    # Get filter dropdowns
    cursor.execute("SELECT id, name FROM armor_sets ORDER BY name")
    sets = cursor.fetchall()
    
    cursor.execute("SELECT id, equip_slot FROM armor_equip_slots ORDER BY id")
    slots = cursor.fetchall()
    
    return render_template("armors.html", 
                         armors=armors,
                         sets=sets,
                         slots=slots,
                         selected_set=set_id,
                         selected_slot=slot_id,
                         weight_order=weight_order,
                         current_page=page,
                         total_pages=total_pages)

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

