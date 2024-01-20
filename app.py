from flask import Flask
from models import db, BlogPost, Category, create_default_categories
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

migrate = Migrate(app, db)

if __name__ == "__main__":
    # Import all routes from all available versions>
    # In this case, only version 1.0 exists
    from api_v1_0.routes import *

    create_default_categories()
    # Run the app
    app.run(port=5001, debug=True)
