import json

def overdue_report(loans: list, current_date: str) -> list:
    overdue = []
    curr = datetime.date.fromisoformat(current_date) if 'datetime' not in globals() else None 
    import datetime
    curr = datetime.date.fromisoformat(current_date)
    for loan in loans:
        if loan['return_date'] is None:
            due = datetime.date.fromisoformat(loan['due_date'])
            if curr > due:
                overdue.append(loan)
    return overdue

def fines_summary(patrons: list) -> dict:
    summary = {}
    for p in patrons:
        if p.get('fines_owed', 0) > 0:
            summary[p['library_id']] = p['fines_owed']
    return summary

def circulation_stats(loans: list, books: list) -> dict:
    isbn_counts = {}
    for loan in loans:
        isbn = loan['isbn']
        isbn_counts[isbn] = isbn_counts.get(isbn, 0) + 1  
    stats = {}
    for isbn, count in isbn_counts.items():
        book = next((b for b in books if b['isbn'] == isbn), None)
        title = book['title'] if book else "Unknown"
        stats[title] = count
    return stats

def export_report(report: dict | list, filename: str) -> str:
    with open(filename, 'w') as f:
        if isinstance(report, list):
            for item in report:
                f.write(json.dumps(item) + "\n")
        else:
            json.dump(report, f, indent=4)
    return filename