import json

def ensure_data_paths(base_dir: str) -> None: 
    import os
    data_paths = [
        os.path.join(base_dir, 'data'),
        os.path.join(base_dir, 'data', 'books.json'),
        os.path.join(base_dir, 'data', 'patrons.json'),
        os.path.join(base_dir, 'data', 'loans.json'),
    ]
    for path in data_paths:
        if not os.path.exists(path):
            if path.endswith('.json'):
                with open(path, 'w') as file:
                    json.dump([], file)
            else:
                os.makedirs(path)

def load_state(base_dir: str) -> tuple[list, list, list]: 
    import os
    books_path = os.path.join(base_dir, 'data', 'books.json')
    patrons_path = os.path.join(base_dir, 'data', 'patrons.json')
    loans_path = os.path.join(base_dir, 'data', 'loans.json')
    with open(books_path, 'r') as file:
        books = json.load(file)
    with open(patrons_path, 'r') as file:
        patrons = json.load(file)
    with open(loans_path, 'r') as file:
        loans = json.load(file)
    return books, patrons, loans

def save_state(base_dir: str, books: list, patrons: list, loans: list) -> None: 
    import os
    books_path = os.path.join(base_dir, 'data', 'books.json')
    patrons_path = os.path.join(base_dir, 'data', 'patrons.json')
    loans_path = os.path.join(base_dir, 'data', 'loans.json')
    with open(books_path, 'w') as file:
        json.dump(books, file, indent=4)
    with open(patrons_path, 'w') as file:
        json.dump(patrons, file, indent=4)
    with open(loans_path, 'w') as file:
        json.dump(loans, file, indent=4)


def backup_state(base_dir: str, backup_dir: str) -> list[str]: 
    import os
    import shutil
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backup_files = []
    for filename in ['books.json', 'patrons.json', 'loans.json']:
        src = os.path.join(base_dir, 'data', filename)
        dst = os.path.join(backup_dir, f"{filename}.bak")
        shutil.copy2(src, dst)
        backup_files.append(dst)
    return backup_files

def validate_catalog_schema(books: list) -> bool: 
    required_fields = {'title', 'author', 'isbn', 'copies_total', 'copies_available'}
    for book in books:
        if not required_fields.issubset(book.keys()):
            return False
    return True