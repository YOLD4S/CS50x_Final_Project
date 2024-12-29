from functools import wraps
from datetime import datetime
import os

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
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch existing encounters and locations for dropdowns
    cursor.execute("SELECT id, name FROM npc_encounters")
    encounters = cursor.fetchall()

    cursor.execute("SELECT id, name FROM locations")
    locations = cursor.fetchall()

    # Fetch weapons and armors using the appropriate joins
    cursor.execute("""
        SELECT 
    rw.name AS weapon_name,
    rw.id AS weapon_order_id,
    MIN(rw_aff.id) AS weapon_affinity_id -- Select the first affinity ID (or other logic)
FROM 
    weapons AS rw     
LEFT JOIN weapons_w_affinities AS rw_aff ON rw.id = rw_aff.main_weapon_id
GROUP BY rw.id, rw.name

    """)
    weapons = cursor.fetchall()

    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 1
    """)
    h_armors = cursor.fetchall()
    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 2
    """)
    b_armors = cursor.fetchall()
    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 3
    """)
    a_armors = cursor.fetchall()
    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 4
    """)
    l_armors = cursor.fetchall()

    if request.method == 'POST':
        # Fetch NPC data
        name = request.form.get('name')
        hp = request.form.get('hp')
        human = request.form.get('human') == 'on'
        add_to_existing_encounter = request.form.get('add_to_existing_encounter') == 'on'
        encounter_id = request.form.get('encounter_id') if add_to_existing_encounter else None
        new_encounter_name = request.form.get('new_encounter_name') or name
        new_encounter_hp = request.form.get('new_encounter_hp')
        new_encounter_runes = request.form.get('new_encounter_runes')

        # Fetch gear and location data
        location_id = request.form.get('location_id')
        right_weapon_id = request.form.get('right_weapon_id')
        left_weapon_id = request.form.get('left_weapon_id')
        armor_head_id = request.form.get('armor_head_id')
        armor_body_id = request.form.get('armor_body_id')
        armor_arms_id = request.form.get('armor_arms_id')
        armor_legs_id = request.form.get('armor_legs_id')

        # Handle encounter logic
        if not add_to_existing_encounter:
            # Create new encounter
            cursor.execute("""
                INSERT INTO npc_encounters (name, hp, runes, location_id)
                VALUES (%s, %s, %s, %s)
            """, (new_encounter_name, new_encounter_hp or 0, new_encounter_runes or 0, location_id))
            encounter_id = cursor.lastrowid
        else:
            # Update existing encounter HP
            cursor.execute("""
                SELECT hp FROM npc_encounters WHERE id = %s
            """, (encounter_id,))
            existing_encounter = cursor.fetchone()
            if existing_encounter:
                existing_hp = existing_encounter['hp']
                updated_hp = existing_hp + int(hp or 0)
                cursor.execute("""
                    UPDATE npc_encounters
                    SET hp = %s
                    WHERE id = %s
                """, (updated_hp, encounter_id))

        # Insert NPC gear into gear table
        cursor.execute("""
            INSERT INTO gear (right_weapon_id, left_weapon_id, armor_head_id, armor_body_id, armor_arms_id, armor_legs_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (right_weapon_id, left_weapon_id, armor_head_id, armor_body_id, armor_arms_id, armor_legs_id))
        gear_id = cursor.lastrowid

        # Insert NPC data
        cursor.execute("""
            INSERT INTO npcs (name, hp, human, encounter_id, gear_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, hp, human, encounter_id, gear_id))

        db.commit()

        return redirect(url_for('npc_detail_page', npc_id=cursor.lastrowid))

    return render_template(
        'add_npc.html', 
        encounters=encounters, 
        locations=locations, 
        weapons=weapons, 
        h_armors=h_armors,
        b_armors=b_armors,
        a_armors=a_armors,
        l_armors=l_armors,
        
    )
    
    
