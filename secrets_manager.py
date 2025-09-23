TABLE_SIZE = 5

input_name = "Test service"
input_name_2 = "openweathermap"
input_name_3 = "anothertest"
input_name_4 = "doesnotmatter"

input_value = "1230480"
input_value_2 = "456545232"
input_value_3 = "999"
input_value_4 = "12348"

# TODO: store credentials in memory or a file
# TODO: encryt and decryt keys

# WIP

def create_hash_table(size=TABLE_SIZE):
    return [[] for _ in range(size)]


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


def table_insert(hash_table, key, value):

    # calculate hash table index using key
    index = get_hash_index(key, len(hash_table))
    print(f"\nInserting ({key}, {value}) at index {index}")

    # collision handling by chaining (add entries to list)
    if not hash_table[index]:
        print("free position!")
    else:
        nr_entries = len(hash_table[index])
        print(f"There are {nr_entries} entries at this position.")
        
    # append the new entry to the list    
    hash_table[index].append([key, value])


def table_retrieve(hash_table, key):

    # calculate hash table index using key
    index = get_hash_index(key, len(hash_table))
    print(f"Searching for key {key} at index {index}")

    # looking trough each entry at the index (chaining)
    for entry in hash_table[index]:

        if entry[0] == key:
            print(f"Found value: {entry[0]}")
            return entry[1]
        
    print("Key not found")
    return None
        

# ------------ testing code --------------------------

# create new table
new_table = create_hash_table()

# save values
input_name_list = [input_name, input_name_2, input_name_3, input_name_4]
input_value_list = [input_value, input_value_2, input_value_3, input_value_4]
for i in range(len(input_name_list)):
    table_insert(new_table, input_name_list[i], input_value_list[i])
print(new_table)

# retrieve value
get_value = table_retrieve(new_table, input_name_3)
print(f"Retrieving value: {get_value}")
