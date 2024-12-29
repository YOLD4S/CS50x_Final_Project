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
    
    # Initialize Flask-Session
    Session(app)
    
    app.teardown_appcontext(close_db)

    # Context processor to make user available in all templates
    @app.context_processor
    def inject_user():
        if session.get('user_id'):
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()
            return {'user': user}
        return {'user': None}

    # Routes
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
    app.add_url_rule("/items", view_func=views.items_page)
    app.add_url_rule("/items/<int:item_key>", view_func=views.item_page)
    app.add_url_rule("/npcs", view_func=views.npcs_page, methods=["GET", "POST"])
    app.add_url_rule("/add_new_npc", view_func=views.add_new_npc, methods=["GET", "POST"])
    app.add_url_rule("/npcs/<int:npc_key>", view_func=views.npc_page)
    app.add_url_rule("/weapons", view_func=views.weapons_page)
    app.add_url_rule("/weapon_groups", view_func=views.weapon_groups_page)
    app.add_url_rule("/weapon_groups/<int:group_id>", view_func=views.individual_group_page)
    app.add_url_rule("/weapons/all", view_func=views.all_weapons_page)
    app.add_url_rule("/weapons/<int:weapon_id>", view_func=views.weapon_detail_page)
    app.add_url_rule("/armors", view_func=views.armors_page)
    app.add_url_rule("/npc/<int:npc_id>", view_func=views.npc_detail_page)
    app.add_url_rule("/npc/<int:npc_id>/delete", view_func=views.delete_npc, methods=['POST'])
    app.add_url_rule("/npc/<int:npc_id>/update", view_func=views.update_npc, methods=['GET', 'POST'])
    app.add_url_rule("/items/<int:item_id>", view_func=views.item_detail_page)
    app.add_url_rule("/armors/<int:armor_id>", view_func=views.armor_detail_page)
    app.add_url_rule("/talismans", view_func=views.talismans_page)
    app.add_url_rule("/talismans/<int:talisman_id>", view_func=views.talisman_detail)
    app.add_url_rule("/magic", view_func=views.magic_page)
    app.add_url_rule("/magic/<int:magic_id>", view_func=views.magic_detail)
    app.add_url_rule("/spirit_ashes", view_func=views.spirit_ashes_page)
    app.add_url_rule("/spirit_ashes/<int:spirit_ash_id>", view_func=views.spirit_ashes_detail)
    app.add_url_rule("/key_items", view_func=views.key_items_page)
    app.add_url_rule("/key_items/<int:key_item_id>", view_func=views.key_item_detail)
    app.add_url_rule("/bolsters", view_func=views.bolsters_page)
    app.add_url_rule("/bolsters/<int:bolster_id>", view_func=views.bolster_detail)
    app.add_url_rule("/profile", view_func=views.profile_page)
    app.add_url_rule("/profile/update", view_func=views.update_profile, methods=["POST"])
    app.add_url_rule("/profile/request-admin", view_func=views.request_admin, methods=["POST"])
    app.add_url_rule("/editor", view_func=views.editor_page)
    app.add_url_rule("/editor/<section>", view_func=views.editor_page)
    app.add_url_rule("/profile/delete", view_func=views.delete_account, methods=["POST"])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config["PORT"])