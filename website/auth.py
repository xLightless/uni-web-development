from flask import Blueprint, render_template, url_for, redirect, request, session, send_file
import hashlib
import time
import mysql.connector

from website.database import Database
from website.booking_logic import Booking, preprocessor, Statistics


auth = Blueprint('auth', __name__)
database = Database(database="ht_database", user="root", password="Password1")
stats = Statistics()

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
        
        else:
            return ValueError("The string '%s' is too small for a password." % string)
        
    
    def authenticate_user(self, email, password):
        """ Authenticates user into session if account exists """

        try:
            contact_record = database.get_table_value_record('contacts', 'email_address', str(email))
            account_record = database.get_table_value_record('accounts', 'contact_id', str(contact_record[0]))
            password_in_account = str(account_record[3])
            username_in_account = str(account_record[2])
            user_type = str(account_record[4])
            
            email_in_table = database.is_value_in_table(table='contacts', column_name='email_address', value=str(email))
            if email_in_table == True:
                if self.generate_password_hash(password) == password_in_account:
                    self.set_key('logged_in', True)
                    self.set_key('email', email)
                    self.set_key('username', username_in_account)
                    
                    # Identify the type of user
                    if user_type == 'Admin':
                        self.set_key('Admin', True)
                    if user_type == 'Standard':
                        self.set_key('Standard', True)
                    
                    # print(session.keys())
                    
                    return redirect(url_for('views.index'))
        except IndexError:
            login_error =  'Invalid email or password used.'
            print(login_error)
    
user_session = Session()
user_auth = Authenticated()

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """ Renders the login page """
    
    error = ""
    # print(session.keys())
    
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
    # print("AUTH account page")
    
    if user_session.get_key_value('logged_in') == True:
        user_auth.set_key('payment_successful', False)
        
        # if request.method == 'POST':
        #     username_ = request.form['username']
        #     fname_ = request.form['fname']
        #     lname_ = request.form['lname']
        #     telephone_ = request.form['telephone']
        #     email_ = request.form['email']
            
        #     return redirect(url_for(
        #         'auth.update_account',
        #         username = username_,
        #         fname = fname_,
        #         lname = lname_,
        #         telephone = telephone_,
        #         email = email_
        #     ))
        
        return redirect(url_for('views.account_page'))
    return redirect(url_for('auth.login'))

# @auth.route('/account/<username>/<fname>/<lname>/<telephone>/<email>/')
# def update_account(username, fname, lname, telephone, email):
#     # print(username, fname, lname, telephone, email)
    
#     try:
#         contacts = database.get_table_value_record('contacts', 'email_address', str(session['email']))
#         contact_id = contacts[0]
#         customer_id = contacts[1]
#         customer = database.get_table_value_record('customers', 'customer_id', str(customer_id))
#         account = database.get_table_value_record('accounts', 'contact_id', str(contact_id))
#         account_id = account[0]
        
#         # Account table
#         database.update_table_record('accounts', 'username', username, 'account_id', account_id)
        
#         # Contacts table
#         database.update_table_record('contacts', 'telephone', telephone, 'contact_id', contact_id)
#         database.update_table_record('contacts', 'email_address', email, 'contact_id', contact_id)
        
#         # Customers table
#         database.update_table_record('customers', 'first_name', fname, 'customer_id', customer_id)
#         database.update_table_record('customers', 'last_name', lname, 'customer_id', customer_id)
#     except TypeError:
#         pass
#     return redirect(url_for('auth.logout'))

