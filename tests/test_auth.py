import os
import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    # Test registration with valid data including avatar upload
    with open('flaskr/static/avatars/test_avatar.png', 'wb') as f:
        f.write(b'test avatar content')

    with open('flaskr/static/avatars/test_avatar.png', 'rb') as avatar:
        response = client.post(
            '/auth/register',
            data={'username': 'a', 'password': 'a', 'avatar': avatar}
        )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        user = get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone()
        assert user is not None
        assert user['avatar'] == 'test_avatar.png'

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

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

def test_like_requires_login(client):
    response = client.post('/like/1')
    assert response.headers["Location"] == "/auth/login"

    with client.session_transaction() as session:
        assert 'You need to be logged in to like posts.' in session['_flashes'][0][1]

@pytest.fixture
def auth(client):
    return AuthActions(client)

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