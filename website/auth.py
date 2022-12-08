from flask import Blueprint, render_template, session, url_for, redirect, request

from website.database import Database

auth = Blueprint('auth', __name__)

# This file is for authentication purposes only

class AuthenticateUser(object):
    def __init__(
        self,
        email = None,
        username = None,
        password = None
    ) -> str:
        
        self.__email = (request.form.get("email") if email is None else email)
        self.__username = (request.form.get("username") if username is None else username)
        self.__password = (request.form.get("password") if password is None else password)
        
        self.__confirm_password = request.form.get("confirmPassword")
        
        first_name = request.form.get("legalFirstName")
        last_name = request.form.get("legalLastName")
        dob = request.form.get("dob")
        phone_number = request.form.get("phoneNumber")
        is_tos_checked = request.form.get("isTOSChecked")

def contains(string:str, has:str):
    """ Checks if an iterable object contains some element of string type """
    return True if any(i in has for i in string) else False

@auth.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Gets login data from the user form """
    
    # Used for checking the client side
    if request.method == 'POST':
        login_error = None
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        
        if (session['username']) and (len(str(session['password'])) >= 8) and (login_error is None):
            session['logged_in'] = True
            return redirect(url_for('views.index'))
        else:
            login_error = 'Invalid username or password used.'
            print(login_error)
            return render_template('login.html')
    
    # Used for when the server gets a response
    if request.method == 'GET':
        for key in session.keys():
            if key in session:
                if key == 'username':
                    print("username : " +session[key])
                    return redirect(url_for('views.account_page'))
    
    return render_template('login.html')

# Account routing
@auth.route('/account/', methods=['GET','POST'])
def account():
    username = session.get('username')
    if username is None:
        return redirect(url_for('auth.login'))
    elif username is not None:
        return redirect(url_for('views.account_page'))


@auth.route('/account/register/', methods=['GET', 'POST'])
def register():
    # register_error = None
    # special_chars = "!#$%^&*()_{-}.:=?@\/[]~"
    # if contains(str(session['password']), special_chars) == False:
    #     register_error = 'Invalid use of special characters'
    
    
        
    return render_template('register.html')

@auth.route('/account/logout/') 
def logout():
    for key in list(session.keys()):
        session.pop(key, None)
        session.clear()
    session['logged_in'] = False
    return redirect(url_for('views.index'))