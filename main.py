from flask import Flask, request
import cgi
import os 
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

def validate_username(username):
    if len(username) < 3 or len(username) > 20 or " " in username:
        username_err = "That's not a valid username"
    else:
        username_err = ""
    return username_err

def validate_password(password):
    if len(password) < 3 or len(password) > 20 or " " in password:
        pw_err = "That's not a valid password"
    else:
        pw_err = ""
    return pw_err

def validate_pw_match(password, verify):
    if password != verify or len(verify) == 0:
        password_err = "Passwords don't match"
    else:
        password_err = ""    
    return password_err

def validate_email(email):
    if len(email) > 0:
        if email.count("@") != 1 or email.count(".") != 1 or len(email) < 3 or len(email) > 20 :
            email_err = "That is not a valid e-mail"
        else:
            email_err = ""
    else:
        email_err = ""
    return email_err


@app.route("/", methods=['POST'])
def validate():
    usern = request.form['user']
    pw = request.form['password']
    ver_pw = request.form['verify']
    em = request.form['email']

    usern_err = validate_username(usern)
    p_err = validate_password(pw)
    pw_err = validate_pw_match(pw, ver_pw)
    em_err = validate_email(em)   

    if usern_err == "" and p_err == "" and pw_err == "" and em_err == "":
        template = jinja_env.get_template('success.html')
        return template.render(username=usern)

    template = jinja_env.get_template('user-signup.html')
    return template.render(username_err=usern_err, verify_err=p_err, password_err=pw_err, email_err=em_err,
    username=usern, email=em)


@app.route("/")
def index():

    template = jinja_env.get_template('user-signup.html')
    return template.render()

app.run()