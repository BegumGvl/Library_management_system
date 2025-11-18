import json

def load_books(path: str) -> list:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_books(path: str, books: list) -> None:
    with open(path, 'w') as file:
        json.dump(books, file, indent=4)

def add_book(books: list, book_data: dict) -> dict:
    books.append(book_data)
    return book_data

def list_books(books: list):
    for book in books:
        print(f"- {book['title']} by {book['author']} ({book['genre']})")

def search_books(books: list, keyword: str) -> list:
    results = []
    keyword = keyword.lower() 
    
    for book in books:
        if keyword in book['title'].lower() or keyword in book['author'].lower():
            results.append(book)
    return results

