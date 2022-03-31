# ############### CURRENTLY NOT IN USE #########################

import os
from sqlite3 import dbapi2
import tempfile
import pytest
from flask import Flask, g, session

from app import create_app
from user_db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


# Tests user registerations
@pytest.fixture
def auth(client):
    return AuthActions(client)

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

# tests error messages
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))

def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

# Tests login error messages as well as whether user is in session when logged in
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/tickets'

    # Checks if user is in session
    with client:
        client.get('/tickets')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

# tests error handling
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Username does not exist'),
    ('test', 'a', b'Incorrect password.'),
))
# validates login information
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

# checks that once user logs out, user is no longer in session
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session