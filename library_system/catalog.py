import json

def load_books(path: str) -> list:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(path: str, books: list) -> None:
    with open(path, 'w') as f:
        json.dump(books, f, indent=4)

def add_book(books: list, book_data: dict) -> dict:
    books.append(book_data)
    return book_data

def update_book(books: list, isbn: str, updates: dict) -> dict:
    for book in books:
        if book['isbn'] == isbn:
            book.update(updates)
            return book
    return {}

def search_books(books: list, keyword: str) -> list:
    keyword = keyword.lower()
    results = []
    for book in books:
        if (keyword in book['title'].lower() or 
            keyword in book['isbn'] or 
            any(keyword in author.lower() for author in book['authors'])):
            results.append(book)
    return results

def filter_books(books: list, genre: str | None = None, year: int | None = None) -> list:
    filtered = books
    if genre:
        filtered = [b for b in filtered if b['genre'].lower() == genre.lower()]
    if year:
        filtered = [b for b in filtered if b['year'] == year]
    return filtered