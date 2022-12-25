from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime

from website import sitemap
from website.database import Database

views = Blueprint('views', __name__)
database = Database(database="ht_database")

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
    return render_template('account.html')







# Testing material for modernisation of website
@views.route('/travelComponent/')
def travel_component():
    return render_template('component_travel_box.html')

@views.route('/newbase/')
def newbase():
    return render_template('component_base.html')








@sitemap.register_generator
def pages():
    yield 'views.index', {}, datetime.now(), 'monthly', 0.7
    yield 'views.booking', {}, datetime.now(), 'monthly', 0.7
    yield 'views.about', {}, datetime.now(), 'monthly', 0.7
    yield 'views.legal', {}, datetime.now(), 'monthly', 0.7