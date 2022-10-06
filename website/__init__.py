from flask import Flask, render_template

def page_not_found(e):
    return render_template('404.html'), 404

def create_flask_app():
    app = Flask(__name__, static_url_path='/static')
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    app.register_error_handler(404, page_not_found)
    
    return app