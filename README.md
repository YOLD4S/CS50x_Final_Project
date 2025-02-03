# CS50x Final Project - Elden Ring Wiki

This is a web application that users can see and modify the stuff of the game Elden Ring.

Contributors:
- Arif Eren Yoldaş
- Alihan Esen
- Hasan İnanç Güney

Languages:
This web apllication was made mostly with Python's Flask framework. In the design of web pages HTML and CSS were also utilized.
MySQL was also used to create and operate the database.

Data Source:
The data about the items of the game was obtained from the link below.
https://docs.google.com/spreadsheets/d/1x6LvzrqA9LWXPbzPZBDG8aL4N3Xc_ZxtEFMWpUxQj5c/edit?gid=1415047826#gid=1415047826

The data obtained from this link was in the csv format. To be integrated and used in the website it was reformatted.

Files:

## How to run the project

1- Run tables.sql in your database to create the tables.
2- Configure and run the python script inside the data/ folder to insert the data to the database.
3- Run foreign_keys.sql in you database to create the foreign keys.
4- Configure .env file with your database credentials.
5- Run server.py to start the server.

Bonus: To become an admin, enter "CokGizli" to the admin request field after creating an account.

Note: make sure you have the required packages installed. You can find them in the requirements.txt file.
