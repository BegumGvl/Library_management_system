# Library Management System
A terminal-driven library system that maintains book inventory, borrower accounts,
and circulation history.

## What the Project Features
* **main.py** (The entry point, CLI navigation)
* **catalog.py** (Search, add, remove books)
* **patron.py** (User registration and login)
* **circulation.py** (Loans and due dates)
* **storage.py** (Save point and backup)
* **reports.py** (Generates overdue lists)
* **data/** (Directory where `books.json`, `patrons.json` and `loans.json` are stored)
  
## How to run:
* First of all Python 3.x must be installed on your system for it to run
* Open terminal and navigate the project folder then run the command `python main.py` for Windows or `python3 main.py` for MacOS/Linux

## Roles:
### Patron:
* Select **Patron Menu** on the main menu
* Login requires a valid Library ID and Password (You can use Library ID: `LIB001`, Password: `111`)
* Patron can search books, see books barrowed, check user loans and renew loans
### Librarian:
* Select **Librarian Menu** on the main menu
* Login requires Password (Enter `librarian` for password)
* Librarian can search catalog, checkout/return books, and view loan history 

## Workflows:
### Workflow 1 (For Librarian):
1.  Log in as a Librarian
2.  Select **Add Book**
3.  Enter the book details as prompted:
    * **ISBN**: Unique identifier (e.g., `001`)
    * **Title**: The name of the book
    * **Authors**: Name of the Author or Authors (comma-seperated)
    * **Year**: Publication year (integer)
    * **Genre**: Book category
    * **Copies**: Total number of physical copies owned
3.  The book will be saved to the inventory

### Workflow 2 (For Librarian):
1.  Log in as a Librarian
2.  Select **Register Patron**
3.  Enter the new user's details as prompted:
    * **Name**: Full name
    * **Library ID**: A unique ID for login (e.g., `P001`)
    * **Email**: Email address
    * **Password**: The password the patron will use to log in (e.g., `111`)
4.  The patron is registered

### Workflow 3 (For Librarian):
1.  Log in as a Librarian
2.  Select **View Overdue Report** to see a list of books that are currently checked out past their due date
3.  Select **View Circulation Stats** to see the most borrowed books

### Workflow 4 (For Patron):
1.  Log in as a Patron
2.  Select **Search Books**
    * Type a keyword (title, author, or ISBN)
    * The system displays matching books and the number of Copies Available
3.  Select **Checkout Book**
    * Enter the ISBN of the book you want (e.g., `001`)
    * The system checks if copies are available and if you are under your borrowing limit
    * If successful, the book is checked out for 14 days

### Workflow 5 (For Patron):
1.  Log in as a Patron
2.  Select **Return Book**
3.  The system displays your Active Loans
4.  Enter the Loan ID into the prompt (e.g., `LOAN1`)
    * The return date is recorded
    * If the book is late, a fine (`$0.50` per day) is calculated and added to your account

### Workflow 6 (For Patron):
1.  Log in as a Patron
2.  Select **My Loans**
3.  The system lists your entire history:
    * **Active**: Shows the Due Date
    * **Returned**: Shows "Returned" status

