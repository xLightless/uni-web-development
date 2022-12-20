from flask import Blueprint, render_template, session, url_for, redirect, request

from website.database import Database

auth = Blueprint('auth', __name__)
database = Database(database="ht_database")

# This file is for authentication purposes only

class AuthenticateUser(object):
    def __init__(
        self,
        email = None,
        username = None,
        password = None
    ) -> str:
        pass
        
    def set_password_hash(self):

        # register_error = None
        # special_chars = "!#$%^&*()_{-}.:=?@\/[]~"
        # if contains(str(), special_chars) == False:
        #     register_error = 'Invalid use of special characters'
        #     print(register_error)
        pass

def contains(string:str, has:str):
    """ Checks if an iterable object contains some element of string type """
    return True if any(i in has for i in string) else False

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Renders the login page """
    
    if session['logged_in'] == True:
        return redirect(url_for('auth.account'))
    
    if request.method == 'POST':
        login_input_email = request.form['loginEmail']
        login_input_password = request.form['password']
        
        return redirect(
            url_for(
                'auth.form_login',
                email=login_input_email,
                password=login_input_password
            )
        )

    return render_template('login.html')

@auth.route('/login/<email>/<password>/')
def form_login(email, password):
    """ Login form function """
    
    login_error = None
    # Fixes some string issues when returning values
    email_str = "".join((email)).replace(' ', '')
    password_str = "".join((password)).replace(' ', '')
    
    # Check if form input email and password exist in relative tables
    email_in_table = database.is_value_in_table(table='contacts', column_name='email_address', value=str(email_str))
    password_in_table = database.is_value_in_table(table='accounts', column_name='password', value=str(password_str))
    
    if (email_in_table == True) and (password_in_table == True):
        session['logged_in'] = True
        session['username'] = database.get_primary_key_record('accounts', 25000)[2]
        return redirect(url_for('views.index'))
    else:
        login_error = 'Invalid username or password used.'
        print(login_error)
        return redirect(url_for('auth.login'))

# Account routing
@auth.route('/account/', methods=['GET','POST'])
def account():
    """ Manages account page authenticated users """
    
    if session['logged_in'] == True:
        return redirect(url_for('views.account_page'))
    return redirect(url_for('auth.login'))

@auth.route('/account/register/', methods=['POST', 'GET'])
def register():
    """ Register page """
    
    if request.method == 'POST':
        email_ = request.form['email']
        username = request.form['username']
        password = request.form['password']
        check_password = request.form['confirmPassword']
        first_name = request.form['legalFirstName']
        last_name = request.form['legalLastName']
        date_of_birth = request.form['dob']
        telephone = request.form['phoneNumber']
        
        session['password'] = password
        session['confirmPassword'] = check_password
        
        return redirect(url_for(
            'auth.form_register',
            email=email_,
            name=username,
            secret=password,
            csecret=check_password,
            fname=first_name,
            lname=last_name,
            dob=date_of_birth,
            phonenumber=telephone
            )
        )
    else:
        return render_template('register.html')

@auth.route('/account/register/<email>/<name>/<secret>/<csecret>/<fname>/<lname>/<dob>/<phonenumber>/')
def form_register(email, name, secret, csecret, fname, lname, dob, phonenumber):
    """ Registers the user using entered form data from register page """
    
    error = None
    email_in_table = database.is_value_in_table(table='contacts', column_name='email_address', value=str(email))
    
    if email_in_table != True:
        
        # If account not made before then check form data conditions match and create an account
        if (str(session.get('password')) == str(session.get('confirmPassword'))):
        
            # Set record data for the registering user
            customers_primary_key = database.count_table_rows('customers')+10000
            contacts_primary_key = database.count_table_rows('contacts')+20000
            accounts_primary_key = database.count_table_rows('accounts')+25000
            
            
            database.set_table_record(
                table='customers', 
                pk_id=customers_primary_key, 
                values=(
                    str(fname),
                    str(lname),
                    str(dob)
                )
            )

            database.set_table_record(
                table='contacts', 
                pk_id=contacts_primary_key, 
                values=(
                    str(customers_primary_key),
                    str(phonenumber),
                    str(email)
                )
            )

            database.set_table_record(
                table='accounts', 
                pk_id=accounts_primary_key, 
                values=(
                    str(contacts_primary_key),
                    str(name),
                    str(secret),
                    'Normal'
                )
            )
        
            return redirect(url_for('auth.login'))
        
        if not (str(session.get('password')) == str(session.get('confirmPassword'))):
            error = "Confirm password and password do not match!"
            print(error)
            return redirect(url_for('auth.register'))
        
    return render_template('bad_login.html')


@auth.route('/account/logout/') 
def logout():
    for key in list(session.keys()):
        session.pop(key, None)
        session.clear()
    session['logged_in'] = False
    return redirect(url_for('views.index'))


# @auth.route('/booking/')
# def booking():
#     if session['logged_in'] == True:
#         return redirect(url_for('views.booking'))
#     return redirect(url_for('auth.login'))