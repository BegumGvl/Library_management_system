import unittest
import os
import shutil
import json
import catalog
import patron
import circulation
import reports

class TestLibrarySystem(unittest.TestCase):
    
    def setUp(self):
        self.books = []
        self.patrons = []
        self.loans = []
        self.book_data = {
            "isbn": "123", "title": "Test Book", "authors": ["Me"], 
            "year": 2024, "genre": "Fiction", 
            "copies_owned": 2, "copies_available": 2
        }
        self.patron_data = {
            "name": "John", "library_id": "P1", "email": "j@test.com", 
            "password": "pass", "borrowing_limit": 2, "fines_owed": 0.0
        }
        catalog.add_book(self.books, self.book_data)
        patron.register_patron(self.patrons, self.patron_data)

    def test_checkout_success(self):
        res = circulation.checkout_book(self.books, self.patrons, self.loans, "123", "P1", 7)
        self.assertIn("loan_id", res)
        self.assertEqual(self.books[0]['copies_available'], 1)

    def test_checkout_fail_limit(self):
        self.patrons[0]['borrowing_limit'] = 0
        res = circulation.checkout_book(self.books, self.patrons, self.loans, "123", "P1", 7)
        self.assertEqual(res['error'], "Borrowing limit reached")

    def test_return_and_fine(self):
        loan = circulation.checkout_book(self.books, self.patrons, self.loans, "123", "P1", 7)
        loan_id = loan['loan_id']
        late_date = "2025-01-01" 
        loan['due_date'] = "2024-12-01"
        
        circulation.return_book(self.books, self.patrons, self.loans, loan_id, late_date)
        self.assertTrue(self.patrons[0]['fines_owed'] > 0)

    def test_search_filter(self):
        res = catalog.filter_books(self.books, genre="Fiction")
        self.assertEqual(len(res), 1)
        res = catalog.filter_books(self.books, genre="Non-Fiction")
        self.assertEqual(len(res), 0)

if __name__ == '__main__':
    unittest.main()