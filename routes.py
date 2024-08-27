import datetime
import random
import string
import jwt
from flask import Flask, request, jsonify
from twilio.rest import Client
from orm_functions import create_data_entry, create_user,update_data_entry,set_user_settings,get_user_settings



from middleware import token_required

otp_store = {}

def define_routes(app):

    @app.route("/public/health", methods=["GET"])
    def health_ping():
        return jsonify({'message': 'success'}), 200
    
    @app.route('/send-otp', methods=['POST'])
    def send_otp():
        data = request.get_json()
        phone_number = data.get('phone_number')
       

        if not phone_number:
            print(phone_number)
            return jsonify({"error": "Phone number is required"}), 400
        
        try:
            payload = {
                "phone_number":phone_number
            }
            print("abc",phone_number)
            user, created = create_user(payload)
        except ValueError as e:
            raise e
            return jsonify({"error": str(e)}), 400
    

        otp = generate_otp()
        otp_store[phone_number] = otp

        try:
            message = client.messages.create(
                body=f"Your verification code is {otp}",
                from_=twilio_phone_number,
                to=phone_number
            )
            return jsonify({"message": "OTP sent successfully", "sid": message.sid})
        except Exception as e:
            raise e
            return jsonify({"error": str(e)}), 500

    @app.route('/verify-otp', methods=['POST'])
    def verify_otp():
        data = request.json
        phone_number = data.get('phone_number')
        otp = data.get('otp')
    
        if not phone_number or not otp:
            return jsonify({"message": "Phone number and OTP are required"}), 400

        if not phone_number or not otp:
            return jsonify({"error": "Phone number and OTP are required"}), 400

        stored_otp = otp_store.get(phone_number)
        if stored_otp and stored_otp == otp:
            # Create a JWT token with a hardcoded ID
            payload = {
                "id": 1,  # Replace with your actual logic to generate the ID
                "phone_number": phone_number,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3600)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            
            # Clear OTP after verification
            otp_store.pop(phone_number, None)
            
            return jsonify({"message": "OTP verified", "token": token}), 200
    
        return jsonify({"message": "Invalid OTP"}), 400

    @app.route('/data', methods=['POST'])
    @token_required
    def create_data(current_user_id):
        data = request.json
        entry = create_data_entry(current_user_id, data)
        return jsonify({"message": "Data entry created", "entry": {
            "entry_id": entry.activity_id,
            "date": entry.activity_date,
            "steps": entry.steps,
            "calories": entry.calories,
            "distance": entry.distance
        }}), 201

    @app.route('/data/<int:entry_id>', methods=['PUT'])
    @token_required
    def update_data(current_user_id, entry_id):
        data = request.json
        entry = update_data_entry(current_user_id, entry_id, data)
        
        if not entry:
            return jsonify({"message": "Entry not found"}), 404
        
        return jsonify({"message": "Data entry updated", "entry": {
            "entry_id": entry.activity_id,
            "date": entry.activity_date,
            "steps": entry.steps,
            "calories": entry.calories,
            "distance": entry.distance
        }}), 200

    @app.route('/user-settings', methods=['POST', 'PUT'])
    @token_required
    def set_user_settings_route(current_user_id):
        data = request.json
        current_user_id=1
        settings = set_user_settings(current_user_id, data)
        
        if not settings:
            return jsonify({"message": "User not found"}), 404
        
        return jsonify({"message": "User settings saved", "settings": {
            "gender": settings.gender,
            "age": settings.age,
            "height": settings.height,
            "weight": settings.weight,
            "health_issues": settings.health_issues,
            "active": settings.active
        }}), 200

    @app.route('/user-settings', methods=['GET'])
    @token_required
    def get_user_settings_route(current_user_id):
        settings = get_user_settings(current_user_id)
        
        if not settings:
            return jsonify({"message": "Settings not found"}), 404
        
        return jsonify({"settings": {
            "gender": settings.gender,
            "age": settings.age,
            "height": settings.height,
            "weight": settings.weight,
            "health_issues": settings.health_issues,
            "active": settings.active
        }}), 200



def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))
