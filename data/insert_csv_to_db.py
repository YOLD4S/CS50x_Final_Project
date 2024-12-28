import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Define the correct order of tables based on foreign key dependencies
table_order = [
    "effects",
    "weapon_groups",
    "regions",
    "armor_sets",
    "armor_equip_slots",
    "magic_types",
    "item_types",
    "key_item_types",
    "npc_encounters",
    "locations",
    "users",
    "items",
    "affinities",
    "weapons",
    "weapons_w_affinities",
    "gear",
    "npcs",
    "armors",
    "magic",
    "key_items",
    "bolsters",
    "ashes_of_war",
    "talismans",
    "spirit_ashes",
    "characters"
]

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "alihan2004",
    "database": "blg317e_eldenring"
}

# Function to insert data into a table
def insert_data(cursor, table_name, data):
    # Create a placeholder for the number of columns
    columns = ", ".join(data.columns)
    placeholders = ", ".join(["%s"] * len(data.columns))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        cursor.executemany(query, data.values.tolist())
    except Error as e:
        raise Exception(f"Error inserting data into {table_name}: {e}")

# Main function to process CSV files and insert data
def main():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Start a transaction
        connection.start_transaction()

        # Iterate over tables in the correct order
        for table in table_order:
            csv_file = f"{table}.csv"

            if not os.path.exists(csv_file):
                print(f"CSV file for table {table} not found. Skipping.")
                continue

            # Load data from CSV
            data = pd.read_csv(csv_file)
            if data.empty:
                print(f"CSV file for table {table} is empty. Skipping.")
                continue

            print(f"Inserting data into {table}...")
            insert_data(cursor, table, data)

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

    except Exception as e:
        # Rollback in case of any error
        if connection:
            connection.rollback()
        print(f"Error: {e}. Rolled back the transaction.")

    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
