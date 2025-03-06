from coris_api.utils.http import http_status_post, http_status_validate, http_status_auth
from coris_api.utils.jwt import get_user, generate_jwt, get_user_by_refresh_token
import frappe
import json

@frappe.whitelist()
def get_token():
    try:
        data = json.loads(frappe.request.data)
        request = frappe.local.request
        http_method = request.method

        if http_status_post(http_method):
            return

        if not 'username' in data and not 'pwd' in data and not 'refresh_token' in data:
            if http_status_validate('params'):
                return

        if not 'refresh_token' in data:
            flag = get_user(data['username'], data['pwd'])
            if not flag:
                http_status_validate('login')
                return

            jwt_data = generate_jwt(data['username'])

            if jwt_data['status']:
                http_status_auth('', jwt_data['token'], jwt_data['refresh_token'], 'Bearer')
                return

        if data['refresh_token']:
            flag = get_user_by_refresh_token(data['refresh_token'])
            if not flag['found']:
                http_status_validate('refresh_token')

            jwt_data = generate_jwt(flag['username'])

            if jwt_data['status']:
                http_status_auth('', jwt_data['token'], jwt_data['refresh_token'], 'Bearer')
                return
    except Exception as e:
        http_status_validate('bad_request')
        return str(e)