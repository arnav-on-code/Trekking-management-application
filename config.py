import os 
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    ADMIN_NAME = os.getenv('ADMIN_NAME')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    ADMIN_PHONE = os.getenv('ADMIN_PHONE')

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set. Please configure it in the .env file.")
    
    if not ADMIN_NAME or not ADMIN_EMAIL or not ADMIN_PASSWORD or not ADMIN_PHONE:
        raise ValueError("One or more admin details are missing. Please configure them in the .env file.")

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, "instance", "trekking.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    