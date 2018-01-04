import os
from flask import Flask, request, redirect
import jinja2


template_dir = os.path.join(os.path.dirname(__file__),
    'templates')

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('signup-form.html')
    return template.render(user='', user_error='', password='', pass_error='', pass_val='', pass_val_error='', email='', email_error='')

def validate_email(email):
    dot = 0
    at = 0
    if len(email)<3 or len(email)>20:
        return False
    for i in email:
        if i == "@":
            at += 1
        if i == "." and at < 1:
            return False
        elif i == ".":
            dot += 1
    if at != 1 or dot != 1:
        return False
    else:
        return True

@app.route("/", methods = ['POST'])
def validate_form():
    user = request.form['username']
    password = request.form['password']
    pass_val = request.form['confpassword']
    email = request.form['mail']

    user_error=''
    pass_error=''
    pass_val_error=''
    email_error=''

    if user == "":
        user_error = "Username required"
    elif len(user)<3 or len(user) >20 or ' ' in user:
        user_error = "invalid Username"

    if password =="":
        pass_error = "password required"
    elif len(password)<3 or len(password)>20 or ' ' in password:
        pass_error = "invalid password"
        

    if pass_val == "" or pass_val != password:
        pass_val_error = "passwords do not match"

    if email != "" and not validate_email(email):
        email_error = "invalid email"

    if not user_error and not pass_error and not pass_val_error and not email_error:
        user = request.form['username']
        template = jinja_env.get_template('welcome.html')
        return template.render(user=user)
    else:
        template = jinja_env.get_template('signup-form.html')
        return template.render(user=user, user_error=user_error, password='', pass_error=pass_error, pass_val='', pass_val_error=pass_val_error, email=email, email_error=email_error)


app.run()