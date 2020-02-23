
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

x = { 
    "user": None,
    "name": None,
    "isAdmin": False,
    "isAuth": False,
    "access_url": "",
    "access_prompt": "",
    "urlText": "",
    "url":""
}

class MainPage(webapp2.RequestHandler):
    def get(self):
        name = 'User'
        isAdmin = False
        user = users.get_current_user()

        if user:
            name = user.nickname()
            url = users.create_logout_url('/')
            #url = users.create_logout_url(self.request.uri)
            x["name"] = name
            x["isAuth"] = True
            x['urlText'] = "Login"
            x['url'] = url
            if users.is_current_user_admin():
                x["isAdmin"] = True
        else:
            url = users.create_login_url('/')
            #url = users.create_login_url(self.request.uri)
            x["isAdmin"] = False
            x["isAuth"] = False
            url = users.create_login_url("/")
            x['urlText'] = "Login"
            x['url'] = url

        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(x))

class AdminPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url('/')
            x["isAuth"] = True
            x['user'] = user
            x['name'] = user.nickname()
            if users.is_current_user_admin():
                x['msg'] = 'You are an Admin.    </br><a href="{}">Logout As Admin</a>'.format(url)
                x['url'] = url
                template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
                self.response.write(template.render(x))
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
