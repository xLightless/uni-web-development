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
    return render_template('index.html')

@views.route('/booking/', methods=['GET', 'POST'])
def booking():
    # if session.get('username') is None:
    #     return redirect(url_for('views.account_page'))
    return render_template('booking.html')

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
    
    print(username, fname, lname, telephone, email)
    
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
    yield 'views.booking', {}, datetime.now(), 'monthly', 0.7
    yield 'views.about', {}, datetime.now(), 'monthly', 0.7
    yield 'views.legal', {}, datetime.now(), 'monthly', 0.7