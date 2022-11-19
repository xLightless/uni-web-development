from flask import Blueprint, render_template, session
from datetime import datetime

from website import sitemap

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/booking')
def booking():
    return render_template('booking.html')

@views.route('/about-us')
def about():
    return render_template('about.html')

@views.route('/terms-and-conditions')
def legal():
    return render_template('legal.html')

@sitemap.register_generator
def pages():
    yield 'views.index', {}, datetime.now(), 'monthly', 0.7
    yield 'views.booking', {}, datetime.now(), 'monthly', 0.7
    yield 'views.about', {}, datetime.now(), 'monthly', 0.7
    yield 'views.legal', {}, datetime.now(), 'monthly', 0.7