from website import create_flask_app
from flask import render_template

app = create_flask_app()

if __name__ == '__main__':
    app.run(debug=True)