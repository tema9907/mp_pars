from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
    MQCONNECTION = os.getenv("MQCONNECTION")