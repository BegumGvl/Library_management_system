import json
PATRON_FILE = 'data/patrons.json'



def load_patrons(path: str) -> list:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    


def save_patrons(path: str, patrons: list) -> None: 
    try:
        with open(path, 'w') as file:
            json.dump(patrons, file, indent=4)
    except FileNotFoundError:
        print("Error, couldn't save data try again or make sure the file exists")



def register_patron(patrons: list, patron_data: dict) -> dict: 
    for p in patrons:
        if p['library_id'] == patron_data['library_id']:
            print("Error, library ID already exists.")
            return {}
    patrons.append(patron_data)
    print(f"User {patron_data['name']} registered successfully.")
    return patron_data



def authenticate_patron(patrons: list, library_id: str, password: str) -> dict | None: 
    for p in patrons:
        if p['library_id'] == library_id and p['password'] == password:
            print(f"User {p['name']} Loggedin successfully.")
            return p
    print("Login failed. Check library ID and password.")
    return None



def update_patron_contact(patrons: list, library_id: str, contact_updates: dict) -> dict:
    for p in patrons:
        if p['library_id'] == library_id:
            if 'email' in contact_updates:
                p['email'] = contact_updates['email']
            if 'contact_info' in contact_updates:
                p['contact_info'] = contact_updates['contact_info']
            print(f"User {p['name']}'s contact information updated.")
            return p
    print("Patron not found.")
    return {}