@auth.route('/account/edit-profile/', methods=['POST', 'GET'])
def update_user_data():
    
    if request.method == 'POST':
        form = request.form.to_dict()
        if session['logged_in'] == True:
            email_address = session.get('email')
            first_name = form.get('first_name')
            last_name = form.get('last_name')
            phone_number = form.get('phone_number')
            currency_type = form.get('currency_type')
            new_password = form.get('new_password')
            confirm_new_password = form.get('confirm_new_password')
            current_password = form.get('current_password')
            
            # Obtain the primary keys from database tables
            contacts = database.get_table_value_record('contacts', 'email_address', str(email_address))
            contact_id = contacts[0]
            accounts = database.get_table_value_record('accounts', 'contact_id', str(contact_id))
            account_id = accounts[0]
            account_password = accounts[3]
            customer_id = contacts[1]
            customers = database.get_table_value_record('customers', 'customer_id', str(customer_id))
            current_first_name = customers[1]

            # Check if passwords match before updating info
            if user_auth.generate_password_hash(str(current_password)) == str(account_password):               
                try:
                    # if ((phone_number == 'None') or (phone_number == '') or (phone_number is None)):
                    #     print(first_name, last_name, phone_number)
                    if ((first_name or last_name or phone_number) != ('' or None or 'None')):
                        
                        print('Updating account information')
                        
                        # Update data in records
                        database.update_table_record_value(
                            'customers',
                            'first_name',
                            str(first_name),
                            'customer_id',
                            str(customer_id)
                        )
                        
                        database.update_table_record_value(
                            'customers',
                            'last_name',
                            str(last_name),
                            'customer_id',
                            str(customer_id)
                        )
                        
                        database.update_table_record_value(
                            'contacts',
                            'telephone',
                            str(int(str(phone_number))), # Convert phone number to an int to check if it is a real number else exception
                            'customer_id',
                            str(customer_id)
                        )
                        
                        database.update_table_record_value(
                            'accounts',
                            'currency_type',
                            str(currency_type),
                            'account_id',
                            str(account_id)
                        )

                        if (str(new_password) != '') and (str(confirm_new_password) != ''):
                            if (str(new_password) == str(confirm_new_password)):
                                print(new_password, confirm_new_password)
                                database.update_table_record_value(
                                    'accounts',
                                    'password',
                                    str(user_auth.generate_password_hash(new_password)),
                                    'account_id',
                                    str(account_id)
                                )
                        
                    else:
                        raise ValueError
                    
                except ValueError or TypeError:
                    return redirect(url_for('auth.account'))
            else:
                print('An entered value did not match.')
            
    return redirect(url_for('auth.account'))

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
                        'Standard',
                        'Pounds'
                    )
                )
            
                return redirect(url_for('auth.login'))
        
        return redirect(url_for('auth.register'))
        
    return redirect(url_for('auth.login'))

@auth.route('/account/logout/') 
def logout():
    for key in list(session.keys()):
        session.pop(key, None)
        session.clear()
    user_session.set_key('logged_in', False)
    return redirect(url_for('views.index'))
 
@auth.route('/booking/payment/', methods=['GET', 'POST'])
def payment():
    """ Handles payments from booking page when the user clicks 'PAYPAL' button """
    # print(preprocessor.get_dict())
    
    if user_auth.get_key_value('payment_successful') == True: return redirect(url_for('auth.account'))
    
    payment_collection = {}
    
    # Although an existing dictionary of the data we want is available, it is being used before the customer clicks pay.
    if request.method == 'POST':
        
        # Check if the user has already been on the active page to prevent overload
        # if 'payment_success' in session:
        #     session.pop('payment_success')
        #     return redirect(url_for('auth.account'))
        
        # Get account id through contacts
        contact_id = database.get_table_value_record('contacts', 'email_address', str(session['email']))[0]
        accounts = database.get_table_value_record('accounts', 'contact_id', str(contact_id))
        account_id = accounts[0]
        payment_id = database.count_table_rows('booking_payment')+12387
        # payment_id = payment_row_count + 12387 # Some random constant to scramble PK ID
        
        # print(request.form.to_dict())
        
        booking_data = preprocessor.get_dict()
        booking = Booking(booking_data)
        from datetime import datetime
        payment_date = datetime.now().date()
        
        # Get the GBP price without string prefix
        price = str(preprocessor.get_one('total_cost')) # May return None if user goes back to an expired page
        try:
            price = float(price[1:])
            
        except ValueError:
            print(('Payment unsuccessful. Could not convert the price.'))
            user_auth.set_key('payment_successful', False)
            return redirect(url_for('views.index'))
        
        discount = str(booking_data.get('discount'))
        
        loc_from = str(preprocessor.get_dict().get('location_from'))
        loc_to = str(preprocessor.get_dict().get('location_to'))    

        # Add payment_wall information to dict
        payment_collection['payment_id'] = payment_id
        payment_collection['payment_date'] = payment_date
        # payment_collection['price'] = price
        
        
        
        
        
        payment_data = Booking(preprocessor.get_dict())
        payment_collection['price'] = payment_data.get_price_string(preprocessor.get_one('currency_type'))
        
        # print(payment_collection['price'])




        # Obtain the journey key from database table
        journey_table = database.get_table_records_of_value('journey', 'departure', loc_from)
        journey_id:int = None
        
        for row in range(len(journey_table)):
            jloc1 = journey_table[row][1]
            jloc2 = journey_table[row][3]
            
            if (jloc1 == loc_from) and (jloc2 == loc_to):
                journey_id = int(journey_table[row][0]) # Convert to INT since the Foreign key is integer
            break
        
        try:
            database.set_table_record(
                'booking_payment',
                payment_id,
                values=(
                    str(account_id), # account_id
                    str(price), # price
                    str(discount), # discount_percentage
                    'PayPal', # payment_method ### May need to update this later to include debit card?
                    str(payment_date), # The purchase date of the ticket but not the date the purchase is finalised due to cancellation
                    # str(['Approved' if str(booking_data.get('date_from')) == str(payment_date) else 'Pending']) # If purchase day is the same as day of travel then pay is approved else pending
                    'Approved',
                    str(journey_id)
                    
                )
            )
            
            booking_record = database.get_table_value_record('booking_payment', 'payment_id', str(payment_id))
            booking_id = payment_id + 34817 # (12392, 25000, Decimal('600.00'), '0', 'PayPal', datetime.date(2023, 4, 6), 'Approved')
            
            database.set_table_record(
                'booking',
                booking_id,
                values=(
                    str(payment_id),
                    str(booking_data.get('seat_class_type')), # Business/Eco
                    str(booking_data.get('passengers_amount')), # No. People
                    str(booking_data.get('date_from')), # Leaving Time
                    str(booking_data.get('date_to')), # Returning if one
                    str(booking_data.get('trip_type')) # Commute type e.g. Return or Oneway
                )
            )
            
            # session['payment_success'] = True
            user_auth.set_key('payment_successful', True)
            
        except mysql.connector.errors.DatabaseError:
            # print(e)
            return redirect(url_for('auth.account'))
        
    return render_template('payment_wall.html', payment_id = payment_collection['payment_id'], payment_date = payment_collection['payment_date'], price = payment_collection['price'])


