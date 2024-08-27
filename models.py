from datetime import datetime
from entrypoint import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Numeric(5, 2), nullable=True)
    weight = db.Column(db.Numeric(5, 2), nullable=True)
    health_issues = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activities = db.relationship('UserActivity', backref='user', lazy=True)

class UserActivity(db.Model):
    __tablename__ = 'user_activity'

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    steps = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Numeric(10, 2), nullable=True)
    activity_date = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(255), nullable=True)

