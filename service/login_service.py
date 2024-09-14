from models import User, UserActivity
from datetime import datetime



class LoginService:
    def __init__(self,ses):
        self.s = ses


    def create_data_entry(self,user_id, data):
        from entrypoint import db
        new_activity = UserActivity(
            user_id=user_id,
            steps=data.get('steps'),
            calories=data.get('calories'),
            distance=data.get('distance'),
            activity_date=data.get('date', datetime.utcnow().datcde())
        )
        db.session.add(new_activity)
        db.session.commit()
        return new_activity

    def create_user(self,params):
        from entrypoint import db
        phone_number = params.get('phone_number')
        gender = params.get('gender')
        age = params.get('age')
        height = params.get('height')
        weight = params.get('weight')
        health_issues = params.get('health_issues')
        active = params.get('active', True)
        print(params)
        if not phone_number:
            raise ValueError("Phone number is required")

        # Check if user already exists
        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            return existing_user, False  # User already exists
        
        # Create a new user
        new_user = User(
            phone_number=phone_number,
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            health_issues=health_issues,
            active=active,
            created_on=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, True  # New user created

    def update_data_entry(self,user_id, entry_id, data):
        from entrypoint import db
        entry = UserActivity.query.filter_by(user_id=user_id, activity_id=entry_id).first()
        
        if entry:
            entry.steps = data.get('steps', entry.steps)
            entry.calories = data.get('calories', entry.calories)
            entry.distance = data.get('distance', entry.distance)
            entry.activity_date = data.get('date', entry.activity_date)
            entry.updated_at = datetime.utcnow()
            db.session.commit()
        
        return entry

    def set_user_settings(self,user_id, settings):
        from entrypoint import db
        user = User.query.get(user_id)
        
        if user:
            user.gender = settings.get('gender', user.gender)
            user.age = settings.get('age', user.age)
            user.height = settings.get('height', user.height)
            user.weight = settings.get('weight', user.weight)
            user.health_issues = settings.get('health_issues', user.health_issues)
            user.active = settings.get('active', user.active)
            user.updated_on = datetime.utcnow()
            db.session.commit()
        
        return user

    def get_user_settings(self,user_id):
        from entrypoint import db
        return User.query.get(user_id)