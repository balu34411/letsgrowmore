import os
import shutil
from cryptography.fernet import Fernet
import getpass

# Function to generate a key and save it to a file (for encryption)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key from a file
def load_key():
    return open("key.key", "rb").read()

# Encrypt the folder name to make it hidden
def encrypt_folder_name(folder_name, key):
    fernet = Fernet(key)
    encrypted_name = fernet.encrypt(folder_name.encode())
    return encrypted_name

# Decrypt the folder name to make it accessible
def decrypt_folder_name(encrypted_name, key):
    fernet = Fernet(key)
    decrypted_name = fernet.decrypt(encrypted_name).decode()
    return decrypted_name

# Lock the folder by renaming it to an encrypted name
def lock_folder(folder_name, key):
    encrypted_name = encrypt_folder_name(folder_name, key)
    os.rename(folder_name, encrypted_name)
    print(f"Folder '{folder_name}' is now locked.")

# Unlock the folder by renaming it back to its original name
def unlock_folder(encrypted_name, folder_name, key):
    decrypted_name = decrypt_folder_name(encrypted_name, key)
    os.rename(encrypted_name, decrypted_name)
    print(f"Folder '{decrypted_name}' is now unlocked.")

# Check password to allow unlocking of the folder
def check_password():
    correct_password = "password123"  # You can modify this with more secure password management
    entered_password = getpass.getpass("Enter your password: ")
    if entered_password == correct_password:
        print("Password correct!")
        return True
    else:
        print("Incorrect password.")
        return False

# Main program for folder lock/unlock
def main():
    folder_name = input("Enter the folder name you want to lock: ")
    
    # Check if folder exists
    if not os.path.exists(folder_name):
        print("The folder does not exist.")
        return
    
    # Ask the user if they want to lock or unlock the folder
    action = input("Do you want to lock or unlock the folder? (lock/unlock): ").strip().lower()
    
    # Generate and load the encryption key
    if not os.path.exists("key.key"):
        generate_key()  # Only generate the key if it doesn't exist
    key = load_key()

    if action == "lock":
        # Lock the folder
        lock_folder(folder_name, key)
    elif action == "unlock":
        # Request password for unlocking
        if check_password():
            # Find the encrypted folder name
            encrypted_name = encrypt_folder_name(folder_name, key)
            if os.path.exists(encrypted_name):
                # Unlock the folder
                unlock_folder(encrypted_name, folder_name, key)
            else:
                print("The folder is not locked.")
        else:
            print("Failed to unlock. Incorrect password.")
    else:
        print("Invalid action. Please choose 'lock' or 'unlock'.")

if __name__ == "__main__":
    main()
