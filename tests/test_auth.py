import pytest


def test_login(client):
    # Testing to see if a user can log in
    response = client.get('/')
    assert b'<h2>Log in</h2>' in response.data
    assert b'New? sign up' in response.data

    response = client.get('/', data={'email': 'Thommond@protonmail.com',
    'password': 'PASSWORD'})

    assert b'<h2>Welcome to Simple Todo</h2>' in response.data

    client.get('/logout')

def test_register(client):
    #Testing to see if a new user can be created and log in
    response = client.get('/register')
    assert b'<h2>Sign Up</h2>' in response.data
    assert b'Already a user? Log In' in response.data

    response = client.post('/register', data={'email': 'joe@gmail.com',
    'password': 'qwerty'}, follow_redirects=True)

    assert b'<h2>Log In</h2>' in response.data

    response = client.post('/', data={'email': 'joe@gmail.com',
     'password': 'qwerty'}, follow_redirects=True)

    assert b'<h2>Welcome to Simple Todo</h2>' in response.data

    client.get('/logout')
