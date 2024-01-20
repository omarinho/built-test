from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )
    category = db.relationship(
        "Category", backref=db.backref("posts", lazy=True)
    )


def create_default_categories():
    from app import app

    with app.app_context():
        existing_categories = Category.query.all()
        if not existing_categories:
            general_category = Category(name="General")
            technology_category = Category(name="Technology")
            random_category = Category(name="Random")
            db.session.add_all(
                [general_category, technology_category, random_category]
            )
            db.session.commit()