def delete_payment_records(payment_id, account_id):
    database.del_table_record('booking', 'payment_id', payment_id)
    time.sleep(3)
    database.del_table_record('booking_payment', 'account_id', account_id)

@auth.route('/cancel-booking/', methods=['POST', 'GET'])
def cancel_booking():
    """ My bookings dashboard cancellation buttons """
    
    if request.method == 'POST':
        
        if session['logged_in'] == True:
            try:
                form = request.form.to_dict()
                payment_id = form.get('payment_id')
                
            except ValueError:
                print('The primary key %s was not found in the database.' % (payment_id))
                return redirect(url_for('views.account_page'))
            
            # Check if the user is making modifications to the html before post
            account_id_1 = database.get_table_value_record('booking_payment', 'payment_id', payment_id)[1]
            contact_id = database.get_table_value_record('contacts', 'email_address', str(session.get('email')))[0]
            account_id_2 = database.get_table_value_record('accounts', 'contact_id', str(contact_id))[0]
            if (account_id_1 == account_id_2):
                database.update_table_record_value('booking_payment', 'purchase_status', 'Cancelled', 'payment_id', payment_id)
                # delete_payment_records(payment_id=payment_id, account_id=account_id_1)
                print('Deleted records from database, refreshing web page.')
                
                return redirect(url_for('views.account_page'))
            else:
                url_build = url_for('views.legal')
                char = url_build[0]
                print('Please do not try and attempt to malipulate our website software. You will be going against Terms and Conditions.')
                print(str(request.url_root) + "".join(url_build.replace(char, '')))
                return redirect(url_for('views.account_page'))
            # If not then remove booking from system
        
        
        
        
    # return redirect(url_for('auth.logout'))
    return redirect(url_for('views.account_page'))

@auth.route('/booking/payment/download/', methods=['POST'])
def payment_download():
    """ Generate a pdf/txt based on a html document about the payment created """
    
    if request.method == 'POST':
        if 'download_payment' in request.form['download_payment']:
            pass
    
    
    file_path = auth.root_path + '\\generator\\receipt.txt'
    
    return send_file(file_path, as_attachment = True)

@auth.route('/account/admin/')
def admin_portal():
    
    data = {}
    total_sales:float = 0
    
    booking_payment_price = database.get_table_column('booking_payment', 'price')
    created_bookings = database.count_table_rows('booking')
    
    contact_id = database.get_table_value_record('contacts', 'email_address', str(session.get('email')))[0]
    user_preferred_currency = database.get_table_value_record('accounts', 'contact_id', str(contact_id))[5] # change to 4 if you remove username
    total_refunded = database.count_permissible_rows('booking_payment', 'purchase_status', 'Refunded')
    
    # Get total sales from price
    for price in booking_payment_price[1]:
        total_sales = float(total_sales) + float(price[0])
        
    total_sales = stats.convert_price(total_sales, str(user_preferred_currency))
    
    return render_template('admin_portal.html', total_sales = total_sales, created_bookings = created_bookings, total_refunded = total_refunded)

@auth.route('/account/admin/permissions/')
def admin_permissions():
    return '<h1> admin perms</h1>'