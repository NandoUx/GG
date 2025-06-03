import instaloader
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()
IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')

L = instaloader.Instaloader()

def save_session():
    L.save_session_to_file(f"{IG_USERNAME}_session")

def login():
    try:
        print(f"Logging in as: {IG_USERNAME}")
        L.login(IG_USERNAME, IG_PASSWORD)
        save_session()
        print("Login successful, session saved.")
    except Exception as e:
        print(f"Login failed: {e}")

if __name__ == "__main__":
    login()
