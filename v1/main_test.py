
import webtest

import main

##NOT TESTED##
def test_admin(testbed, login):
    app = webtest.TestApp(main.app)

    response = app.get('/admin')
    assert 'You are not logged in' in response.body

    login()
    response = app.get('/admin')
    assert 'You are not an administrator' in response.body

    login(is_admin=True)
    response = app.get('/admin')
    assert 'You are an administrator' in response.body
