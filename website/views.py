from flask import Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime

from website import sitemap
from website.database import Database

views = Blueprint('views', __name__)
database = Database(database="ht_database", user="root", password="Password1")

# class Bookings(object):
#     """ Manages table UI for the booking web page """
    
#     booking_id = database.get_table_column('bookings', 'booking_id')[1]
#     booking_date = database.get_table_column('bookings', 'booking_date')[1]
#     journey_seat_types = database.get_table_column('bookings', 'journey_seat_types')[1]
#     advance_booking_days = database.get_table_column('bookings', 'advance_booking_days')[1]
#     booking_return_date = database.get_table_column('bookings', 'booking_return_date')[1]
    

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
    
        # radio_return        = request.form.get('params-traveller-return'),
        # radio_oneway        = request.form.get('params-traveller-oneway'),
        location_from       = request.form.get('input-box-from'),
        location_to         = request.form.get('input-box-to'),
        passengers_amount   = request.form.get('passengers-amount'),
        seat_class_type     = request.form.get('seat-class-type'),
        date_from           = request.form.get('swing-from-datepicker'),
        date_to             = request.form.get('swing-from-datepicker')
        
        search_results = {}
        if location_from is not None: search_results['location_from'] = location_from
        if location_to is not None: search_results['location_to'] = location_to
        if passengers_amount is not None: search_results['passengers_amount'] = passengers_amount
        if seat_class_type is not None: search_results['seat_class_type'] = seat_class_type
        if date_from is not None: search_results['date_from'] = date_from
        if date_to is not None: search_results['date_to'] = date_to
        
        # Format search results to match comparisons
        for k,v in search_results.items():
            val = str(v).replace('(', '').replace(')', '').replace(',','').replace("'", '')
            search_results[k] = val
            
            # If any value from search results is invalid or empty then cancel booking confirmation
            if (search_results.get(k) == ""):
                return redirect(url_for('views.index'))
        # print(database.get_table_value_record('journey', 'departure', value='Bristol'))
        
        
        
        journey_rows = database.count_table_rows('journey')
         
        
        # Remove
        return redirect(url_for('views.index'))
            
        
        # Checks if the params from the search submit is valid in the database
        
    
    # if (session.get("logged_in") is not None) and (session['logged_in'] == True):
    #     return render_template(
    #         'search.html',
    #         # radio_return        = request.form.get('params-traveller-return'),
    #         # radio_oneway        = request.form.get('params-traveller-oneway'),
    #         # location_from       = request.form.get('input-box-from'),
    #         # location_to         = request.form.get('input-box-to'),
    #         # passengers_amount   = request.form.get('passengers-amount'),
    #         # seat_class_type     = request.form.get('seat-class-type'),
    #         # date_from           = request.form.get('swing-from-datepicker'),
    #         # date_to             = request.form.get('swing-from-datepicker')
    #     )

    # return redirect(url_for('auth.login'))


def handle_search_results(*key, **val): pass

@views.route('/about-us/')
def about():
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
    
    # print(username, fname, lname, telephone, email)
    
    return redirect(url_for('auth.account'))



# Testing material for modernisation of website

# Temp routing for modifications to base
# @views.route('/newbase/')
# def newbase():
    
#     if session['logged_in'] == False:
#         return redirect(url_for('auth.login'))
#     return render_template('component_base.html')








@sitemap.register_generator
def pages():
    yield 'views.index', {}, datetime.now(), 'monthly', 0.7
    # yield 'views.booking', {}, datetime.now(), 'monthly', 0.7
    yield 'views.about', {}, datetime.now(), 'monthly', 0.7
    yield 'views.legal', {}, datetime.now(), 'monthly', 0.7