from flask import Blueprint, render_template, url_for, redirect, request, session, send_file
import hashlib
import time
import mysql.connector
from datetime import datetime

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
        # user_auth.set_key('payment_successful', False)
        
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
    
    # if user_auth.get_key_value('payment_successful') == True: return redirect(url_for('auth.account'))
    
    payment_collection = {} # Temporarily store extra info about the payment that wouldnt be in booking or preprocessor
    
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

        booking_data = preprocessor.get_dict()
        booking = Booking(booking_data)
        from datetime import datetime
        payment_date = datetime.now().date()
        
        # Get the GBP price without string prefix
        price = str(preprocessor.get_one('total_cost')) # May return None if user goes back to an expired page
        prefix_price = price[0] # Price string with exchange type
        try:
            
            # Reset values back to gbp before putting them into the database so it does not look like we are overcharging the user.
            if prefix_price == '£':
                price = float(price[1:])/1
                
            elif prefix_price == '$':
                price = float(price[1:])/1.25
                
            elif prefix_price == '€':
                price = float(price[1:])/1.13
                
            
        except ValueError as e:
            print(e)
            print('Payment unsuccessful. Could not convert the price.')
            # user_auth.set_key('payment_successful', False)
            return redirect(url_for('views.index'))
        
        discount = str(booking_data.get('discount'))
        
        loc_from = str(preprocessor.get_dict().get('location_from'))
        loc_to = str(preprocessor.get_dict().get('location_to'))    

        # Add payment_wall information to dict
        payment_collection['payment_id'] = payment_id
        payment_collection['payment_date'] = payment_date
        # payment_collection['price'] = price
        
        # print(preprocessor.get_dict())
        payment_data = Booking(preprocessor.get_dict())

        # Obtain the journey key from database table
        journey_table = database.get_table_records_of_value('journey', 'departure_location', loc_from)
        # journey_id:int = None
        for row in range(len(journey_table)):
            jloc1 = journey_table[row][1]
            jloc2 = journey_table[row][3]
            
            print(jloc1, loc_from, jloc2, loc_to)
            if (jloc1 == loc_from) and (jloc2 == loc_to):
                journey_id = int(journey_table[row][0]) # Convert to INT since the Foreign key is integer
                try:
                    database.insert_table_null_record(
                        'booking_payment',
                        payment_id,
                        values=(
                            str(account_id), # account_id
                            str(price), # price
                            str(discount), # discount_percentage
                            'PayPal', # Payment Type
                            str(payment_date), # The purchase date of the ticket but not the date the purchase is finalised due to cancellation
                            'Approved', # Purchase Status
                            str(journey_id)
                        ),
                        null_column = 8 # (NULL) No cancellation date created yet so the value has to be null
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
                    # user_auth.set_key('payment_successful', True)
                    
                except mysql.connector.errors.DatabaseError as e:
                    print(e)
                    return redirect(url_for('auth.account'))
    

        # Get payment data after confirming booking
        payment_data = {
            'payment_id' : payment_collection['payment_id'],
            'payment_date' : payment_collection['payment_date'],
            'price'    : preprocessor.get_one('total_cost')
        }
        
        # Place the data into preprocessor to create a dict object for downloading receipts
        preprocessor.set_dict(payment_data)
    
    return render_template('payment_wall.html', payment_id = payment_collection['payment_id'], payment_date = payment_collection['payment_date'], price = preprocessor.get_one('total_cost'))


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
            
            cancellation_date = str(datetime.now().date()).replace('-','/')
            
            if (account_id_1 == account_id_2):
                database.update_table_record_value('booking_payment', 'purchase_status', 'Cancelled', 'payment_id', payment_id)
                database.update_table_record_value('booking_payment', 'cancellation_date', cancellation_date, 'payment_id', payment_id)
                # delete_payment_records(payment_id=payment_id, account_id=account_id_1)
                print('Deleted records from database, refreshing web page.')
                
                return redirect(url_for('views.account_page'))
            else:
                url_build = url_for('views.legal')
                char = url_build[0]
                print('Please do not try and attempt to malipulate our website software. You will be going against the Terms and Conditions.')
                print(str(request.url_root) + "".join(url_build.replace(char, '')))
                return redirect(url_for('views.account_page'))
            # If not then remove booking from system
        
        
        
        
    # return redirect(url_for('auth.logout'))
    return redirect(url_for('views.account_page'))

@auth.route('/booking/payment/download/', methods=['POST'])
def payment_download():
    """ Generate a pdf/txt based on a html document about the payment created """
    
    file_path = auth.root_path + '\\generator\\receipt.txt'
    if request.method == 'POST':
        payment_data = preprocessor.get_dict()
        with open(file_path, "w") as file:
            file.write(f"Horizon Travels -> Payment Receipt. \n\n- Payment Price: {payment_data.get('price')}. \n- Payment Date: {payment_data.get('payment_date')}. \n- Payment ID: {payment_data.get('payment_id')} \n\n Thank you for travelling with us. We wish you a safe journey!")
    
    return send_file(file_path, as_attachment = True)

@auth.route('/account/admin/')
def admin_portal():
    
    total_sales:float = 0
    
    booking_payment_price = database.get_table_column('booking_payment', 'price')
    created_bookings = database.count_table_rows('booking')
    
    contact_id = database.get_table_value_record('contacts', 'email_address', str(session.get('email')))[0]
    user_preferred_currency = database.get_table_value_record('accounts', 'contact_id', str(contact_id))[5] # change to 4 if you remove username
    total_refunded = database.count_permissible_rows('booking_payment', 'purchase_status', 'Cancelled')
    
    # Get total sales from price
    for price in booking_payment_price[1]:
        total_sales = float(total_sales) + float(price[0])
    
    # If not dollars or euros then it must be GBP (pounds)
    if (user_preferred_currency == 'Dollars') or (user_preferred_currency == 'Euros'):
        total_sales = stats.convert_price(total_sales, str(user_preferred_currency))
    else:
        total_sales = stats.convert_price(total_sales, 'Pounds')
        
     
    # Journey table data
    journey_data = {}
    
    jdata = database.get_table('journey')
    
    for row in range(len(jdata)): 
        journey_data[row] = {
            'journey_id'        : jdata[row][0],
            'departure'         : jdata[row][1],
            'deparature_time'   : jdata[row][2],
            'return'            :  jdata[row][3],
            'return_time'       : jdata[row][4]
        }
        
    ### Add data to graphs
    
    # Get only data that is not cancelled to display true Net value
    data = database.get_table_records_of_value('booking_payment', 'purchase_status', 'Approved')
    
    months_of_year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    total_price = 0
    month = ''
    monthly_sales = {}
    
    for row in range(len(data)):
        # print(months_of_year[row])
        col_date = str(data[row][5]) # Use payment date as the month date. Change to booking-date for testing purposes.
        col_price = data[row][2] # Row Price data
        
        strtime = datetime.strptime(col_date, "%Y-%m-%d")
        numerical_month = strtime.month

        for month in months_of_year:
            if month == months_of_year[numerical_month]:
                total_price = total_price + col_price
                month = months_of_year[numerical_month]
        
                # Add total_price to monthly sales
                # monthly_sales[month] = total_price
                monthly_sales[month] = stats.convert_price(float(total_price), str(user_preferred_currency))[1:] # Get the converted sale price - prefix char
                
                # Add 100 percent refunds to monthly sales
                
                
    
    return render_template(
        'admin_portal.html',
        total_sales = total_sales,
        created_bookings = created_bookings,
        total_refunded = total_refunded,
        journey_data = journey_data,
        monthly_sales = monthly_sales
    )

@auth.route('/account/admin/edit-journeys/', methods=['POST', 'GET'])
def admin_portal_journeys():
    """ Handle post request for forms in admin portal """
    
    if request.method == 'POST':
        
        # Check if the user clicked add, update or remove journey buttons
        response = request.form.to_dict()
        departure = str(response['departure-location']).capitalize()
        returning = str(response['return-location']).capitalize()
        departure_response = str(response['departure-time'])
        returning_response = str(response['return-time'])
        
        # Check if departure_location and return_location not/are in the existing table
        journey_table = database.get_table_records_of_value('journey', 'departure_location', str(response['departure-location']))
        new_journey_id = database.count_table_rows('journey')+1

        # print(request.form.to_dict().keys())
        
        if (departure.isalpha() == True) and (returning.isalpha() == True):
            for row in range(len(journey_table)):
                
                # for col in journey_table[row]:
                journey_id = journey_table[row][0]
                departure_loc = journey_table[row][1]
                departure_time = journey_table[row][2]
                returning_loc = journey_table[row][3]
                returning_time = journey_table[row][4]
                
                
                if 'add-journey' in request.form.to_dict().keys():
                    database.set_table_record(
                        'journey',
                        new_journey_id,
                        values=(
                            str(departure),
                            str(departure_response),
                            str(returning),
                            str(returning_response)
                        ))
                    
                    print(f"Added new route to database:\n - Going From: {departure} at {departure_response},\n - Going To: {returning} at {returning_response}.")
                    break
                    
                elif 'update-journey' in request.form.to_dict().keys():
                    if (departure == departure_loc) and (returning == returning_loc):
                        
                        database.update_table_record_values(
                            'journey',
                            column_names = (
                                'departure_location',
                                'departure_time',
                                'return_location',
                                'return_time'
                            ),
                            values = (
                                str(departure_loc),
                                str(departure_response),
                                str(returning_loc),
                                str(returning_response)
                            ),
                            pk_column_name = str('journey_id'),
                            pk_id = int(journey_id)
                        )
                        print(f"Updated a route in the database:\n - Going From: {departure_loc} at {departure_response},\n - Going To:   {returning_loc} at {returning_response}.")
                
                elif 'remove-journey' in response:
                    if (departure == departure_loc) and (returning == returning_loc):
                        database.del_table_record('journey', 'journey_id', int(journey_id))
                        
                        print(f"Deleted route in the database:\n - Going From: {departure_loc} at {departure_response},\n - Going To:   {returning_loc} at {returning_response}.")
                        # I could add time based deletion but its not a necessary requirement.
    
    return redirect(url_for('auth.admin_portal'))


@auth.route('/account/admin/edit-accounts/')
def admin_portal_accounts():
    return redirect(url_for('auth.admin_portal'))


@auth.route('/account/admin/permissions/')
def admin_permissions():
    return '<h1> admin perms</h1>'