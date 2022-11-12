from flask import Blueprint, render_template
from datetime import datetime

from website import sitemap

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/booking')
def booking():
    return render_template('booking.html')

@sitemap.register_generator
def index():
    yield 'views.index', {}, datetime.now(), 'monthly', 0.7
    yield 'views.booking', {}, datetime.now(), 'monthly', 0.7