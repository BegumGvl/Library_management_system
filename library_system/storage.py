import os
import json
import shutil
import catalog
import patron

def ensure_data_paths(base_dir: str) -> None:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    files = ["books.json", "patrons.json", "loans.json"]
    for f in files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            with open(path, 'w') as file:
                json.dump([], file)

def load_state(base_dir: str) -> tuple[list, list, list]:
    books_path = os.path.join(base_dir, "books.json")
    patrons_path = os.path.join(base_dir, "patrons.json")
    loans_path = os.path.join(base_dir, "loans.json")
    books = catalog.load_books(books_path)
    patrons = patron.load_patrons(patrons_path)
    with open(loans_path, 'r') as f:
        loans = json.load(f)   
    return books, patrons, loans

def save_state(base_dir: str, books: list, patrons: list, loans: list) -> None:
    books_path = os.path.join(base_dir, "books.json")
    patrons_path = os.path.join(base_dir, "patrons.json")
    loans_path = os.path.join(base_dir, "loans.json")
    catalog.save_books(books_path, books)
    patron.save_patrons(patrons_path, patrons)
    with open(loans_path, 'w') as f:
        json.dump(loans, f, indent=4)

def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    files = ["books.json", "patrons.json", "loans.json"]
    backed_up_files = []
    for f in files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(backup_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            backed_up_files.append(dst)      
    return backed_up_files

def validate_catalog_schema(books: list) -> bool:
    required_keys = {"isbn", "title", "authors", "year", "genre", "copies_owned", "copies_available"}
    for book in books:
        if not required_keys.issubset(book.keys()):
            return False
    return True