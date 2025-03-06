import frappe


def auth_log(user, method):
    frappe.get_doc({
        'doctype': 'Auth Logs',
        'user': user,
        'status': 'OK',
        'ip_address': ip_address,
        'method_auth': method
    }).insert(ignore_permissions=True)