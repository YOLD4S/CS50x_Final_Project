 CS50x Final Project - Elden Ring Wiki

This is a web application that allows users to view and modify various elements of the game Elden Ring. The application provides a comprehensive database of items, weapons, armors, NPCs, and more, all sourced from the game. Users can explore detailed information about each item and even contribute by adding or modifying entries.

## Contributors

- Arif Eren Yoldaş
- Alihan Esen
- Hasan İnanç Güney

## Technologies Used

### Languages and Frameworks

- **Python**: The core backend logic is implemented using Python.
- **Flask**: This lightweight WSGI web application framework is used to build  and deploy the web application.
- **HTML**: Used for structuring the web pages.
- **CSS**: Used for styling the web pages.
- **JavaScript**: Used for enhancing user interactions on the web pages.
- **MySQL**: The relational database management system used to store and manage the data.

### Data Source

The data about the items of the game was obtained from the following link:
[Google Spreadsheet](https://docs.google.com/spreadsheets/d/1x6LvzrqA9LWXPbzPZBDG8aL4N3Xc_ZxtEFMWpUxQj5c/edit?gid=1415047826#gid=1415047826)

The data retrieved from the link was not suitable for direct integration into the web application. To ensure compatibility and usability, certain portions were extracted and reformatted before being incorporated into the website.

## Project Structure

### Directories and Files

- **data/**: Includes the source data that the database is built on.
  - `affinities.csv`
  - `armor_equip_slots.csv`
  - `armor_sets.csv`
  - `armors.csv`
  - `ashes_of_war.csv`
  - `bolsters.csv`
  - `characters.csv`
  - `insert_csv_to_db.py`: Script to insert CSV data into the database.
  - `item_types.csv`
  - `items.csv`
  - `key_item_types.csv`
  - `key_items.csv`
  - `locations.csv`
  - `magic_types.csv`
  - `magic.csv`
  - `npc_encounters.csv`
  - `npcs.csv`
  - `weapons.csv`

- **database/**: Includes the SQL scripts used to create and configure the tables of the database.
  - `tables.sql`: Script to create the database tables.
  - `foreign_keys.sql`: Script to create the foreign keys.

- **Website_Files/**: Contains the main application files.
  - `db.py`: Functions to connect and disconnect the MySQL database.
  - `settings.py`: Configurations of the application.
  - `views.py`: Includes the display functions and routes.
  - `server.py`: Main code that runs and deploys the application with Flask.
  - **templates/**: HTML documents for each page displayed.
    - `layout.html`: Base layout template.
    - `home.html`: Home page template.
    - `armor_detail.html`: Armor detail page template.
    - `armors.html`: Armors listing page template.
    - `editor/`: Templates for the editor pages.
      - `armors_add.html`: Template for adding new armors.
      - `armors_delete.html`: Template for deleting armors.
      - `armors_modify.html`: Template for modifying armors.
      - `weapons_add.html`: Template for adding new weapons.
      - `weapons_delete_navigate.html`: Template for navigating and deleting weapons.
      - `weapons_modify.html`: Template for modifying weapons.
  - **static/**: Contains the icons, images, and stylesheet.
    - `styles.css`: Main stylesheet.
    - `images/`: Various images used in the application.
    - `icons/`: Icons used in the application.
    - `uploads/`: Profile pictures uploaded by users.

- **ERD.png, ERD2.png**: Images of the entity-relationship diagram of the database.

## How to Run the Project

1. **Create the Database Tables**:
   Run `tables.sql` in your MySQL database to create the necessary tables.

2. **Insert Data into the Database**:
   Configure and run the Python script `insert_csv_to_db.py` inside the `data/` folder to insert the data into the database.

3. **Create Foreign Keys**:
   Run `foreign_keys.sql` in your MySQL database to create the foreign keys.

4. **Configure Environment Variables**:
   Create a `.env` file with your database credentials. The `.env` file should include the following variables:
   ```env
   DB_HOST=your_database_host
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_NAME=your_database_name
   ```

5. **Install Required Packages**:
   Make sure you have the required packages installed. You can find them in the 

requirements.txt file. Install them using the following command:
   ```sh
   pip install -r Website_Files/requirements.txt
   ```

6. **Run the Server**:
   Navigate to the Website_Files directory and run server.py  to start the server:

   ```sh
   python server.py
   ```

7. **Access the Application**:
   Open your web browser and go to `http://localhost:5000` to access the application.

## Bonus: Become an Admin

To become an admin, enter "CokGizli" in the admin request field after creating an account.

## Additional Information

### .gitignore

The .gitignore file includes the following entries to exclude unnecessary files and directories from the repository:
```ignore
.idea/
__pycache__/
.DS_Store
.env
.venv/
Website_Files/flask_session/
/Website_Files/static/uploads/
```

### .gitattributes

The .gitattributes file includes the following entry to handle text file normalization:
```properties
* text=auto
```

### Acknowledgements

We would like to thank the creators of Elden Ring for providing such an amazing game and the community for their contributions to the game's data.
