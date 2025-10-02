# ----------------------------- import modules ----------------------------------

import os
import json
import base64 # base 64 str encoding for json file format
from cryptography.fernet import Fernet

# ----------------------------- variables --------------------------------------

KEY_FILE = "filekey.key"  # for en/decryption
TABLE_SIZE = 11
TABLE_NAME = 'data_table'

# test variables 
input_name = "Test service"
input_name_2 = "openweathermap"
input_name_3 = "anothertest"
input_name_4 = "doesnotmatter"

input_value = "1230480"
input_value_2 = "456545232"
input_value_3 = "999"
input_value_4 = "12348"

input_name_list = [input_name, input_name_2, input_name_3, input_name_4]
input_value_list = [input_value, input_value_2, input_value_3, input_value_4]

# ----------------------------- utility functions -----------------------------

def load_or_create_key():
    # for en/decryption

    if os.path.exists(KEY_FILE):
        # Load existing key
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    else:
        # Generate new key and save
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return key


def encrypt(to_encrypt:str) -> str:
    # str must be encoded into bytes with encode()
    encrypted = fernet.encrypt(to_encrypt.encode())
    # Convert to base64 string for JSON
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt(to_decrypt:str) -> str:
    encrypted_bytes = base64.b64decode(to_decrypt.encode("utf-8"))
    decrypted_bytes = fernet.decrypt(encrypted_bytes) # bytes
    # decode to return a str
    return decrypted_bytes.decode("utf-8") 


def create_hash_table(size=TABLE_SIZE):
    print(f"\n+++ Creating new data table with size {TABLE_SIZE} +++")
    return [[] for _ in range(size)]


def load_table(filename=f"{TABLE_NAME}.json", size=TABLE_SIZE):
    # If file does not exist: create a new empty table
    if not os.path.exists(filename):
        return create_hash_table(size)

    try:
        with open(filename, "r") as f:
            data = json.load(f)

        # Validate: must be a list of lists
        if isinstance(data, list) and len(data) == size:
            print("\n+++ Loading data table from json +++")
            return data
        else:
            # File is invalid or wrong size:reset
            return create_hash_table(size)

    except (json.JSONDecodeError, IOError):
        # File unreadable or corrupted: reset
        return create_hash_table(size)


def save_table(table,filename=f"{TABLE_NAME}.json"):
    with open(filename, "w") as f:
        json.dump(table, f)


def get_hash_index(key: str, table_size=TABLE_SIZE) -> int:
    """
    The Hash function is used to get the index of the hash table at 
    which a value assosiated with a key is stored = mapping. 
    """
    key_sum = transform_key(key)
    return key_sum % table_size


def transform_key(key:str) -> int:
    """
    Transform a key (character str) to a number by summing up the ascii codes of each letter.
    This value can be used to calculate the table index with the hash func.
    """
    ascii_values = [ord(key[i]) for i in range(len(key))]
    return sum(ascii_values)


def table_insert(table, key, value, verbose=0):

    # Calculate hash table index using key
    index = get_hash_index(key, len(table))
    
    # Encrypt value
    encypted_value = encrypt(value)

    # Check if key already exists, update it
    for i, (k, _) in enumerate(table[index]):
        if k == key:
            table[index][i] = (key, encypted_value)
            return
    # Otherwise, append to the list  
    table[index].append((key, encypted_value))
    print(f"Saved {key}")
    
    if verbose:
        #print(f"\nInserting ({key}, {encypted_value}) at index {index}")
        # collision handling by chaining (add entries to list)
        if not table[index]:
            print("Free position!")
        else:
            nr_entries = len(table[index])
            print(f"There are {nr_entries} entries at this position.")
     

def table_lookup(hash_table, key):

    # Calculate hash table index using key
    index = get_hash_index(key, len(hash_table))
    # print(f"Searching for key {key} at index {index}")

    # Looking trough each entry at the index (chaining)
    for entry in hash_table[index]:

        if entry[0] == key:
            # print(f"+++ Found: {entry[0]} +++")
            # Decrypt value
            decrypted_value = decrypt(entry[1])
            return decrypted_value
        
    return None


def input_handling():
    # itneractive input mode
    while True:
        # Ask for input until the user types 'q'
        ask_job = input("\n+++ What do you want to do? +++" \
        "\n    - Type 's' to save a new key." \
        "\n    - Type 'l' lookup a key." \
        "\n    - Type 'q' to quit. ").lower().strip()
        
        if ask_job == 'q' or ask_job =='quit':
            print('+++ Closing the program +++')
            return
            
        if ask_job == 's':
            new_key_name = input("\n    For which service do you want to save a new key: ").strip()
            new_key_value = input("\n    What is the new API key: ").strip()
            table_insert(data_table, new_key_name, new_key_value)
            save_table(data_table)

        elif ask_job == 'l':
            load_key_value = input("    \nFor which service do you want to get the key: ").strip()
            api_key = table_lookup(data_table, load_key_value)
            if api_key:
                print(f"The key for {load_key_value} is:\n{api_key}")
            else:
                print(f"Could not find {load_key_value} in the table.")
        else:
            print("   - No valid command.") 

# ----------------------------- main program ---------------------------------- 

if __name__ == "__main__":
    
    print("+++ Welcome to your API secrets manager. +++")
    # check for key 
    CRYPTO_KEY = load_or_create_key()
    # create Fernet class instance with the encryption key
    fernet = Fernet(CRYPTO_KEY)
    # load or create table
    data_table = load_table()
    # Ask for action
    input_handling()
    

