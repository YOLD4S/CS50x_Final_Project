from functools import wraps
from datetime import datetime
import os
from mysql.connector import Error

from flask import (
    Flask,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    abort,
    current_app,
    jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
from db import get_db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

            try:
                # Start a transaction
                cursor.execute("START TRANSACTION")

                # Insert the user into the database
                query = """
                    INSERT INTO users (username, password)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (username, generate_password_hash(password)))

                # Commit the transaction if all goes well
                db.commit()
                flash("You have been registered successfully!", "success")
                return redirect(url_for("login_page"))

            except Error as e:
                # Rollback the transaction if something goes wrong
                db.rollback()

                if e.errno == 1062 and "users.username" in str(e):  # Duplicate entry error code
                    flash("There is already an existing user with that username.", "error")
                else:
                    flash(f"An error occurred: {str(e)}", "error")

            finally:
                # Always close the cursor
                cursor.close()

    return render_template("register.html")


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
            rw.default_skill_id AS weapon_skill_id,
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
        location_id = request.form.get('location_id') or None
        right_weapon_id = request.form.get('right_weapon_id') or None
        left_weapon_id = request.form.get('left_weapon_id') or None
        armor_head_id = request.form.get('armor_head_id') or None
        armor_body_id = request.form.get('armor_body_id') or None
        armor_arms_id = request.form.get('armor_arms_id') or None
        armor_legs_id = request.form.get('armor_legs_id') or None

        # Fetch default skills for the selected weapons
        right_weapon_skill_id = next(
            (weapon['weapon_skill_id'] for weapon in weapons if weapon['weapon_affinity_id'] == int(right_weapon_id)),
            None
        ) if right_weapon_id else None

        left_weapon_skill_id = next(
            (weapon['weapon_skill_id'] for weapon in weapons if weapon['weapon_affinity_id'] == int(left_weapon_id)),
            None
        ) if left_weapon_id else None

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
            INSERT INTO gear (right_weapon_id, left_weapon_id, right_weapon_skill_id, left_weapon_skill_id,
                              armor_head_id, armor_body_id, armor_arms_id, armor_legs_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (right_weapon_id, left_weapon_id, right_weapon_skill_id, left_weapon_skill_id,
              armor_head_id, armor_body_id, armor_arms_id, armor_legs_id))
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
    search = request.args.get('search')
    
    # Base query
    query = """
        SELECT 
            npcs.id,
            npcs.name,
            n.name AS encounter_name,
            l.name AS location_name,
            n.only_night
        FROM 
            npcs
        LEFT JOIN 
            npc_encounters n ON npcs.encounter_id = n.id
        LEFT JOIN 
            locations l ON n.location_id = l.id
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
    if search:
        query += " AND npcs.name LIKE %s"
        params.append(f"%{search}%")
    
    query += " ORDER BY npcs.name ASC"
    
    # Execute main query
    cursor.execute(query, params)
    npcs = cursor.fetchall()
    
    # Get locations for filter dropdown
    cursor.execute("SELECT id, name FROM locations ORDER BY name ASC")
    locations = cursor.fetchall()
    
    return render_template(
        "npcs.html", 
        npcs=npcs,
        locations=locations,
        selected_location=location_id,
        only_night=only_night,
        search=search
    )


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
            rw.default_skill_id AS weapon_skill_id,
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
            gear.right_weapon_skill_id,
            gear.left_weapon_id,
            gear.left_weapon_skill_id,
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
        location_id = request.form.get('location_id') or None  # Handle NULL
        only_night = request.form.get('only_night') == 'on'

        # Gear details
        right_weapon_id = request.form.get('right_weapon_id') or None
        left_weapon_id = request.form.get('left_weapon_id') or None
        armor_head_id = request.form.get('armor_head_id') or None
        armor_body_id = request.form.get('armor_body_id') or None
        armor_arms_id = request.form.get('armor_arms_id') or None
        armor_legs_id = request.form.get('armor_legs_id') or None

        # Fetch default skills for the selected weapons
        right_weapon_skill_id = next(
            (weapon['weapon_skill_id'] for weapon in weapons if weapon['weapon_affinity_id'] == int(right_weapon_id)),
            None
        ) if right_weapon_id else None

        left_weapon_skill_id = next(
            (weapon['weapon_skill_id'] for weapon in weapons if weapon['weapon_affinity_id'] == int(left_weapon_id)),
            None
        ) if left_weapon_id else None

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
                        right_weapon_skill_id = %s, left_weapon_skill_id = %s,
                        armor_head_id = %s, armor_body_id = %s, 
                        armor_arms_id = %s, armor_legs_id = %s
                    WHERE id = %s
                """, (right_weapon_id, left_weapon_id, right_weapon_skill_id, left_weapon_skill_id,
                      armor_head_id, armor_body_id, armor_arms_id, armor_legs_id, gear_id))
            else:
                # Create new gear and update the NPC's gear_id
                cursor.execute("""
                    INSERT INTO gear (right_weapon_id, left_weapon_id, right_weapon_skill_id, left_weapon_skill_id, 
                                      armor_head_id, armor_body_id, armor_arms_id, armor_legs_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (right_weapon_id, left_weapon_id, right_weapon_skill_id, left_weapon_skill_id,
                      armor_head_id, armor_body_id, armor_arms_id, armor_legs_id))
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

def manage_npc():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch NPCs for dropdown
    cursor.execute("SELECT id, name FROM npcs ORDER BY name ASC")
    npcs = cursor.fetchall()

    if request.method == 'POST':
        npc_id = request.form.get('npc_id')
        action = request.form.get('action')

        if not npc_id or not action:
            flash("Please select an NPC and an action.", "warning")
            return redirect(url_for('manage_npc'))

        if action == "update":
            return redirect(url_for('update_npc', npc_id=npc_id))
        elif action == "delete":
            # Delete the NPC
            cursor.execute("DELETE FROM npcs WHERE id = %s", (npc_id,))
            db.commit()
            flash("NPC deleted successfully!", "success")
            return redirect(url_for('manage_npc'))

    return render_template("editor/npcs.html", npcs=npcs)




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

    # Fetch armor details along with related set and equip slot information
    cursor.execute("""
            SELECT a.id, a.weight, a.description, a.price, a.can_alter, 
                   i.name AS name, 
                   s.name AS set_name, s.id AS set_id, 
                   e.equip_slot AS equip_slot, e.id AS equip_slot_id, 
                   a.image_url
            FROM armors a
            LEFT JOIN items i ON a.id = i.id
            LEFT JOIN armor_sets s ON a.set_id = s.id
            LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id
            WHERE a.id = %s
        """, (armor_id,))
    armor = cursor.fetchone()

    if not armor:
        abort(404)

    return render_template("armor_detail.html", armor=armor)

def create_armor_set():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Set name is required'}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Insert new armor set
        cursor.execute("""
            INSERT INTO armor_sets (name)
            VALUES (%s)
        """, (name,))
        
        set_id = cursor.lastrowid
        
        db.commit()
        return jsonify({
            'id': set_id,
            'name': name,
            'message': 'Armor set created successfully'
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

def talismans_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get current page, sorting options, and order
    page = request.args.get("page", 1, type=int)
    sort_by = request.args.get("sort_by", "name")
    sort_order = request.args.get("order", "asc")  # Default order is ascending
    per_page = 12
    offset = (page - 1) * per_page

    # Determine sorting column
    sort_column = "i.name"  # Default sorting by name
    if sort_by == "weight":
        sort_column = "t.weight"
    elif sort_by == "price":
        sort_column = "t.price"

    # Ensure valid sort order
    sort_order = "ASC" if sort_order.lower() == "asc" else "DESC"

    # Query to fetch total number of talismans for pagination
    cursor.execute("SELECT COUNT(*) AS total FROM talismans")
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Query to fetch talismans for the current page
    cursor.execute(f"""
            SELECT t.id, i.name, t.image_url, t.weight, t.price
            FROM talismans t
            LEFT JOIN items i ON t.id = i.id
            ORDER BY {sort_column} {sort_order}
            LIMIT %s OFFSET %s
        """, (per_page, offset))
    talismans = cursor.fetchall()

    return render_template(
        "talismans.html",
        talismans=talismans,
        current_page=page,
        total_pages=total_pages,
        sort_by=sort_by,
        order=sort_order.lower()
    )

def talisman_detail(talisman_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch talisman details
    cursor.execute("""
            SELECT t.id, i.name, t.info, t.description, t.weight, t.price, t.image_url
            FROM talismans t
            LEFT JOIN items i ON t.id = i.id
            WHERE t.id = %s
        """, (talisman_id,))
    talisman = cursor.fetchone()

    if not talisman:
        abort(404)

    return render_template("talisman_detail.html", talisman=talisman)


def magic_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get current page, filter, and pagination parameters
    page = request.args.get("page", 1, type=int)
    type_id = request.args.get("type_id", None, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # Base query
    query = """
            SELECT m.id, i.name, m.image_url, t.magic_type 
            FROM magic m
            LEFT JOIN items i ON m.id = i.id
            LEFT JOIN magic_types t ON m.type_id = t.id
            WHERE 1=1
        """
    count_query = "SELECT COUNT(*) as total FROM magic WHERE 1=1"
    params = []

    # Apply filtering by type_id
    if type_id:
        query += " AND m.type_id = %s"
        count_query += " AND type_id = %s"
        params.append(type_id)

    # Add sorting and pagination
    query += " ORDER BY i.name ASC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    # Fetch total count for pagination
    cursor.execute(count_query, params[:len(params) - 2])
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Fetch magic for the current page
    cursor.execute(query, params)
    magics = cursor.fetchall()

    # Fetch magic types for filtering dropdown
    cursor.execute("SELECT id, magic_type FROM magic_types ORDER BY magic_type ASC")
    magic_types = cursor.fetchall()

    return render_template(
        "magic.html",
        magics=magics,
        magic_types=magic_types,
        selected_type_id=type_id,
        current_page=page,
        total_pages=total_pages
    )

def magic_detail(magic_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch magic details along with type information
    cursor.execute("""
        SELECT m.id, i.name, m.info, m.description, m.fp_cost, m.fp_cost_continuous, 
               m.stamina_cost, m.slots_used, m.req_int, m.req_fai, m.req_arc, m.image_url,
               t.magic_type, t.id AS magic_type_id
        FROM magic m
        LEFT JOIN items i ON m.id = i.id
        LEFT JOIN magic_types t ON m.type_id = t.id
        WHERE m.id = %s
    """, (magic_id,))
    magic = cursor.fetchone()

    if not magic:
        abort(404)

    return render_template("magic_detail.html", magic=magic)

def spirit_ashes_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get current page and calculate offset
    page = request.args.get("page", 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # Query to fetch total number of spirit ashes for pagination
    cursor.execute("SELECT COUNT(*) AS total FROM spirit_ashes")
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Query to fetch spirit ashes for the current page
    cursor.execute("""
            SELECT sa.id, i.name, sa.image_url 
            FROM spirit_ashes sa
            LEFT JOIN items i ON sa.id = i.id
            ORDER BY i.name ASC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
    spirit_ashes = cursor.fetchall()

    return render_template(
        "spirit_ashes.html",
        spirit_ashes=spirit_ashes,
        current_page=page,
        total_pages=total_pages
    )

def spirit_ashes_detail(spirit_ash_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch spirit ash details
    cursor.execute("""
            SELECT sa.id, i.name, sa.info, sa.description, sa.fp_cost, sa.hp_cost, sa.hp, sa.image_url
            FROM spirit_ashes sa
            LEFT JOIN items i ON sa.id = i.id
            WHERE sa.id = %s
        """, (spirit_ash_id,))
    spirit_ash = cursor.fetchone()

    if not spirit_ash:
        abort(404)

    return render_template("spirit_ashes_detail.html", spirit_ash=spirit_ash)

def key_items_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get current page, filter, and pagination parameters
    page = request.args.get("page", 1, type=int)
    type_id = request.args.get("type_id", None, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # Base query
    query = """
            SELECT ki.id, i.name, ki.image_url, t.key_item_type
            FROM key_items ki
            LEFT JOIN items i ON ki.id = i.id
            LEFT JOIN key_item_types t ON ki.type_id = t.id
            WHERE 1=1
        """
    count_query = "SELECT COUNT(*) as total FROM key_items WHERE 1=1"
    params = []

    # Apply filtering by type_id
    if type_id:
        query += " AND ki.type_id = %s"
        count_query += " AND type_id = %s"
        params.append(type_id)

    # Add pagination
    query += " ORDER BY i.name ASC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    # Fetch total count for pagination
    cursor.execute(count_query, params[:len(params) - 2])
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Fetch key items for the current page
    cursor.execute(query, params)
    key_items = cursor.fetchall()

    # Fetch key item types for filtering dropdown
    cursor.execute("SELECT id, key_item_type FROM key_item_types ORDER BY key_item_type ASC")
    key_item_types = cursor.fetchall()

    return render_template(
        "key_items.html",
        key_items=key_items,
        key_item_types=key_item_types,
        selected_type_id=type_id,
        current_page=page,
        total_pages=total_pages
    )

def key_item_detail(key_item_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch key item details
    cursor.execute("""
        SELECT ki.id, i.name, ki.info, ki.description, ki.image_url,
               t.key_item_type, t.id AS key_item_type_id
        FROM key_items ki
        LEFT JOIN items i ON ki.id = i.id
        LEFT JOIN key_item_types t ON ki.type_id = t.id
        WHERE ki.id = %s
    """, (key_item_id,))
    key_item = cursor.fetchone()

    if not key_item:
        abort(404)

    return render_template("key_item_detail.html", key_item=key_item)


def bolsters_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get current page, sorting options, and pagination parameters
    page = request.args.get("page", 1, type=int)
    sort_by = request.args.get("sort_by", "name")  # Default sorting by name
    order = request.args.get("order", "asc")  # Default order is ascending
    per_page = 12
    offset = (page - 1) * per_page

    # Determine sorting column
    sort_column = "i.name"
    if sort_by == "price":
        sort_column = "b.price"

    # Ensure valid sort order
    sort_order = "ASC" if order.lower() == "asc" else "DESC"

    # Query to fetch total number of bolsters for pagination
    cursor.execute("SELECT COUNT(*) AS total FROM bolsters")
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Query to fetch bolsters for the current page
    cursor.execute(f"""
        SELECT b.id, i.name, b.image_url, b.price 
        FROM bolsters b
        LEFT JOIN items i ON b.id = i.id
        ORDER BY {sort_column} {sort_order}
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    bolsters = cursor.fetchall()

    return render_template(
        "bolsters.html",
        bolsters=bolsters,
        current_page=page,
        total_pages=total_pages,
        sort_by=sort_by,
        order=order
    )


def bolster_detail(bolster_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch bolster details
    cursor.execute("""
        SELECT b.id, i.name, b.info, b.description, b.max_held, b.max_storage, b.price, b.image_url
        FROM bolsters b
        LEFT JOIN items i ON b.id = i.id
        WHERE b.id = %s
    """, (bolster_id,))
    bolster = cursor.fetchone()

    if not bolster:
        abort(404)

    return render_template("bolster_detail.html", bolster=bolster)


def profile_page():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))
        
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    return render_template('profile.html', user=user)

def upload_profile_picture():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))

    if 'profile_picture' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('profile_page'))

    file = request.files['profile_picture']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('profile_page'))

    if file and allowed_file(file.filename):
        # Define the upload folder for profile pictures
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/profile_pictures')
        os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists

        # Save the file as user_<id>.png
        filename = f"user_{session['user_id']}.png"
        filepath = os.path.join(upload_folder, filename)

        try:
            # Open the image and crop it to a square
            image = Image.open(file)
            min_dim = min(image.size)  # Find the smallest dimension
            left = (image.width - min_dim) / 2
            top = (image.height - min_dim) / 2
            right = (image.width + min_dim) / 2
            bottom = (image.height + min_dim) / 2

            cropped_image = image.crop((left, top, right, bottom))
            cropped_image = cropped_image.resize((150, 150))  # Resize to 150x150 pixels
            cropped_image.save(filepath)

            # Update the database
            db = get_db()
            cursor = db.cursor()
            cursor.execute("START TRANSACTION")
            cursor.execute("""
                    UPDATE users
                    SET profile_picture = %s
                    WHERE id = %s
                """, (f"profile_pictures/{filename}", session['user_id']))
            db.commit()

            flash('Profile picture updated successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash('Error saving profile picture. Please try again.', 'error')
            print(f"Error: {str(e)}")
    else:
        flash('Invalid file type. Please upload a PNG, JPG, or GIF.', 'error')

    return redirect(url_for('profile_page'))

def remove_profile_picture():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)  # Ensure the cursor returns dictionaries
        cursor.execute("START TRANSACTION")

        # Fetch the current profile picture path
        cursor.execute("SELECT profile_picture FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user and user['profile_picture']:  # Access using dictionary keys
            # Delete the profile picture file
            picture_path = os.path.join(current_app.root_path, 'static/uploads', user['profile_picture'])
            if os.path.exists(picture_path):
                os.remove(picture_path)

        # Update the database to remove the profile picture
        cursor.execute("""
                UPDATE users
                SET profile_picture = NULL
                WHERE id = %s
            """, (session['user_id'],))
        db.commit()

        flash('Profile picture removed successfully!', 'success')
    except Exception as e:
        db.rollback()
        flash('Error removing profile picture. Please try again.', 'error')
        print(f"Error: {str(e)}")

    return redirect(url_for('profile_page'))

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
            update_query = "UPDATE users SET username = %s"
            parameters = [username]

            if email != "":
                update_query += ", email = %s"
                parameters.append(email)
            if name != "":
                update_query += ", name = %s"
                parameters.append(name)
            if steam_url != "":
                update_query += ", steam_url = %s"
                parameters.append(steam_url)

            # Add the WHERE clause
            update_query += " WHERE id = %s"
            parameters.append(session['user_id'])

            # Execute the query
            cursor.execute(update_query, tuple(parameters))
            
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

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login_page'))
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT admin FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        if not user or not user['admin']:
            flash('You need administrator privileges to access this page.', 'error')
            return redirect(url_for('home_page'))
            
        return f(*args, **kwargs)
    return decorated_function

@admin_required
def armor_editor():
    return render_template('editor/armors.html')

@admin_required
def add_armor():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch armor sets and equipment slots for dropdowns
    cursor.execute("SELECT id, name FROM armor_sets ORDER BY name")
    armor_sets = cursor.fetchall()
    
    cursor.execute("SELECT id, equip_slot FROM armor_equip_slots ORDER BY id")
    equip_slots = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            # Start transaction
            cursor.execute("START TRANSACTION")
            
            # Handle new set creation if selected
            set_id = request.form['set_id']
            if set_id == 'new':
                new_set_name = request.form['new_set_name']
                cursor.execute("""
                    INSERT INTO armor_sets (name)
                    VALUES (%s)
                """, (new_set_name,))
                set_id = cursor.lastrowid
                flash(f'New armor set "{new_set_name}" created successfully!', 'success')
            
            # Get the armor name for the message
            armor_name = request.form['name']
            
            # Insert into items table first
            cursor.execute("""
                INSERT INTO items (type_id, name)
                VALUES (2, %s)  -- type_id 2 for armors
            """, (armor_name,))
            
            armor_id = cursor.lastrowid
            
            # Then insert into armors table
            cursor.execute("""
                INSERT INTO armors (id, set_id, equip_slot_id, description, weight, price, can_alter, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                armor_id,
                set_id,
                request.form['equip_slot'],
                request.form['description'],
                float(request.form['weight']),
                request.form['price'] if request.form['price'] else None,
                'can_alter' in request.form,
                request.form['image_url']
            ))
            
            db.commit()
            flash(f'Armor "{armor_name}" has been added successfully!', 'success')
            return redirect(url_for('armor_editor'))
            
        except Exception as e:
            db.rollback()
            flash(f'Error adding armor: {str(e)}', 'error')
    
    return render_template('editor/armors_add.html', armor_sets=armor_sets, equip_slots=equip_slots)

@admin_required
def modify_armor(armor_id=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if armor_id:
        # Show edit form for specific armor
        cursor.execute("SELECT id, name FROM armor_sets ORDER BY name")
        armor_sets = cursor.fetchall()
        
        cursor.execute("SELECT id, equip_slot FROM armor_equip_slots ORDER BY id")
        equip_slots = cursor.fetchall()
        
        cursor.execute("""
            SELECT a.*, i.name, s.name as set_name, e.equip_slot
            FROM armors a 
            LEFT JOIN items i ON a.id = i.id
            LEFT JOIN armor_sets s ON a.set_id = s.id 
            LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id 
            WHERE a.id = %s
        """, (armor_id,))
        armor = cursor.fetchone()
        
        if not armor:
            abort(404)
        
        if request.method == 'POST':
            try:
                # Start transaction
                cursor.execute("START TRANSACTION")
                
                # Get the old and new names for the message
                old_name = armor['name']
                new_name = request.form['name']
                
                # Update items table
                cursor.execute("""
                    UPDATE items 
                    SET name = %s
                    WHERE id = %s
                """, (new_name, armor_id))
                
                # Update armors table
                cursor.execute("""
                    UPDATE armors 
                    SET set_id = %s, 
                        equip_slot_id = %s, 
                        description = %s,
                        weight = %s, 
                        price = %s, 
                        can_alter = %s,
                        image_url = %s
                    WHERE id = %s
                """, (
                    request.form['set_id'],
                    request.form['equip_slot'],
                    request.form['description'],
                    float(request.form['weight']),
                    request.form['price'] if request.form['price'] else None,
                    'can_alter' in request.form,
                    request.form['image_url'],
                    armor_id
                ))
                
                db.commit()
                if old_name != new_name:
                    flash(f'Armor "{old_name}" has been renamed to "{new_name}" and updated successfully!', 'success')
                else:
                    flash(f'Armor "{old_name}" has been updated successfully!', 'success')
                return redirect(url_for('modify_armor'))
                
            except Exception as e:
                db.rollback()
                flash(f'Error updating armor: {str(e)}', 'error')
        
        return render_template('editor/armors_modify_form.html', armor=armor, armor_sets=armor_sets, equip_slots=equip_slots)
    
    # Show list of armors to modify
    cursor.execute("""
        SELECT a.*, i.name, s.name as set_name, e.equip_slot
        FROM armors a 
        LEFT JOIN items i ON a.id = i.id
        LEFT JOIN armor_sets s ON a.set_id = s.id 
        LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id 
        ORDER BY i.name
    """)
    armors = cursor.fetchall()
    return render_template('editor/armors_modify.html', armors=armors)

@admin_required
def armor_delete_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Fetch armor sets with their armor counts
    cursor.execute("""
        SELECT s.id, s.name, COUNT(a.id) as armor_count
        FROM armor_sets s
        LEFT JOIN armors a ON s.id = a.set_id
        GROUP BY s.id, s.name
        ORDER BY s.name
    """)
    armor_sets = cursor.fetchall()
    
    # Fetch armors
    cursor.execute("""
        SELECT a.*, i.name, s.name as set_name, e.equip_slot
        FROM armors a 
        LEFT JOIN items i ON a.id = i.id
        LEFT JOIN armor_sets s ON a.set_id = s.id 
        LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id 
        ORDER BY i.name
    """)
    armors = cursor.fetchall()
    
    return render_template('editor/armors_delete.html', armors=armors, armor_sets=armor_sets)

@admin_required
def delete_armor_set(set_id):
    if request.method == 'POST':
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Get the set name for the message
            cursor.execute("SELECT name FROM armor_sets WHERE id = %s", (set_id,))
            result = cursor.fetchone()
            if not result:
                flash('Armor set not found.', 'error')
                return redirect(url_for('armor_delete_page'))
                
            set_name = result[0]
            
            # Start transaction
            cursor.execute("START TRANSACTION")
            
            
            # Delete the armor set
            cursor.execute("DELETE FROM armor_sets WHERE id = %s", (set_id,))
            
            db.commit()
            flash(f'Armor set "{set_name}" has been deleted successfully!', 'success')
            return redirect(url_for('armor_delete_page'))
            
        except Exception as e:
            db.rollback()
            flash(f'Error deleting armor set: {str(e)}', 'error')
            return redirect(url_for('armor_delete_page'))
    
    # If GET request, redirect to delete page
    return redirect(url_for('armor_delete_page'))

@admin_required
def delete_armor(armor_id):
    if request.method == 'POST':
        try:
            db = get_db()
            cursor = db.cursor()
            
            # Get the armor name for the message
            cursor.execute("SELECT name FROM items WHERE id = %s", (armor_id,))
            result = cursor.fetchone()
            if not result:
                flash('Armor not found.', 'error')
                return redirect(url_for('armor_delete_page'))
                
            armor_name = result[0]
            
            # Start transaction
            cursor.execute("START TRANSACTION")
            
            # Delete from items table first (this will cascade to armors table)
            cursor.execute("DELETE FROM items WHERE id = %s", (armor_id,))
            
            db.commit()
            flash(f'Armor "{armor_name}" has been deleted successfully!', 'success')
            return redirect(url_for('armor_delete_page'))
            
        except Exception as e:
            db.rollback()
            flash(f'Error deleting armor: {str(e)}', 'error')
            return redirect(url_for('armor_delete_page'))
    
    # If GET request, redirect to delete page
    return redirect(url_for('armor_delete_page'))

def delete_account():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))

    db = get_db()
    cursor = db.cursor()

    try:
        # Start transaction
        cursor.execute("START TRANSACTION")

        # Delete user from database
        cursor.execute("DELETE FROM users WHERE id = %s", (session['user_id'],))

        # Commit transaction
        db.commit()

        # Clear session
        session.clear()

        flash('Your account has been deleted successfully!', 'success')
    except Exception as e:
        # Rollback in case of error
        cursor.execute("ROLLBACK")
        flash('Error deleting account.', 'error')
        print(f"Error: {str(e)}")

    return redirect(url_for('home_page'))

def update_armor(armor_id):
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401

    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        try:
            # Start transaction
            cursor.execute("START TRANSACTION")
            
            # Update items table
            cursor.execute("""
                UPDATE items 
                SET name = %s
                WHERE id = %s
            """, (data['name'], armor_id))
            
            # Update armors table
            cursor.execute("""
                UPDATE armors 
                SET set_id = %s, 
                    equip_slot_id = %s, 
                    weight = %s, 
                    price = %s, 
                    can_alter = %s,
                    description = %s,
                    image_url = %s
                WHERE id = %s
            """, (
                data['set_id'], 
                data['equip_slot'],
                data['weight'],
                data.get('price', None),
                data.get('can_alter', False),
                data.get('description', ''),
                data.get('image_url', ''),
                armor_id
            ))
            
            db.commit()
            return jsonify({'message': 'Armor updated successfully'}), 200
            
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
            
    # GET request - fetch armor details
    cursor.execute("""
        SELECT a.*, i.name, s.name as set_name, e.equip_slot
        FROM armors a 
        LEFT JOIN items i ON a.id = i.id
        LEFT JOIN armor_sets s ON a.set_id = s.id 
        LEFT JOIN armor_equip_slots e ON a.equip_slot_id = e.id 
        WHERE a.id = %s
    """, (armor_id,))
    
    armor = cursor.fetchone()
    if not armor:
        return jsonify({'error': 'Armor not found'}), 404
        
    return jsonify(armor)

@admin_required
def editor_page(section=None):
    if section == 'armor':
        return redirect(url_for('armor_editor'))
    return render_template('editor/editor.html', section=section)

@admin_required
def weapon_editor_page():
    return render_template('editor/weapons.html')

@admin_required
def add_weapon():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch data for dropdowns
    cursor.execute("SELECT id, name FROM weapon_groups ORDER BY name")
    weapon_groups = cursor.fetchall()

    cursor.execute("SELECT id, description FROM effects ORDER BY id")
    effects = cursor.fetchall()

    cursor.execute("SELECT id, name FROM weapon_skills ORDER BY name")
    skills = cursor.fetchall()

    cursor.execute("SELECT id, name FROM affinities ORDER BY id")
    affinities = cursor.fetchall()

    if request.method == 'POST':
        try:
            cursor.execute("START TRANSACTION")

            # Weapon data
            name = request.form.get('name')
            description = request.form.get('description')
            group_id = request.form.get('group_id')
            weapon_passive_id = request.form.get('weapon_passive_id') or None
            hidden_effect_id = request.form.get('hidden_effect_id') or None
            default_skill_id = request.form.get('default_skill_id') or None
            weight = float(request.form.get('weight'))
            req_str = int(request.form.get('req_str') or 0)
            req_dex = int(request.form.get('req_dex') or 0)
            req_int = int(request.form.get('req_int') or 0)
            req_fai = int(request.form.get('req_fai') or 0)
            req_arc = int(request.form.get('req_arc') or 0)

            cursor.execute("""
                INSERT INTO weapons (group_id, name, description, weapon_passive_id, hidden_effect_id,
                                     default_skill_id, weight, req_str, req_dex, req_int, req_fai, req_arc, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
            """, (group_id, name, description, weapon_passive_id, hidden_effect_id, default_skill_id, weight,
                  req_str, req_dex, req_int, req_fai, req_arc))
            weapon_id = cursor.lastrowid

            # Handle image upload
            file = request.files.get('image_file')
            print(file)
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Define upload folder and ensure it exists
                    upload_folder = os.path.join(current_app.root_path, 'static/uploads/weapons')
                    os.makedirs(upload_folder, exist_ok=True)

                    # Use weapon ID as the filename
                    filename = f"{weapon_id}.png"
                    filepath = os.path.join(upload_folder, filename)

                    # Open the image, crop and resize it to 200x200 pixels
                    image = Image.open(file)
                    min_dim = min(image.size)  # Find the smallest dimension
                    left = (image.width - min_dim) / 2
                    top = (image.height - min_dim) / 2
                    right = (image.width + min_dim) / 2
                    bottom = (image.height + min_dim) / 2

                    cropped_image = image.crop((left, top, right, bottom))
                    resized_image = cropped_image.resize((200, 200))
                    resized_image.save(filepath)

                    # Update the weapon record with the image path
                    image_url = f"uploads/weapons/{filename}"
                    cursor.execute("""
                        UPDATE weapons
                        SET image_url = %s
                        WHERE id = %s
                    """, (image_url, weapon_id))
                except Exception as e:
                    db.rollback()
                    flash(f"Error processing image: {str(e)}", "error")
            else:
                flash('Invalid or missing image file. Weapon added without image.', 'info')

            # Process affinities (same logic as before)
            for affinity in affinities:
                affinity_id = affinity['id']
                str_scaling = int(request.form.get(f'str_scaling_{affinity_id}') or 0)
                dex_scaling = int(request.form.get(f'dex_scaling_{affinity_id}') or 0)
                int_scaling = int(request.form.get(f'int_scaling_{affinity_id}') or 0)
                fai_scaling = int(request.form.get(f'fai_scaling_{affinity_id}') or 0)
                arc_scaling = int(request.form.get(f'arc_scaling_{affinity_id}') or 0)

                if any([str_scaling, dex_scaling, int_scaling, fai_scaling, arc_scaling]):
                    item_name = f"{affinity['name']} {name}"
                    cursor.execute("""
                            INSERT INTO items (type_id, name)
                            VALUES (1, %s)
                        """, (item_name,))
                    wwa_id = cursor.lastrowid

                    cursor.execute("""
                            INSERT INTO weapons_w_affinities (id, main_weapon_id, affinity_id, str_scaling, dex_scaling, 
                                                              int_scaling, fai_scaling, arc_scaling)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                    wwa_id, weapon_id, affinity_id, str_scaling, dex_scaling, int_scaling, fai_scaling, arc_scaling))

            # Default entry if no affinities
            if not any(
                    any([int(request.form.get(f'{scaling}_{affinity["id"]}') or 0) for scaling in
                         ["str_scaling", "dex_scaling", "int_scaling", "fai_scaling", "arc_scaling"]])
                    for affinity in affinities
            ):
                cursor.execute("""
                        INSERT INTO items (type_id, name)
                        VALUES (1, %s)
                    """, (name,))
                wwa_id = cursor.lastrowid
                cursor.execute("""
                        INSERT INTO weapons_w_affinities (id, main_weapon_id, affinity_id, str_scaling, dex_scaling, 
                                                          int_scaling, fai_scaling, arc_scaling)
                        VALUES (%s, %s, NULL, 0, 0, 0, 0, 0)
                    """, (wwa_id, weapon_id))

            db.commit()
            flash(f"Weapon '{name}' added successfully!", "success")
            return redirect(url_for('add_weapon'))  # Redirect stays on the same page

        except Exception as e:
            db.rollback()
            flash(f"Error adding weapon: {str(e)}", "error")

    return render_template('editor/weapons_add.html', weapon_groups=weapon_groups, effects=effects, skills=skills,
                           affinities=affinities)

@admin_required
def modify_weapon(weapon_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch data for dropdowns
    cursor.execute("SELECT id, name FROM weapon_groups ORDER BY name")
    weapon_groups = cursor.fetchall()

    cursor.execute("SELECT id, description FROM effects ORDER BY id")
    effects = cursor.fetchall()

    cursor.execute("SELECT id, name FROM weapon_skills ORDER BY name")
    skills = cursor.fetchall()

    cursor.execute("SELECT id, name FROM affinities ORDER BY id")
    affinities = cursor.fetchall()

    # Fetch current weapon details
    cursor.execute("""
        SELECT * FROM weapons WHERE id = %s
    """, (weapon_id,))
    weapon = cursor.fetchone()

    if not weapon:
        abort(404)

    # Fetch affinities for the weapon
    cursor.execute("""
        SELECT wwa.*, a.name AS affinity_name
        FROM weapons_w_affinities wwa
        LEFT JOIN affinities a ON wwa.affinity_id = a.id
        WHERE wwa.main_weapon_id = %s
    """, (weapon_id,))
    weapon_affinities = cursor.fetchall()

    if request.method == 'POST':
        try:
            cursor.execute("START TRANSACTION")

            # Update weapon fields
            name = request.form.get('name')
            description = request.form.get('description')
            group_id = request.form.get('group_id')
            weapon_passive_id = request.form.get('weapon_passive_id') or None
            hidden_effect_id = request.form.get('hidden_effect_id') or None
            default_skill_id = request.form.get('default_skill_id') or None
            weight = float(request.form.get('weight'))
            req_str = int(request.form.get('req_str') or 0)
            req_dex = int(request.form.get('req_dex') or 0)
            req_int = int(request.form.get('req_int') or 0)
            req_fai = int(request.form.get('req_fai') or 0)
            req_arc = int(request.form.get('req_arc') or 0)

            # Update weapon in the database
            cursor.execute("""
                UPDATE weapons
                SET group_id = %s, name = %s, description = %s, weapon_passive_id = %s,
                    hidden_effect_id = %s, default_skill_id = %s, weight = %s,
                    req_str = %s, req_dex = %s, req_int = %s, req_fai = %s, req_arc = %s
                WHERE id = %s
            """, (group_id, name, description, weapon_passive_id, hidden_effect_id, default_skill_id,
                  weight, req_str, req_dex, req_int, req_fai, req_arc, weapon_id))

            # Handle image upload
            file = request.files.get('image_file')
            if file and file.filename and allowed_file(file.filename):
                upload_folder = os.path.join(current_app.root_path, 'static/uploads/weapons')
                os.makedirs(upload_folder, exist_ok=True)

                filename = f"{weapon_id}.png"
                filepath = os.path.join(upload_folder, filename)

                image = Image.open(file)
                min_dim = min(image.size)
                left = (image.width - min_dim) / 2
                top = (image.height - min_dim) / 2
                right = (image.width + min_dim) / 2
                bottom = (image.height + min_dim) / 2

                cropped_image = image.crop((left, top, right, bottom))
                resized_image = cropped_image.resize((200, 200))
                resized_image.save(filepath)

                image_url = f"uploads/weapons/{filename}"
                cursor.execute("""
                    UPDATE weapons
                    SET image_url = %s
                    WHERE id = %s
                """, (image_url, weapon_id))

            # Update affinities
            for affinity in affinities:
                affinity_id = affinity['id']
                str_scaling = int(request.form.get(f'str_scaling_{affinity_id}') or 0)
                dex_scaling = int(request.form.get(f'dex_scaling_{affinity_id}') or 0)
                int_scaling = int(request.form.get(f'int_scaling_{affinity_id}') or 0)
                fai_scaling = int(request.form.get(f'fai_scaling_{affinity_id}') or 0)
                arc_scaling = int(request.form.get(f'arc_scaling_{affinity_id}') or 0)

                if any([str_scaling, dex_scaling, int_scaling, fai_scaling, arc_scaling]):
                    # Check if the affinity already exists for this weapon
                    cursor.execute("""
                        SELECT id FROM weapons_w_affinities
                        WHERE main_weapon_id = %s AND affinity_id = %s
                    """, (weapon_id, affinity_id))
                    existing_affinity = cursor.fetchone()

                    if existing_affinity:
                        # Update the existing scaling values
                        cursor.execute("""
                            UPDATE weapons_w_affinities
                            SET str_scaling = %s, dex_scaling = %s, int_scaling = %s,
                                fai_scaling = %s, arc_scaling = %s
                            WHERE id = %s
                        """, (str_scaling, dex_scaling, int_scaling, fai_scaling, arc_scaling, existing_affinity['id']))
                    else:
                        # Add a new item for this affinity
                        item_name = f"{affinity['name']} {name}"
                        cursor.execute("""
                            INSERT INTO items (type_id, name)
                            VALUES (1, %s)
                        """, (item_name,))
                        wwa_id = cursor.lastrowid

                        cursor.execute("""
                            INSERT INTO weapons_w_affinities (id, main_weapon_id, affinity_id, str_scaling, dex_scaling,
                                                              int_scaling, fai_scaling, arc_scaling)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (wwa_id, weapon_id, affinity_id, str_scaling, dex_scaling, int_scaling, fai_scaling,
                              arc_scaling))

            db.commit()
            flash(f"Weapon '{name}' updated successfully!", "success")
            return redirect(url_for('modify_weapon', weapon_id=weapon_id))

        except Exception as e:
            db.rollback()
            flash(f"Error updating weapon: {str(e)}", "error")

    return render_template(
        'editor/weapons_modify.html',
        weapon=weapon,
        weapon_groups=weapon_groups,
        effects=effects,
        skills=skills,
        affinities=affinities,
        weapon_affinities=weapon_affinities
    )

@admin_required
def modify_weapons():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get the current page and search query from the request
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    search_query = request.args.get("search", "").strip()

    # Build the query for total count and filtered weapons
    search_clause = "WHERE name LIKE %s" if search_query else ""
    search_param = f"%{search_query}%" if search_query else None

    # Fetch total weapon count
    cursor.execute(f"SELECT COUNT(*) AS total FROM weapons {search_clause}", (search_param,) if search_param else ())
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Fetch weapons for the current page
    cursor.execute(f"""
            SELECT id, name, image_url
            FROM weapons
            {search_clause}
            ORDER BY name ASC
            LIMIT %s OFFSET %s
        """, ((search_param,) if search_param else ()) + (per_page, offset))
    weapons = cursor.fetchall()

    return render_template(
        "editor/weapons_modify_navigate.html",
        weapons=weapons,
        current_page=page,
        total_pages=total_pages,
        search_query=search_query  # Pass the search query to the template
    )


@admin_required
def navigate_weapons_delete():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get current page, search query, and pagination settings
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    search_query = request.args.get("search", "").strip()

    # Build the query for total count and filtered weapons
    search_clause = f"WHERE name LIKE %s" if search_query else ""
    search_param = f"%{search_query}%" if search_query else None

    # Fetch total weapon count
    cursor.execute(f"SELECT COUNT(*) AS total FROM weapons {search_clause}", (search_param,) if search_param else ())
    total = cursor.fetchone()["total"]
    total_pages = (total + per_page - 1) // per_page

    # Fetch weapons for the current page
    cursor.execute(f"""
            SELECT id, name, image_url
            FROM weapons
            {search_clause}
            ORDER BY name ASC
            LIMIT %s OFFSET %s
        """, ((search_param,) if search_param else ()) + (per_page, offset))
    weapons = cursor.fetchall()

    return render_template(
        "editor/weapons_delete_navigate.html",
        weapons=weapons,
        current_page=page,
        total_pages=total_pages,
        search_query=search_query  # Pass the search query to the template
    )

@admin_required
def delete_weapon(weapon_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch query parameters from form data or default values
    page = request.form.get("page", 1, type=int)
    search_query = request.form.get("search", "").strip()

    # Fetch weapon details
    cursor.execute("SELECT name FROM weapons WHERE id = %s", (weapon_id,))
    weapon = cursor.fetchone()

    if not weapon:
        flash("Weapon not found.", "error")
        return redirect(url_for('navigate_weapons_delete', page=page, search=search_query))

    try:
        # Start transaction
        cursor.execute("START TRANSACTION")

        # Fetch item IDs from weapons_w_affinities before deletion
        cursor.execute("""
                SELECT id FROM weapons_w_affinities
                WHERE main_weapon_id = %s
            """, (weapon_id,))
        affinity_items = cursor.fetchall()

        # Delete associated rows from items
        for item in affinity_items:
            cursor.execute("""
                    DELETE FROM items
                    WHERE id = %s
                """, (item['id'],))

        # Delete the weapon (this also deletes rows in weapons_w_affinities due to foreign key constraints)
        cursor.execute("DELETE FROM weapons WHERE id = %s", (weapon_id,))

        # Commit transaction
        db.commit()
        flash(f"Weapon '{weapon['name']}' and associated items have been deleted successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting weapon: {str(e)}", "error")

    return redirect(url_for('navigate_weapons_delete', page=page, search=search_query))