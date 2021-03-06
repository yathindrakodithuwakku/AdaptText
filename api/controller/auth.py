from flask import Blueprint, jsonify, request, make_response
from ..connection.initializers import guard

auth_controller = Blueprint('auth', __name__)


@auth_controller.route('/login', methods=['POST'])
def login():
    """
    Login the user
    :rtype: object
    """
    json_obj = request.get_json()
    if not json_obj:
        return make_response(jsonify({'error': 'Bad Request', 'message': 'No credentials provided', 'status_code': 400}), 400)

    try:
        user_name = json_obj['username']
        password = json_obj['password']
    except:
        return make_response(jsonify({'error': 'Bad Request', 'message': 'No credentials provided', 'status_code': 400}), 400)

    # authenticate and encode the user
    user = guard.authenticate(user_name, password)
    token = guard.encode_jwt_token(user)

    return jsonify({'access_token': token}), 200


@auth_controller.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh token
    :rtype: object
    """
    json_data = request.get_json()

    if not json_data:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'Token not found', 'status_code': 400}), 400)

    prev_token = json_data['token']
    if not prev_token:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'Token not found', 'status_code': 400}), 400)

    # refresh and return the token
    token = guard.refresh_jwt_token(prev_token)
    return jsonify({'access_token': token})
