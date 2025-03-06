import frappe


def http_status_get(http_method='', name='', type_method='', data=''):
    if http_method != 'GET':
        frappe.local.response['http_status_code'] = 405
        frappe.local.response["status_code"] = 405
        frappe.local.response["status"] = "METHOD NOT ALLOWED"
        frappe.local.response["message"] = f"Error en el metodo de la peticion."

        return f"Error en el metodo de la peticion."


def http_status_post(http_method='', name='', type_method='', data=''):
    if http_method != 'POST':
        frappe.local.response['http_status_code'] = 405
        frappe.local.response["status_code"] = 405
        frappe.local.response["status"] = "METHOD NOT ALLOWED"
        frappe.local.response["message"] = f"Error en el metodo de la peticion."

        return f"Error en el metodo de la peticion."


def http_status_validate(value='', name='', type_method='', data=''):

    if value == 'params':
        frappe.local.response['http_status_code'] = 400
        frappe.local.response["status_code"] = 400
        frappe.local.response["status"] = "BAD REQUEST"
        frappe.local.response["message"] = 'Necesitas el uso de user/pwd o token para iniciar sesion'

        return 'Necesitas el uso de user/pwd o token para iniciar sesion'
    
    if value == 'bad_formed':
        frappe.local.response['http_status_code'] = 400
        frappe.local.response["status_code"] = 400
        frappe.local.response["status"] = "BAD REQUEST"
        frappe.local.response["message"] = 'Tokens mal formados'

        return 'Tokens mal formados'
    
    if value == 'bad_request':
        frappe.local.response['http_status_code'] = 400
        frappe.local.response["status_code"] = 400
        frappe.local.response["status"] = "BAD REQUEST"
        frappe.local.response["message"] = 'Petición mal formada'

        return 'Petición mal dormada'
    
    if value == 'login':
        frappe.local.response['http_status_code'] = 401
        frappe.local.response["status_code"] = 401
        frappe.local.response["status"] = "UNAUTHORIZED"
        frappe.local.response["message"] = 'El usuario o contraseña ingresado son incorrectas'

        return 'El usuario o contraseña ingresado son incorrectas'

    if value == 'refresh_token':
        frappe.local.response['http_status_code'] = 401
        frappe.local.response["status_code"] = 401
        frappe.local.response["status"] = "UNAUTHORIZED"
        frappe.local.response["message"] = 'El token es incorrecto o a caducado'

        return 'El token es incorrecto o a caducado'


def http_status_auth(name, token, refresh_token, type_method):
    frappe.local.response['http_status_code'] = 200
    frappe.local.response["status_code"] = 200
    frappe.local.response["status"] = "OK"
    frappe.local.response["unique_id"] = name
    frappe.local.response["token"] = token
    frappe.local.response["refresh_token"] = refresh_token
    frappe.local.response["auth_type"] = type_method
    frappe.local.response["message"] = "Solicitud correcta."

    return "Solicitud correcta."


def http_status_jwt():
    frappe.local.response['http_status_code'] = 401
    frappe.local.response["status_code"] = 401
    frappe.local.response["status"] = "UNAUTHORIZED"
    frappe.local.response["message"] = "El token ha caducado o es incorrecto"

    return "El token ha caducado o es incorrecto"


def http_status_request():
    frappe.local.response['http_status_code'] = 200
    frappe.local.response["status_code"] = 200
    frappe.local.response["status"] = "OK"
    frappe.local.response["message"] = "Solicitud correcta."

    return "Solicitud correcta."