from flask import Blueprint, render_template, session, url_for, redirect, request
from website import database

auth = Blueprint('auth', __name__)

# This file is for authentication purposes only

@auth.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Gets login data from the user form """
    
    # Used for checking the client side
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('views.index'))
    
    # Used for when the server gets a response
    if request.method == 'GET':
        for i in session.keys():
            if i in session:
                if i == 'username':
                    print("username : " +session[i])
                    return redirect(url_for('views.account_page'))
    
    return render_template('login.html')

# Account routing
@auth.route('/account/', methods=['POST', 'GET'])
def account():
    if session.get('username') == None:
        return redirect(url_for('auth.login'))
    elif session.get('username') != None:
        return redirect(url_for('views.account_page'))

@auth.route('/account/register/')
def register():
    return render_template('register.html')

@auth.route('/account/logout/') 
def logout():
    for key in list(session.keys()):
        session.pop(key, None)
        session.clear()
    return redirect(url_for('views.index'))