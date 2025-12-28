import json

def load_patrons(path: str) -> list:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_patrons(path: str, patrons: list) -> None:
    with open(path, 'w') as f:
        json.dump(patrons, f, indent=4)

def register_patron(patrons: list, patron_data: dict) -> dict:
    patrons.append(patron_data)
    return patron_data

def authenticate_patron(patrons: list, library_id: str, password: str) -> dict | None:
    for p in patrons:
        if p['library_id'] == library_id and p.get('password') == password:
            return p
    return None

def update_patron_contact(patrons: list, library_id: str, contact_updates: dict) -> dict:
    for p in patrons:
        if p['library_id'] == library_id:
            p.update(contact_updates)
            return p
    return {}