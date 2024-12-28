#!/usr/bin/env python3
import os
import csv
import mysql.connector
from mysql.connector import Error

TABLE_LOAD_ORDER = [
    # Level 1: No references
    "users",
    "item_types",
    "key_item_types",
    "magic_types",
    "armor_equip_slots",
    "armor_sets",
    "weapon_groups",
    "weapon_skills",
    "regions",
    
    # Level 2: References a previously loaded table
    "locations",        # references regions
    "npc_encounters",   # references locations
    "items",            # references item_types
    "npcs",             # references npc_encounters, gear, items
    "effects",          # is referenced by affinities/weapons
    "affinities",       # references effects
    "weapons",          # references weapon_groups, effects, weapon_skills
    "weapons_w_affinities",  # references items, weapons, affinities
    "ashes_of_war",          # references items, affinities, weapon_skills
    "armors",           # references items, armor_sets, armor_equip_slots
    "gear",             # references weapons_w_affinities, weapon_skills, armors
    "characters",       # references users, gear
    "talismans",        # references items
    "magic",            # references items, magic_types
    "spirit_ashes",     # references items
    "bolsters",         # references items
    "key_items",        # references items, key_item_types
]

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "alihan2004",
    "database": "blg317e_eldenring",
}

def load_csv_into_table(cursor, table_name, csv_file_path):
    """
    Reads the CSV file at csv_file_path and inserts each row into table_name.
    Assumes the header row matches the columns you want to insert (including auto-increment 'id' if it exists).
    """
    if not os.path.isfile(csv_file_path):
        print(f" [INFO] CSV file not found for table '{table_name}': {csv_file_path}. Skipping.")
        return  # If no CSV is found, skip insertion

    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames  # column names from the CSV

        # Build an INSERT statement like: INSERT INTO table (col1, col2, ...) VALUES (%s, %s, ...)
        columns = ", ".join(f"`{h}`" for h in headers)
        placeholders = ", ".join(["%s"] * len(headers))
        insert_sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

        row_count = 0
        for row in reader:
            # Convert dict values into a tuple, respecting the column order
            # If any value is an empty string, treat it as None
            values_tuple = tuple(row[h] if row[h] != "" else None for h in headers)
            try:
                cursor.execute(insert_sql, values_tuple)
                row_count += 1
            except Error as e:
                print(f" [ERROR] Failed to insert row into '{table_name}': {e}")
                raise  # Re-raise the exception to trigger rollback

    print(f" [OK] Inserted {row_count} rows into '{table_name}' from '{csv_file_path}'.")

def main():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("[INFO] Successfully connected to the database.")

        cursor = connection.cursor()

        # Start a transaction; we’ll rollback if anything fails.
        connection.start_transaction()

        # Optional: Disable foreign key checks temporarily (not recommended if load order is correct)
        # cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        # print("[WARNING] Foreign key checks temporarily disabled.")

        try:
            for table_name in TABLE_LOAD_ORDER:
                csv_file_name = f"{table_name}.csv"
                csv_file_path = os.path.join(os.getcwd(), csv_file_name)
                print(f"\n[INFO] Loading data for table '{table_name}' from '{csv_file_path}'...")
                load_csv_into_table(cursor, table_name, csv_file_path)

            # If everything worked so far, commit the transaction
            connection.commit()
            print("\n[SUCCESS] All CSV data has been inserted successfully. Transaction committed.")

        except Error as e:
            print(f" [ERROR] A database error occurred: {e}")
            print(" [ACTION] Rolling back the transaction.")
            connection.rollback()

        finally:
            # Optional: Re-enable foreign key checks if you disabled them
            # cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print("[INFO] MySQL connection is closed.")

    except Error as err:
        print(f"[CRITICAL] Could not connect to MySQL: {err}")

if __name__ == "__main__":
    main()
