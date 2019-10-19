
# [START all]
import os
import urllib
from google.appengine.api import users
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        name = 'User'
        isAdmin = False
        user = users.get_current_user()

        if user:
            name = user.nickname()
            url = users.create_logout_url('/')
            #url = users.create_logout_url(self.request.uri)
            urlText = 'Logout'
            if users.is_current_user_admin():
                isAdmin = True 
        else:
            url = users.create_login_url('/')
            #url = users.create_login_url(self.request.uri)
            urlText = 'Login'

        template_values = {
            'user': name,
            'url': url,
            'urlText': urlText,
            'isAdmin': isAdmin
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class AdminPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url('/')
            if users.is_current_user_admin():
                msg = 'You are an Admin.    </br><a href="{}">Logout As Admin</a>'.format(url)
                self.response.write(msg)
            else:
                msg = 'Sorry, Admin Access Only.    </br><a href="{}">Logout As User</a>'.format(url)
                self.response.write(msg)
        else:
            url = users.create_login_url('/')
            msg = 'Please Login: <a href="{}">Here</a>'.format(url)
            self.response.write(msg)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage)
], debug=True)
# [END all]
