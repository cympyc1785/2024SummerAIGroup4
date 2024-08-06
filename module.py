from dotenv import load_dotenv
import os

# load .env
load_dotenv()

API_KEY = os.environ.get('API_KEY')

def call():
    print("hello")