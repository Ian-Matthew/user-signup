#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import validation

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
        label {
            display: inline-block;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>
        User Signup
    </h1>
"""

page_footer = """
</body>
</html>
"""

class SignUp(webapp2.RequestHandler):


    def generate_form(self,username="", username_error="",password_error="",verify_error="",email_adress="",email_error=""):
        form = """
        <form action = "/" method ="post">
            <label> Username
                <input type ="text" name = "username" value="{user_name}"/>
                {error1}
            </label>
            <br>
            <label> Password
                <input type = "password" name = "password" />
            </label>
            {error2}
            <br>
            <label> Verify Password
                <input type = "password" name = "verify_password" />
            </label>
            {error3}
            <br>
            <label> Email
                <input type = "text" name = "email" value="{email}"
            </label>
            {error4}
            <input type="submit" value="Sign up!"/>
        </form>
        """
        return form.format(user_name=username,error1=username_error,error2=password_error,error3=verify_error,email=email_adress, error4=email_error)


    def get(self):
        content = page_header + self.generate_form() + page_footer
        self.response.write(content)

    def post(self):

        error = False

        # Grab user's input and store in variables
        username = self.request.get("username")
        password = self.request.get("password")
        verified_password = self.request.get("verify_password")
        email_adress = self.request.get("email")

        # Validate input and generate error messages if needed
        if not validation.valid_username(username):
            username_error = '''<span class="error">That is not a valid username!</span>'''
            error = True
        else:
            username_error = ""


        if not validation.valid_password(password):
            password_error= '''<span class="error">That is not a valid password!</span>'''
            error = True
        else:
            password_error = ""


        if verified_password != password:
            verify_error= '''<span class="error">Your passwords didn't match</span>'''
            error = True
        else:
            verify_error = ""


        if not validation.valid_email(email_adress):
            email_error = '''<span class="error"> That is not a valid email!</span>'''
        else:
            email_error = ""


        # If there are Errors, generate form and notify the user of errors
        if error:
            content = page_header + self.generate_form(username,username_error,password_error,verify_error,email_adress,email_error) + page_footer
            self.response.write(content)
        else:
            self.redirect("/Welcome?username=" + username)


class WelcomePage(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        welcome_message = '''<h1>Welcome, ''' + username + '''!</h1>'''
        self.response.write(welcome_message)


app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/Welcome', WelcomePage)
], debug=True)
