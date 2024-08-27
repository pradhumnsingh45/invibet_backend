import jwt
import datetime
from flask import Flask, request, jsonify
from functools import wraps
# Secret key for JWT encoding/decoding
SECRET_KEY = "my_app"

# In-memory store for user data and settings (for demonstration purposes)
user_data_store = {}
user_settings_store = {}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['id']
        except:
            return jsonify({"message": "Token is invalid!"}), 403
        return f(current_user_id, *args, **kwargs)
    return decorated