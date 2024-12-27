from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

DEBUG = True
PORT = 8080

# Read environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "game_database")

SECRET_KEY = 'your-secret-key-here'  # Replace with a secure secret key
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
