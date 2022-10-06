from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/booking')
def booking():
    return render_template('booking.html')

# url_for('static', filename='index.html')