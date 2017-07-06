from flask import Flask, request, redirect
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route('/', methods=['POST'])
def verify():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']
    usererror = ''
    passworderror = ''
    verifyerror = ''
    emailerror = ''

    #validate username
    if username == '':
        usererror = "That's not a valid username"

    #validate password
    if password == '':
        passworderror = "That's not a valid password"
    elif len(password) < 3:
        passworderror = "That's not a valid password"
    elif len(password) > 20:
        passworderror = "That's not a valid password"
    elif " " in password:
        passworderror = "That's not a valid password"

    #validate verification password
    if password == '':
        verifyerror = "Passwords don't match"
    elif password != verify:
        verifyerror = "Passwords don't match"

    #validate email
    if len(email) == 0:
        emailerror =''
    elif len(email) < 3:
        emailerror = "That's not a valid email"
    elif len(email) > 20:
        emailerror = "That's not a valid email"
    elif " " in email:
       emailerror = "That's not a valid email"
    elif "@" not in email:
        emailerror = "That's not a valid email"
    elif "." not in email:
        emailerror = "That's not a valid email"

    if not usererror and not passworderror and not verifyerror and not emailerror:
        return redirect('/welcome?username={0}'.format(username))
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username=username,email=email,usererror=usererror,
            passworderror=passworderror,
            verifyerror=verifyerror,
            emailerror=emailerror)

@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

app.run()
