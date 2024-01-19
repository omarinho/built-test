from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Import the Config class from the config.py file

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from the Config class

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def show_config():
    # Accessing config values in the template
    return render_template('config.html', config=app.config)

if __name__ == '__main__':
    app.run(debug=True)
