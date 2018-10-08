from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def display():
    template = jinja_env.get_template('signup.html')
    return template.render(user_Name='',password='',vPassword='',email='')

@app.route("/", methods=['POST'])
def validate():
    user_Name = request.form['user_Name']
    password  = request.form['Password']
    vPassword = request.form['VerifyPassword']
    email     = request.form['Email']
    
    userNameError = ''
    passwordError = ''
    emailError = ''

    numOfSym = ''
    numOfDot = ''
#username varification
    if user_Name == '':
        userNameError = "username was left blank"
        user_Name = ''
    elif len(user_Name) < 3:
        userNameError = "username is to short"
        user_Name = ''
    elif len(user_Name) > 20:
        userNameError = "username is to big"
        user_Name = ''
    else:
        user_Name = str(user_Name)
        for let in user_Name:
            if let == " ":
                userNameError = "no spaces in username"
                user_Name = ""
#Password varification
    if password != vPassword:
        passwordError = "The passwords do not match"
        password = ''
        vPassword = ''
    elif password == '':
        passwordError = "password was left blank"
        password = ''
        vPassword = ''
    else:
        if len(password)<3 or len(password) > 20:
            passwordError = "password is to short or long"
            password = ''
            vPassword = ''
#Email varification
    if len(email)>0:
        print(len(email))
        for let in email:
            if let == '@':
                numOfSym += let
            elif let == ' ':
                emailError = "no spaces in email"
            elif let == '.':
                numOfDot += let

        if len(numOfDot) > 1 or len(numOfDot) < 1:
            emailError = "Too many '.' symbols or you need one"
            email = '' 

        elif len(numOfSym) > 1 or len(numOfSym) < 1:
            emailError = "Too many '@' symbols or you need one"
            email = ''

        elif len(email) < 3 or len(email) > 20:
            emailError = "The email is too short or too long"
            email = ''
        

#returning information for display
    if not userNameError and not passwordError and not emailError:
        return redirect('/UserName?user_Name={0}'.format(user_Name))

    else:

        template = jinja_env.get_template('signup.html')
    
        return template.render(user_Name=user_Name, userNameError=userNameError, passwordError=passwordError, emailError=emailError, email=email)



@app.route("/UserName")
def userName():
    user_Name = request.args.get('user_Name')
    template = jinja_env.get_template('welcome.html')
    return template.render(user_Name=user_Name)
app.run()