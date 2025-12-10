import datetime

def checkout_book(books, patrons, loans, isbn, library_id, loan_period_days):
    book_found = None
    for b in books:
        if b['isbn'] == isbn:
            book_found = b
            break
    if book_found is None:
        return {'success': False, 'message': 'Book not found'}
    if book_found['copies_available'] < 1:
        return {'success': False, 'message': 'No copies available'}
    patron_found = None
    for p in patrons:
        if p['library_id'] == library_id:
            patron_found = p
            break
    if patron_found is None:
        return {'success': False, 'message': 'Patron not found'}
    today = datetime.date.today()
    due_date = today + datetime.timedelta(days=loan_period_days)
    loan_id = str(len(loans) + 1)
    new_loan = {
        'loan_id': loan_id,
        'isbn': isbn,
        'library_id': library_id,
        'borrow_date': today,
        'due_date': due_date,
        'returned': False
    }
    loans.append(new_loan)
    book_found['copies_available'] -= 1
    return {'success': True, 'message': 'Book checked out successfully', 'loan_id': loan_id, 'due_date': str(due_date)}

def return_book(books, patrons, loans, loan_id, return_date_str):
    loan_found = None
    for loan in loans:
        if loan['loan_id'] == loan_id:
            loan_found = loan
            break
    if loan_found is None:
        return {'success': False, 'message': 'Loan not found'}
    if loan_found['returned'] == True:
        return {'success': False, 'message': 'Book already returned'}
    loan_found['returned'] = True
    book_found = None
    for b in books:
        if b['isbn'] == loan_found['isbn']:
            book_found = b
            break
    if book_found:
        book_found['copies_available'] += 1
    date_format = "%Y-%m-%d"
    due_date = datetime.datetime.strptime(loan_found['due_date'], date_format).date()
    return_date = datetime.datetime.strptime(return_date_str, date_format).date()
    overdue_days = (return_date - due_date).days
    fine_amount = 0.0
    if overdue_days > 0:
        daily_fine_rate = 1.0 
        fine_amount = overdue_days * daily_fine_rate
        fine_result = apply_fine(patrons, loan_found['library_id'], fine_amount)
        if not fine_result.get('success', False):
            return {'success': False, 'message': f"Book returned, but fine application failed: {fine_result.get('message', '')}", 'fine': fine_amount}
    return {'success': True, 'message': 'Book returned', 'fine': fine_amount}

def renew_loan(loans, loan_id, extension_days):
    loan_found = None
    for loan in loans:
        if loan['loan_id'] == loan_id:
            loan_found = loan
            break
    if loan_found is None:
        return {'success': False, 'message': 'Loan not found'}
    if loan_found['returned'] == True:
        return {'success': False, 'message': 'Cannot renew returned book'}
    date_format = "%Y-%m-%d"
    current_due_date = datetime.datetime.strptime(loan_found['due_date'], date_format).date()
    new_due_date = current_due_date + datetime.timedelta(days=extension_days)
    loan_found['due_date'] = str(new_due_date)
    return {'success': True, 'message': 'Loan renewed', 'new_due_date': str(new_due_date)}

def apply_fine(patrons, library_id, amount):
    patron_found = None
    for p in patrons:
        if p['library_id'] == library_id:
            patron_found = p
            break 
    if patron_found:
        current_fines = patron_found.get('fines_owed', 0.0)
        patron_found['fines_owed'] = current_fines + amount
        return {'success': True, 'message': 'Fine applied'}
    return {'success': False, 'message': 'Patron not found'}

def list_patron_loans(loans, library_id):
    patron_loans = []
    for loan in loans:
        if loan['library_id'] == library_id:
            patron_loans.append(loan)
    return patron_loans

