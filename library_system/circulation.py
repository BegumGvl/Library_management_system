import datetime

def checkout_book(books: list, patrons: list, loans: list, isbn: str, library_id: str, loan_period_days: int) -> dict:
    book = next((b for b in books if b['isbn'] == isbn), None)
    patron = next((p for p in patrons if p['library_id'] == library_id), None)
    if not book or not patron:
        return {"error": "Book or Patron not found"}
    if book['copies_available'] < 1:
        return {"error": "No copies available"}
    active_loans = [l for l in loans if l['library_id'] == library_id and l['return_date'] is None]
    if len(active_loans) >= patron.get('borrowing_limit', 5):
        return {"error": "Borrowing limit reached"}
    book['copies_available'] -= 1
    due_date = (datetime.date.today() + datetime.timedelta(days=loan_period_days)).isoformat()
    loan = {
        "loan_id": f"{library_id}-{isbn}-{datetime.date.today().isoformat()}",
        "isbn": isbn,
        "library_id": library_id,
        "checkout_date": datetime.date.today().isoformat(),
        "due_date": due_date,
        "return_date": None
    }
    loans.append(loan)
    return loan

def return_book(books: list, patrons: list, loans: list, loan_id: str, return_date: str) -> dict:
    loan = next((l for l in loans if l['loan_id'] == loan_id), None)
    if not loan:
        return {"error": "Loan not found"}
    if loan['return_date']:
        return {"error": "Book already returned"}
    loan['return_date'] = return_date
    book = next((b for b in books if b['isbn'] == loan['isbn']), None)
    if book:
        book['copies_available'] += 1
    due = datetime.date.fromisoformat(loan['due_date'])
    ret = datetime.date.fromisoformat(return_date)
    fine = 0.0
    if ret > due:
        overdue_days = (ret - due).days
        fine = overdue_days * 0.50 
        apply_fine(patrons, loan['library_id'], fine)
    return {"status": "returned", "fine": fine}

def renew_loan(loans: list, loan_id: str, extension_days: int) -> dict:
    loan = next((l for l in loans if l['loan_id'] == loan_id), None)
    if not loan:
        return {"error": "Loan not found"}
    if loan['return_date']:
        return {"error": "Cannot renew returned book"}
    current_due = datetime.date.fromisoformat(loan['due_date'])
    new_due = current_due + datetime.timedelta(days=extension_days)
    loan['due_date'] = new_due.isoformat()
    return loan

def apply_fine(patrons: list, library_id: str, amount: float) -> dict:
    patron = next((p for p in patrons if p['library_id'] == library_id), None)
    if patron:
        patron['fines_owed'] = patron.get('fines_owed', 0.0) + amount
        return patron
    return {}

def list_patron_loans(loans: list, library_id: str) -> list:
    return [l for l in loans if l['library_id'] == library_id]
