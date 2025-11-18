from functools import wraps
from flask import request, jsonify
import os
import re

def check_auth():
    try:
        # Get session from either cookie or body
        cookies = request.cookies
        data = request.get_json()
        
        session_id = None
        # Check in cookies first
        if 'PHPSESSID' in cookies:
            session_id = cookies['PHPSESSID']
        # Then check in body
        elif data and '_session' in data:
            session_id = data['_session']
            
        if not session_id:
            return None, "Login required"

        # Read PHP session file
        session_file = os.path.join('/tmp', f'sess_{session_id}')
        if not os.path.exists(session_file):
            return None, "Login required"

        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = f.read()

        # Extract user ID and role from session data
        user_id_match = re.search(r'_authenticated_user_id\|s:\d+:"(\d+)"', session_data)
        role_match = re.search(r'_authenticated_user_role\|s:\d+:"([^"]+)"', session_data)

        if not user_id_match:
            return None, "Login required"

        return {
            'userId': user_id_match.group(1),
            'userRole': role_match.group(1) if role_match else None
        }, None

    except Exception as e:
        return None, "Internal server error"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_info, error = check_auth()
        
        if error:
            error_code = 500 if error == "Internal server error" else 1501
            return {'success': False,"error": {'message': error}}

        # Add user info to request context
        request.user_id = user_info['userId']
        request.user_role = user_info['userRole']
        
        return f(*args, **kwargs)
    return decorated 