def delete_npc(npc_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM npcs WHERE id = %s", (npc_id,))
    db.commit()
    flash("NPC deleted successfully!", "success")
    return redirect(url_for('npcs_page'))

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

    # Fetch NPC details along with associated encounter, gear, and item details
    cursor.execute("""
        SELECT 
            npcs.*, 
            npc_encounters.name AS encounter_name,
            npc_encounters.hp AS encounter_hp,
            npc_encounters.runes AS encounter_runes,
            npc_encounters.only_night AS encounter_only_night,
            locations.name AS location_name,
            gear.right_weapon_id,
            gear.right_weapon_skill_id,
            gear.left_weapon_id,
            gear.left_weapon_skill_id,
            gear.armor_head_id,
            gear.armor_body_id,
            gear.armor_arms_id,
            gear.armor_legs_id,
            items.name AS dropped_item_name
        FROM 
            npcs
        LEFT JOIN 
            npc_encounters ON npcs.encounter_id = npc_encounters.id
        LEFT JOIN 
            locations ON npc_encounters.location_id = locations.id
        LEFT JOIN 
            gear ON npcs.gear_id = gear.id
        LEFT JOIN 
            items ON npcs.dropped_item_id = items.id
        WHERE 
            npcs.id = %s
    """, (npc_id,))
    npc = cursor.fetchone()

    if not npc:
        abort(404)

    # Handle case where gear_id is null
    gear_id = npc.get("gear_id")
    if gear_id:
        # Fetch detailed gear information (weapons, weapons_w_affinities, and armors)
        cursor.execute("""
            SELECT 
                rw_aff.main_weapon_id AS right_weapon_main_id,
                rw.name AS right_weapon_name,
                rws.name AS right_weapon_skill_name,
                lw_aff.main_weapon_id AS left_weapon_main_id,
                lw.name AS left_weapon_name,
                lws.name AS left_weapon_skill_name,
                head.id AS head_armor_id,
                items_head.name AS head_armor_name,
                body.id AS body_armor_id,
                items_body.name AS body_armor_name,
                arms.id AS arms_armor_id,
                items_arms.name AS arms_armor_name,
                legs.id AS legs_armor_id,
                items_legs.name AS legs_armor_name
            FROM 
                gear
            LEFT JOIN weapons_w_affinities AS rw_aff ON gear.right_weapon_id = rw_aff.id
            LEFT JOIN weapons AS rw ON rw_aff.main_weapon_id = rw.id
            LEFT JOIN weapon_skills AS rws ON gear.right_weapon_skill_id = rws.id
            LEFT JOIN weapons_w_affinities AS lw_aff ON gear.left_weapon_id = lw_aff.id
            LEFT JOIN weapons AS lw ON lw_aff.main_weapon_id = lw.id
            LEFT JOIN weapon_skills AS lws ON gear.left_weapon_skill_id = lws.id
            LEFT JOIN armors AS head ON gear.armor_head_id = head.id
            LEFT JOIN items AS items_head ON head.id = items_head.id
            LEFT JOIN armors AS body ON gear.armor_body_id = body.id
            LEFT JOIN items AS items_body ON body.id = items_body.id
            LEFT JOIN armors AS arms ON gear.armor_arms_id = arms.id
            LEFT JOIN items AS items_arms ON arms.id = items_arms.id
            LEFT JOIN armors AS legs ON gear.armor_legs_id = legs.id
            LEFT JOIN items AS items_legs ON legs.id = items_legs.id
            WHERE gear.id = %s
        """, (gear_id,))
        gear_details = cursor.fetchone()
    else:
        # No gear associated with the NPC
        gear_details = {
            "right_weapon_name": None,
            "right_weapon_skill_name": None,
            "left_weapon_name": None,
            "left_weapon_skill_name": None,
            "head_armor_name": None,
            "body_armor_name": None,
            "arms_armor_name": None,
            "legs_armor_name": None,
        }

    # Organize the fetched details into structured data for rendering
    npc_data = {
        "npc": npc,
        "gear": {
            "weapons": {
                "right_weapon": {
                    "name": gear_details.get("right_weapon_name"),
                    "skill": gear_details.get("right_weapon_skill_name"),
                },
                "left_weapon": {
                    "name": gear_details.get("left_weapon_name"),
                    "skill": gear_details.get("left_weapon_skill_name"),
                },
            },
            "armors": {
                "head": gear_details.get("head_armor_name"),
                "body": gear_details.get("body_armor_name"),
                "arms": gear_details.get("arms_armor_name"),
                "legs": gear_details.get("legs_armor_name"),
            },
        },
    }

    # Render template with detailed NPC data
    return render_template("npc_detail.html", npc=npc_data["npc"], gear_details=npc_data["gear"])


    gear_details = cursor.fetchone()
    
    # Organize the fetched details into structured data for rendering
    npc_data = {
        "npc": npc,
        "gear": {
            "weapons": {
                "right_weapon": {
                    "name": gear_details.get("right_weapon_name"),
                    "skill": gear_details.get("right_weapon_skill_name"),
                },
                "left_weapon": {
                    "name": gear_details.get("left_weapon_name"),
                    "skill": gear_details.get("left_weapon_skill_name"),
                },
            },
            "armors": {
                "head": gear_details.get("head_armor_name"),
                "body": gear_details.get("body_armor_name"),
                "arms": gear_details.get("arms_armor_name"),
                "legs": gear_details.get("legs_armor_name"),
            },
        },
    }
    print(gear_details)

    # Render template with detailed NPC data
    return render_template("npc_detail.html", npc=npc_data["npc"], gear_details=npc_data["gear"])




def npc_page(npc_key): # may remove this later
    db_npcs = current_app.config["db_npcs"]
    npc = db_npcs.get_npc(npc_key)
    if npc is None:
        abort(404)
    return render_template("npc.html", npc=npc)

def update_npc(npc_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch existing encounters and locations for dropdowns
    cursor.execute("SELECT id, name FROM npc_encounters")
    encounters = cursor.fetchall()

    cursor.execute("SELECT id, name FROM locations")
    locations = cursor.fetchall()

    # Fetch weapons and armors for dropdowns
    cursor.execute("""
        SELECT 
            rw.name AS weapon_name,
            rw.id AS weapon_order_id,
            MIN(rw_aff.id) AS weapon_affinity_id
        FROM 
            weapons AS rw     
        LEFT JOIN weapons_w_affinities AS rw_aff ON rw.id = rw_aff.main_weapon_id
        GROUP BY rw.id, rw.name
    """)
    weapons = cursor.fetchall()

    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 1
    """)
    h_armors = cursor.fetchall()
    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 2
    """)
    b_armors = cursor.fetchall()
    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 3
    """)
    a_armors = cursor.fetchall()
    cursor.execute("""
        SELECT 
            armors.id AS armor_id,
            items.name AS armor_name,
            armors.equip_slot_id
        FROM 
            armors 
        LEFT JOIN items ON armors.id = items.id
        WHERE armors.equip_slot_id = 4
    """)
    l_armors = cursor.fetchall()

    # Fetch NPC and related encounter details for pre-filling the form
    cursor.execute("""
        SELECT 
            npcs.*, 
            npc_encounters.name AS encounter_name,
            npc_encounters.hp AS encounter_hp,
            npc_encounters.runes AS encounter_runes,
            npc_encounters.only_night AS encounter_only_night,
            npc_encounters.location_id AS encounter_location_id,
            gear.right_weapon_id,
            gear.left_weapon_id,
            gear.armor_head_id,
            gear.armor_body_id,
            gear.armor_arms_id,
            gear.armor_legs_id
        FROM 
            npcs
        LEFT JOIN npc_encounters ON npcs.encounter_id = npc_encounters.id
        LEFT JOIN gear ON npcs.gear_id = gear.id
        WHERE npcs.id = %s
    """, (npc_id,))
    npc = cursor.fetchone()

    if not npc:
        abort(404)

    # Handle POST request to update NPC
    if request.method == 'POST':
        # NPC and encounter details
        name = request.form.get('name')
        hp = request.form.get('hp')
        runes = request.form.get('runes')
        encounter_id = request.form.get('encounter_id')
        location_id = request.form.get('location_id')  # Updates the `npc_encounters` table
        only_night = request.form.get('only_night') == 'on'

        # Gear details
        right_weapon_id = request.form.get('right_weapon_id')
        left_weapon_id = request.form.get('left_weapon_id')
        armor_head_id = request.form.get('armor_head_id')
        armor_body_id = request.form.get('armor_body_id')
        armor_arms_id = request.form.get('armor_arms_id')
        armor_legs_id = request.form.get('armor_legs_id')

        # Update encounter details
        cursor.execute("""
            UPDATE npc_encounters
            SET name = %s, hp = %s, runes = %s, location_id = %s, only_night = %s
            WHERE id = %s
        """, (name, hp, runes, location_id, only_night, encounter_id))

        # Check if the NPC already has gear
        gear_id = npc.get('gear_id')
        if right_weapon_id or left_weapon_id or armor_head_id or armor_body_id or armor_arms_id or armor_legs_id:
            if gear_id:
                # Update existing gear
                cursor.execute("""
                    UPDATE gear
                    SET right_weapon_id = %s, left_weapon_id = %s, 
                        armor_head_id = %s, armor_body_id = %s, 
                        armor_arms_id = %s, armor_legs_id = %s
                    WHERE id = %s
                """, (right_weapon_id, left_weapon_id, armor_head_id, armor_body_id, armor_arms_id, armor_legs_id, gear_id))
            else:
                # Create new gear and update the NPC's gear_id
                cursor.execute("""
                    INSERT INTO gear (right_weapon_id, left_weapon_id, armor_head_id, armor_body_id, armor_arms_id, armor_legs_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (right_weapon_id, left_weapon_id, armor_head_id, armor_body_id, armor_arms_id, armor_legs_id))
                gear_id = cursor.lastrowid
                cursor.execute("""
                    UPDATE npcs
                    SET gear_id = %s
                    WHERE id = %s
                """, (gear_id, npc_id))

        # Update the NPC details
        cursor.execute("""
            UPDATE npcs
            SET name = %s, hp = %s, encounter_id = %s
            WHERE id = %s
        """, (name, hp, encounter_id, npc_id))

        db.commit()
        flash("NPC updated successfully!", "success")
        return redirect(url_for('npc_detail_page', npc_id=npc_id))

    return render_template(
        'update_npc.html', 
        npc=npc, 
        encounters=encounters, 
        locations=locations, 
        weapons=weapons, 
        h_armors=h_armors,
        b_armors=b_armors,
        a_armors=a_armors,
        l_armors=l_armors
    )






def weapon_groups_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch all weapon groups
    cursor.execute("""
            SELECT wg.id, wg.name, 
                   (SELECT image_url 
                    FROM weapons 
                    WHERE group_id = wg.id AND image_url IS NOT NULL AND image_url != ''
                    ORDER BY RAND() LIMIT 1) AS random_image
            FROM weapon_groups wg
        """)
    groups = cursor.fetchall()

    # Fetch 4 random weapons for the "All Weapons" box
    cursor.execute("""
            SELECT image_url
            FROM weapons
            WHERE image_url IS NOT NULL AND image_url != ''
            ORDER BY RAND()
            LIMIT 4
        """)
    all_weapons_images = cursor.fetchall()

    return render_template("weapon_groups.html", groups=groups, all_weapons_images=all_weapons_images)


def individual_group_page(group_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get the current page from the request, default to 1
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    # Fetch total weapon count for the group
    cursor.execute("SELECT COUNT(*) AS total FROM weapons WHERE group_id = %s", (group_id,))
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Fetch weapons for the current page
    cursor.execute("""
            SELECT id, name, image_url
            FROM weapons
            WHERE group_id = %s
            ORDER BY name ASC
            LIMIT %s OFFSET %s
        """, (group_id, per_page, offset))
    weapons = cursor.fetchall()

    # Fetch the group name
    cursor.execute("SELECT id, name FROM weapon_groups WHERE id = %s", (group_id,))
    group = cursor.fetchone()

    if not group:
        abort(404)

    return render_template(
        "individual_group.html",
        group=group,
        weapons=weapons,
        current_page=page,  # Pass current_page explicitly
        total_pages=total_pages
    )


def all_weapons_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get the current page from the request, default to 1
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    # Fetch total weapon count for pagination
    cursor.execute("SELECT COUNT(*) AS total FROM weapons")
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page  # Calculate total pages

    # Fetch weapons for the current page
    cursor.execute("""
            SELECT id, name, image_url
            FROM weapons
            ORDER BY name ASC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
    weapons = cursor.fetchall()

    return render_template(
        "all_weapons.html",
        weapons=weapons,
        current_page=page,  # Pass current_page explicitly
        total_pages=total_pages
    )


def weapons_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch weapon groups
    cursor.execute("SELECT id, name FROM weapon_groups")
    groups = cursor.fetchall()

    # Get filter parameters from the request
    selected_groups = request.args.getlist("group_id")

    # Base query for weapons
    query = """
            SELECT id, name, image_url, group_id 
            FROM weapons
        """
    params = []

    # Add filtering conditions
    if selected_groups:
        query += " WHERE group_id IN (%s)" % ",".join(["%s"] * len(selected_groups))
        params.extend(selected_groups)

    query += " ORDER BY name ASC"

    # Fetch weapons based on filters
    cursor.execute(query, params)
    weapons = cursor.fetchall()

    # Organize weapons by group
    weapons_by_group = {group['id']: [] for group in groups}
    for weapon in weapons:
        weapons_by_group[weapon['group_id']].append(weapon)

    return render_template(
        "weapons.html",
        groups=groups,
        weapons_by_group=weapons_by_group,
        selected_groups=selected_groups
    )

def weapon_detail_page(weapon_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch the weapon details
    cursor.execute("""
            SELECT w.id, w.name, w.description, w.weight, w.image_url, 
                   w.group_id, g.name AS group_name, 
                   e1.description AS passive_effect, 
                   e2.description AS hidden_effect, 
                   ws.name AS skill
            FROM weapons w
            JOIN weapon_groups g ON w.group_id = g.id
            LEFT JOIN effects e1 ON w.weapon_passive_id = e1.id
            LEFT JOIN effects e2 ON w.hidden_effect_id = e2.id
            LEFT JOIN weapon_skills ws ON w.default_skill_id = ws.id
            WHERE w.id = %s
        """, (weapon_id,))
    weapon = cursor.fetchone()

    if not weapon:
        abort(404)

    # Fetch requirements
    cursor.execute("""
            SELECT req_str, req_dex, req_int, req_fai, req_arc
            FROM weapons
            WHERE id = %s
        """, (weapon_id,))
    requirements = cursor.fetchone()

    # Fetch affinities
    cursor.execute("""
            SELECT a.name AS affinity_name, 
                   a.affinity_passive_id,
                   wwa.str_scaling, wwa.dex_scaling, 
                   wwa.int_scaling, wwa.fai_scaling, wwa.arc_scaling,
                   e.description AS affinity_passive
            FROM weapons_w_affinities wwa
            LEFT JOIN affinities a ON wwa.affinity_id = a.id
            LEFT JOIN effects e ON a.affinity_passive_id = e.id
            WHERE wwa.main_weapon_id = %s
        """, (weapon_id,))
    affinities = cursor.fetchall()

    # If no affinities are found, add a default "Standard" row
    if not affinities:
        affinities = [{
            "affinity_name": None,
            "affinity_passive": None,
            "str_scaling": requirements["req_str"],
            "dex_scaling": requirements["req_dex"],
            "int_scaling": requirements["req_int"],
            "fai_scaling": requirements["req_fai"],
            "arc_scaling": requirements["req_arc"],
        }]

    return render_template(
        "weapon_detail.html",
        weapon=weapon,
        requirements=requirements,
        affinities=affinities
    )


def armors_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Get filter parameters
    set_id = request.args.get('set_id')
    slot_id = request.args.get('slot_id')
    weight_order = request.args.get('weight_order')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of armors per page
    
    # Base query
    query = """
        SELECT a.*, i.name as name, s.name as set_name, e.equip_slot
        FROM armors a 
        LEFT JOIN items i ON a.id = i.id
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

def armor_detail_page(armor_id, name=None, equip_slot=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = """SELECT a.*, i.name as name, e.equip_slot as equip_slot
                FROM armors a
                LEFT JOIN items i ON a.id = i.id
                LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id
                WHERE a.id = %s
    """
    cursor.execute(query, (armor_id,))
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

def profile_page():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    return render_template('profile.html', user=user)

def update_profile():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        steam_url = request.form.get('steam_url')
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            # Start transaction
            cursor.execute("START TRANSACTION")
            
            # Check if username is already taken by another user
            cursor.execute("""
                SELECT id FROM users 
                WHERE username = %s AND id != %s
            """, (username, session['user_id']))
            
            if cursor.fetchone():
                cursor.execute("ROLLBACK")
                flash('Username is already taken.', 'error')
                return redirect(url_for('profile_page'))
            
            # Update user profile
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, name = %s, steam_url = %s
                WHERE id = %s
            """, (username, email, name, steam_url, session['user_id']))
            
            # Commit transaction
            db.commit()
            
            # Update session username if it was changed
            session['username'] = username
            flash('Profile updated successfully!', 'success')
            
        except Exception as e:
            # Rollback in case of error
            cursor.execute("ROLLBACK")
            flash('Error updating profile.', 'error')
            print(f"Error: {str(e)}")
            
    return redirect(url_for('profile_page'))

def request_admin():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))
        
    if request.method == 'POST':
        admin_key = request.form.get('admin_key')
        ADMIN_KEY = os.getenv('ADMIN_KEY', 'CokGizli')
        
        if admin_key == ADMIN_KEY:
            db = get_db()
            cursor = db.cursor()
            
            try:
                # Start transaction
                cursor.execute("START TRANSACTION")
                
                # Update user to admin
                cursor.execute("""
                    UPDATE users 
                    SET admin = 1
                    WHERE id = %s
                """, (session['user_id'],))
                
                # Commit transaction
                db.commit()
                
                # Update session
                session['is_admin'] = True
                flash('Administrator access granted!', 'success')
                
            except Exception as e:
                # Rollback in case of error
                cursor.execute("ROLLBACK")
                flash('Error granting administrator access.', 'error')
                print(f"Error: {str(e)}")
        else:
            flash('Invalid administration key.', 'error')
            
    return redirect(url_for('profile_page'))

def editor_page():
    if not session.get('is_admin'):
        abort(403)  # Forbidden
    return render_template('editor.html')


