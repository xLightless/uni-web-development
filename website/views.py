from flask import Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime

from website import sitemap
from website.database import Database
from website.booking_logic import Booking, preprocessor

views = Blueprint('views', __name__)
database = Database(database="ht_database", user="root", password="Password1")

# booking_data = {} # used to store search_results data from a route

@views.route('/')
def index():
    """ Renders the index template and its search filter options """
    
    search_items = database.get_table_column('locations', 'location')[1]
    search_filter_items = []
    for item in search_items:
        search_item = str(item).replace('(', '').replace(')', '').replace(',','').replace("'", '')
        search_filter_items.append(search_item)
    
    return render_template(
        'index.html',
        search_items = search_filter_items
    )

@views.route('/', methods=['POST', 'GET'])
def form_index_search():
    """ Gets input queries from index booking form to use for other functionality """
    
    if request.method == 'POST':
    
        radio_return        = request.form.get('params-traveller-return'),
        radio_oneway        = request.form.get('params-traveller-oneway'),
        location_from       = request.form.get('input-box-from'),
        location_to         = request.form.get('input-box-to'),
        passengers_amount   = request.form.get('passengers-amount'),
        seat_class_type     = request.form.get('seat-class-type'),
        date_from           = request.form.get('swing-from-datepicker'),
        date_to             = request.form.get('swing-to-datepicker')
        print("SEARCH POST TEST")
        
        return_trip = str(radio_return).replace(',','').replace('(','').replace(')','').replace("'", '')
        oneway_trip = str(radio_oneway).replace(',','').replace('(','').replace(')','').replace("'", '')            
        
        global search_results
        search_results = {}
        if location_from is not None: search_results['location_from'] = location_from
        if location_to is not None: search_results['location_to'] = location_to
        if passengers_amount is not None: search_results['passengers_amount'] = passengers_amount
        if seat_class_type is not None: search_results['seat_class_type'] = seat_class_type
        if date_from is not None: search_results['date_from'] = date_from
        # if date_to is not None: search_results['date_to'] = date_to
        search_results['date_to'] = date_to
        
        # Format search results to match comparisons
        for k,v in search_results.items():
            val = str(v).replace('(', '').replace(')', '').replace(',','').replace("'", '')
            search_results[k] = val
            
            # If any value from search results is invalid or empty then cancel booking confirmation
            if (k != 'date_to') and (search_results.get(k) == ""):
                return redirect(url_for('views.index'))

        # If not logged in then login before creating a search
        if (session.get("logged_in") is None) or (session['logged_in'] == False):
            return redirect(url_for('auth.login'))

        if (session.get("logged_in") is not None) and (session['logged_in'] == True):
            for i in range(database.count_table_rows('journey')):
                table_record = database.get_table_record('journey', i)
                
                if (search_results['location_from'] == table_record[1]) and (search_results['location_to'] == table_record[3]):
                    print(f"Route found for: {table_record[1]} to {table_record[3]}")
                    booking = Booking(search_results)
                    
                    # If return date is none then it must be a one way ticket or same day return
                    if search_results.get('date_to') == '':
                        search_results['date_to'] = search_results.get('date_from')
                        
                    
                    search_results['departure_time'] = table_record[2]
                    search_results['return_time'] = table_record[4]
                    booking = Booking(search_results)
                    
                    if (return_trip == 'on') and (oneway_trip == 'None'):
                        search_results['trip_type'] = 'Return Trip'
                        booking.return_trip = True
                    elif (return_trip == 'None') and (oneway_trip == 'on'):
                        search_results['trip_type'] = 'Oneway Trip'
                        booking.return_trip = False
                        
                    # # If conditions are met then add data into the booking object
                    # booking = Booking(search_results)
                    
                    # Apply discount and price to the UI
                    search_results['discount'] = booking.get_booking_discount()
                    search_results['total_cost'] = booking.get_price()
                    
                    discount = search_results['discount']
                    total_cost = search_results['total_cost']
                    
                    preprocessor.set_dict(search_results)
                    print(search_results)
                    
                    return render_template('search.html', search_items = search_results)
                
                # If search does not match then cancel search
                if (i == database.count_table_rows('journey')) and (search_results['location_from'] != table_record[1]) and (search_results['location_to'] != table_record[3]):
                    return redirect(url_for('views.index'))
                
        return redirect(url_for('views.index'))

@views.route('/about-us/')
def about():
    print()
    return render_template('about.html')

@views.route('/terms-and-conditions/')
def legal():
    return render_template('legal.html')

@views.route('/account/')
def account_page():
    """ Redirects the user from auth to the genuine account page """
    if session['logged_in'] == False:
        return redirect(url_for('auth.login'))
    
    contacts = database.get_table_value_record('contacts', 'email_address', str(session['email']))
    contact_id = contacts[0]
    customer_id = contacts[1]
    telephone = contacts[2]
    email = contacts[3]
    
    customer = database.get_table_value_record('customers', 'customer_id', str(customer_id))
    fname = customer[1]
    lname = customer[2]
    
    accounts = database.get_table_value_record('accounts', 'contact_id', str(contact_id))
    username = accounts[2]
    
    account_id = int(accounts[0])
    
    # 1. SEARCH THROUGH ACCOUNT IDS FOR ALL BOOKINGS AND DYNAMICALLY UPDATE TO TABLE IN DASHBOARD
    
    # 2. DELETE OLD RECORDS FROM DATABASE IF RETURN_DATE HAS BEEN SURPASSED
    
    
    # database.update_table_record('accounts', 'username', 'reeceturner', 'account_id', 25000)
    
    
    
    return render_template(
        'account.html',
        current_username = str(username),
        current_fname = str(fname),
        current_lname = str(lname),
        current_telephone = str(telephone),
        current_email = str(email)
        )

@views.route('/account/<username>/<fname>/<lname>/<telephone>/<email>/')
def update_account(username, fname, lname, telephone, email):
    return redirect(url_for('auth.account'))

@sitemap.register_generator
def pages():
    yield 'views.index', {}, datetime.now(), 'monthly', 0.7
    # yield 'views.booking', {}, datetime.now(), 'monthly', 0.7
    yield 'views.about', {}, datetime.now(), 'monthly', 0.7
    yield 'views.legal', {}, datetime.now(), 'monthly', 0.7