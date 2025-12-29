import os
import datetime
import storage
import catalog
import patron
import circulation
import reports

BASE_DIR = "data"
BACKUP_DIR = "backups"

def main():
    storage.ensure_data_paths(BASE_DIR)
    books, patrons, loans = storage.load_state(BASE_DIR)
    while True:
        print("\n--- Library Management System ---")
        print("1. Librarian Menu")
        print("2. Patron Menu")
        print("3. Save & Exit")  
        choice = input("Select role: ")
        if choice == "1":
            pwd = input("Enter Librarian Password: ")
            if pwd == "librarian":
                librarian_menu(books, patrons, loans)
            else:
                print("Incorrect password.")
        elif choice == "2":
            patron_menu(books, patrons, loans)
        elif choice == "3":
            storage.save_state(BASE_DIR, books, patrons, loans)
            storage.backup_state(BASE_DIR, BACKUP_DIR)
            print("Data saved. Exiting.")
            break
        else:
            print("Invalid option.")

def librarian_menu(books, patrons, loans):
    while True:
        print("\n--- Librarian Menu ---")
        print("1. Add Book")
        print("2. Register Patron")
        print("3. View Overdue Report")
        print("4. View Circulation Stats")
        print("5. Back")
        cmd = input("Command: ")
        if cmd == "1":
            isbn = input("ISBN: ")
            title = input("Title: ")
            authors = input("Authors (comma sep): ").split(",")
            year = int(input("Year: "))
            genre = input("Genre: ")
            copies = int(input("Copies: "))
            book = {
                "isbn": isbn, "title": title, "authors": authors, 
                "year": year, "genre": genre, 
                "copies_owned": copies, "copies_available": copies
            }
            catalog.add_book(books, book)
            print("Book added.")    
        elif cmd == "2":
            name = input("Name: ")
            lid = input("Library ID: ")
            email = input("Email: ")
            pwd = input("Password: ")
            p_data = {
                "name": name, "library_id": lid, "email": email, 
                "password": pwd, "borrowing_limit": 5, "fines_owed": 0.0
            }
            patron.register_patron(patrons, p_data)
            print("Patron registered.")      
        elif cmd == "3":
            today = datetime.date.today().isoformat()
            overdue = reports.overdue_report(loans, today)
            for item in overdue:
                print(f"Overdue: {item['isbn']} by {item['library_id']}")       
        elif cmd == "4":
            stats = reports.circulation_stats(loans, books)
            print("Circulation Stats:", stats) 
        elif cmd == "5":
            break

def patron_menu(books, patrons, loans):
    lid = input("Enter Library ID: ")
    pwd = input("Enter Password: ")
    user = patron.authenticate_patron(patrons, lid, pwd) 
    if not user:
        print("Authentication failed.")
        return 
    while True:
        print(f"\n--- Welcome {user['name']} ---")
        print("1. Search Books")
        print("2. Checkout Book")
        print("3. Return Book")
        print("4. My Loans")
        print("5. Back")   
        cmd = input("Command: ")
        if cmd == "1":
            kw = input("Keyword: ")
            res = catalog.search_books(books, kw)
            for b in res:
                print(f"{b['title']} ({b['isbn']}) - Available: {b['copies_available']}")        
        elif cmd == "2":
            isbn = input("ISBN to checkout: ")
            res = circulation.checkout_book(books, patrons, loans, isbn, lid, 14)
            print(res) 
        elif cmd == "3":
            my_loans = circulation.list_patron_loans(loans, lid)
            for l in my_loans:
                if not l['return_date']:
                    print(f"ID: {l['loan_id']} | Book: {l['isbn']}")
            loan_id = input("Loan ID to return: ")
            res = circulation.return_book(books, patrons, loans, loan_id, datetime.date.today().isoformat())
            print(res)   
        elif cmd == "4":
            my_loans = circulation.list_patron_loans(loans, lid)
            for l in my_loans:
                status = "Returned" if l['return_date'] else f"Due: {l['due_date']}"
                print(f"{l['isbn']} : {status}")        
        elif cmd == "5":
            break
if __name__ == "__main__":
    main()