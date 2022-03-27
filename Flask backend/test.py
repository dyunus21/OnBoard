import os
import unittest
 
from app import app
 
TEST_DB = 'test.db'
 
class Tests(unittest.TestCase):
# executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
    
    # executed after each test
    def tearDown(self):
        pass
 
#### tests ####
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.app.get('/accregister', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/acclogin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_forgot(self):
        response = self.app.get('/forgot_password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_reset(self):
        response = self.app.get('/reset', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_tickets(self):
        response = self.app.get('/tickets', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_business_dashboard(self):
        response = self.app.get('/business_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_dashboard(self):
        response = self.app.get('/user_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main()