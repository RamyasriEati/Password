import hashlib
import os
from getpass import getpass
import random
from PIL import Image

# Mock database
user_db = {}

def hash_password(password):
    """Hash a password for storing."""
    salt = os.urandom(32)
    hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + hashed_pw

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    salt = stored_password[:32]
    stored_hash = stored_password[32:]
    hashed_pw = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return hashed_pw == stored_hash

def captcha():
    """Simple CAPTCHA to prevent bots."""
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    print(f"CAPTCHA: What is {num1} + {num2}?")
    answer = int(input())
    return answer == num1 + num2

def register():
    """User registration."""
    username = input("Enter username: ")
    if username in user_db:
        print("Username already exists.")
        return
    password = getpass("Enter password: ")
    hashed_pw = hash_password(password)
    
    # Example of graphical password (image selection)
    graphical_password = input("Choose an image as your graphical password (input the name of the image): ")
    
    user_db[username] = {
        "password": hashed_pw,
        "graphical_password": graphical_password
    }
    print("User registered successfully.")

def login():
    """User login."""
    username = input("Enter username: ")
    if username not in user_db:
        print("User not found.")
        return
    
    password = getpass("Enter password: ")
    if not verify_password(user_db[username]['password'], password):
        print("Incorrect password.")
        return

    graphical_password = input("Enter your graphical password (input the name of the image): ")
    if user_db[username]['graphical_password'] != graphical_password:
        print("Incorrect graphical password.")
        return
    
    if captcha():
        print("Login successful!")
    else:
        print("CAPTCHA failed. Login failed.")

def main():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")

if name == "main":
    main()
