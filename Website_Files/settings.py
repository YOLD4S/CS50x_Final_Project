from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

DEBUG = os.getenv("DEBUG", True)
PORT = os.getenv("PORT", 8080)

# Read environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "game_database")

# Secret key is loaded from .env file
SECRET_KEY = os.getenv('SECRET_KEY', 'c9e225d2a6d53c85f83f595ce2a4f75b6c48e7f40c3b8452')
SESSION_PERMANENT = os.getenv("SESSION_PERMANENT", False)
SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")