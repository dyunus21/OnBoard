import os
import unittest
import app
from app import app, User,account_registration
from flask_login import FlaskLoginClient,login_user
from flask.testing import FlaskClient
from flask import url_for, g,session
from flask_sqlalchemy import SQLAlchemy
import pytest
# from flask_tracking.test_base import BaseTestCase

app.test_client_class = FlaskClient
 
TEST_DB = 'test.db'

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketsdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aiuhewr9y9q2392304iuahi3'
# app.run(debug = False)
db = SQLAlchemy(app)

app = app.test_client()
    
class Tests(unittest.TestCase):
    
    # executed after each test
    def tearDown(self):
        pass
 
#### tests each page ####
 
    def test_main_page(self):
        response = app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = app.get('/accregister', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        u_curr = User(username = "this5", emailAddress = "email5", passwordHash = "pass", userType = "Individual")
        db.session.add(u_curr)
        db.session.commit()
        exists = db.session.query(db.exists().where(User.username == 'this5')).scalar()
        
        self.assertEqual(exists, True)
        db.session.delete(u_curr)
        db.session.commit()
        exists = db.session.query(db.exists().where(User.username == 'this5')).scalar()
        self.assertEqual(exists, False)

    def test_login(self):
        response = app.get('/acclogin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_forgot(self):
        response = app.get('/forgot_password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_reset(self):
        response = app.get('/reset', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_tickets(self):
        response = app.get('/tickets', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_business_dashboard(self):
        response = app.get('/business_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_dashboard(self):
        response = app.get('/user_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

  
if __name__ == "__main__":
    unittest.main()