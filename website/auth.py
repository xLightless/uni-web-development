from flask import Blueprint, render_template, url_for, redirect, request, session
import hashlib

from website.database import Database

auth = Blueprint('auth', __name__)
database = Database(database="ht_database")

class Session(object):
    """ Public session data """        
        
    def has_key(self, key):
        """ Validates if session has a key """
        
        for iterkey in session.keys():
            if iterkey == key:
                return True
        return False
    
    def set_key(self, key, value):
        """ Sets a key in session """
        session[key] = value
            
    def get_key_value(self, key):
        return session.get(key)
    
class Authenticated(Session):
    """ Authenticated User Session """
    
    def __contains(self, string:str, has:str):
        """ Checks if an iterable object contains some element of string type """
        
        return True if any(i in has for i in string) else False
    
    def generate_password_hash(self, string):
        """ Generates a SHA1 password hash from string """
        
        special_chars = "~!@#$%^*&ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if len(string) >= 8:
            if self.__contains(string, special_chars) == True:
                password = bytes(string, 'utf-8')
                hash = hashlib.sha1(password)
                hash_password = hash.hexdigest()
                return hash_password
            
            return ValueError("Hash failed. The string '%s' did not contain any special chars. " % string)
        
        return ValueError("The string '%s' is too small for a password." % string)
        
    
    def authenticate_user(self, email, password):
        """ Authenticates user into session if account exists """

        contact_record = database.get_table_value_record('contacts', 'email_address', str(email))
        account_record = database.get_table_value_record('accounts', 'contact_id', str(contact_record[0]))
        password_in_account = str(account_record[3])
        username_in_account = str(account_record[2])
        
        email_in_table = database.is_value_in_table(table='contacts', column_name='email_address', value=str(email))
        if email_in_table == True:
            if self.generate_password_hash(password) == password_in_account:
                self.set_key('username', username_in_account)
                self.set_key('logged_in', True)
                
                return redirect(url_for('views.index'))
        
        login_error =  'Invalid email or password used.'
        print(login_error)
    
user_session = Session()
user_auth = Authenticated()

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Renders the login page """
    
    error = ""
    
    # If new session then create a login boolean
    if user_session.has_key('logged_in') == False:
        user_session.set_key('logged_in', False)
    
    try:
        if user_session.get_key_value('logged_in') == True:
            return redirect(url_for('auth.account'))
    except KeyError:
        error = "Session key '%s' not found. "
        print(error)
    
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
    
    user_auth.authenticate_user(email, password)
    return redirect(url_for('auth.login'))
    

# Account routing
@auth.route('/account/', methods=['GET','POST'])
def account():
    """ Manages account page authenticated users """
    
    if user_session.get_key_value('logged_in') == True:
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
        if (secret == csecret):
            if len(secret) >= 8:
                
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
                        str(user_auth.generate_password_hash(secret)),
                        'Normal'
                    )
                )
            
                return redirect(url_for('auth.login'))
        
        return redirect(url_for('auth.register'))
        # if not (str(session.get('password')) == str(session.get('confirmPassword'))):
        #     error = "Confirm password and password do not match!"
        #     print(error)
        #     return redirect(url_for('auth.register'))
        
    return redirect(url_for('auth.login'))

@auth.route('/account/logout/') 
def logout():
    for key in list(session.keys()):
        session.pop(key, None)
        session.clear()
    user_session.set_key('logged_in', False)
    return redirect(url_for('views.index'))


# @auth.route('/booking/')
# def booking():
#     if session['logged_in'] == True:
#         return redirect(url_for('views.booking'))
#     return redirect(url_for('auth.login'))