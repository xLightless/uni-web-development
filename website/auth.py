from flask import Blueprint, render_template, session, url_for, redirect, request
from datetime import timedelta

auth = Blueprint('auth', __name__)
# session.permanent = timedelta(minutes = 5)

@auth.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

# Account routing
@auth.route('/account/')
def account():
    return render_template('account.html')

@auth.route('/account/register')
def register():
    return render_template('register.html')

@auth.route('/account/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['password'] = request.form['password']
        print(username)
        return redirect(url_for('views.index'))
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        
    return render_template('login.html')
    
    
    
    
    
    

# @auth.route('/account/<arguments>', methods = ['POST', 'GET'])
# def account_post(arguments:str):
#     """ Handles account URL manipulation """
    
#     # This variable will be changed for an SQL database quiery
#     logged_in = True
    
#     # Tuple containing url points
#     account_args = (
#         "register",
#         "login",
#         "logout"
#     )
    
#     for args in account_args:
#         if args == arguments:
#             return render_template(f'{arguments}.html')
    
#     if request.method == 'POST':
#         username = request.form['password']
#         password = request.form['password']
#         return redirect(url_for('auth.success', name = username))
    
#     if request.method == 'GET':
#         username = request.args.get('username')
#         return redirect(url_for('auth.success', name = username))
        
    
    