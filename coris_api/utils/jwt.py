from coris_api.utils.http import http_status_post, http_status_get, http_status_validate, http_status_auth, http_status_jwt, http_status_request
from frappe.utils.password import get_decrypted_password
import datetime
import frappe
import json
import jwt

doctype = 'Queue WhatsApp'


def get_user(user, pwd):
    try:
        response = []
        password = get_decrypted_password("Auth JWT", user, 'pwd')
        
        if password == pwd:
            response = frappe.get_list("Auth JWT", filters={'username': user}, fields=['name'])
        
        if len(response) > 0:
            return True
        else:
            return False
    except:
        return False


def get_user_by_refresh_token(refresh_token):
    try:
        SECRET_KEY = 'G2cLy$xKJzQ#f44WAiC$87Io285#'

        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])

        user = decoded_token['user_id'].split("@")[0]

        response = []
        password = get_decrypted_password("Auth JWT", user, 'refresh_token')

        if refresh_token == password:

            response = frappe.get_list("Auth JWT", filters={'username': user}, fields=['name'])
        
        if len(response) > 0:
            return {
                'username': user,
                'found': True
            }
        else:
            return {
                'username': '',
                'found': False
            }
    except:
        return {
                'username': '',
                'found': False
            }


def generate_jwt(username):
    SECRET_KEY = 'G2cLy$xKJzQ#f44WAiC$87Io285#'

    payload = {
        'user_id': frappe.session.user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    payload_refresh = {
        'user_id': frappe.session.user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(payload_refresh, SECRET_KEY, algorithm='HS256')

    doc = frappe.get_doc('Auth JWT', username)
    doc.token = token
    doc.refresh_token = refresh_token

    doc.save(ignore_permissions=True)

    return {
        'status': True,
        'token': token,
        'refresh_token': refresh_token
    }


def verify_token(token):
    try:
        SECRET_KEY = 'G2cLy$xKJzQ#f44WAiC$87Io285#'
        
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        expiration_time = datetime.datetime.utcfromtimestamp(decoded_token['exp'])
        current_time = datetime.datetime.utcnow()

        if decoded_token['user_id'] != frappe.session.user:
            return 401

        user = decoded_token['user_id'].split("@")[0]
        password = get_decrypted_password("Auth JWT", user, 'token')

        if current_time > expiration_time:
            return 400
        else:
            if password == token:
                return 200
            else:
                return 401
    except:
        return 401


def validate_api(request, http_method):

    if http_status_get(http_method):
        return 
    else:
        header = request.headers.get('X-Access-Token')
        if header:
            header = header.split(" ")

            if len(header) == 2:
                auth_type = header[0]
                if auth_type.lower() == 'bearer':
                    v_token = verify_token(header[1])
                    if v_token == 200:
                        return {
                            'status_code': 200
                        }
                    if v_token == 400:
                        http_status_validate('bad_formed')
                        return
                    if v_token == 401:
                        http_status_jwt()
                        return
                else:
                    http_status_validate('bad_formed')
                    return
            else:
                http_status_validate('bad_formed')
                return
        else:
            http_status_jwt()
            return