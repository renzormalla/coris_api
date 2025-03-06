from coris_api.utils.http import http_status_post
from coris.helpers.cola import get_name_cola
from coris.middleware.env import get_var
from frappe.utils import now
import frappe
import json
import time

DEFAULT_PRODUCT_LEADS = get_var('DEFAULT_PRODUCT_LEADS')
frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger()
logger_api = frappe.logger("api", allow_site=True, file_count=50)

@frappe.whitelist()
def add_lead():
    request = frappe.local.request
    try:
        start_time = time.time()
        http_method = request.method

        if http_status_post(http_method):
            return

        body = json.loads(frappe.request.data)

        if not 'product' in body:
            body['product'] = DEFAULT_PRODUCT_LEADS

            result = frappe.get_all('Approval Campaign Table', 
                            filters={'parent': 'Approval Campaign', 'product': DEFAULT_PRODUCT_LEADS},
                            fields=['cola'])

            if result:
                if 'cola' in body:
                    body['cola'] = result[0].cola
                else:
                    body['cola'] = get_name_cola(result[0].cola)
        
        phone2 = ''
        phone3 = ''
        full_name = ''

        if 'full_name' in body:
            full_name = body['full_name']
        else:
            if 'names' in body and 'family_name' in body:
                full_name = f"{body['family_name']} {body['names']}"
            else:
                frappe.log_error(message=f"Not Found: full_name or names/family_name ->{request}", title="Error Token APIs")
                frappe.local.response['http_status_code'] = 400
                frappe.local.response["status_code"] = 400
                frappe.local.response["status"] = "BAD REQUEST"
                frappe.local.response["message"] = f"ERROR: No se ha encontrado full_name or names/family_name en la peticion"

                return

        doc = frappe.get_doc({
            "doctype":"External Leads",
            "status": 'IN QUEUE',
            "identification": body['identification'],
            "product": body['product'],
            "cola": body['cola'],
            "full_name": full_name,
            "phone": body['phone'] if 'phone' in body else "",
            "phone2": body['phone2'] if 'phone2' in body else "",
            "phone3": body['phone3'] if 'phone3' in body else "",
            "email": body['email'] if 'email' in body else "",
            "birth_date": body['birth_date'] if 'birth_date' in body else ""
        })

        doc.insert()

        time_taken = end_time - start_time
        logger_api.info(f"API: whatsapp/redirect_wp | Time taken: {time_taken:.4f} seconds")

        frappe.local.response['http_status_code'] = 201
        frappe.local.response["status_code"] = 201
        frappe.local.response["id_transaction"] = doc.name
        frappe.local.response["status"] = 'CREATED'
        frappe.local.response["message"] = 'LEAD CREADO CORRECTAMENTE'

        return

    except Exception as e:
        frappe.log_error(message=f"{str(e)} -> {request}", title="Error Token APIs")
        frappe.local.response['http_status_code'] = 500
        frappe.local.response["status_code"] = 500
        frappe.local.response["status"] = "INTERNAL SERVER ERROR"
        frappe.local.response["message"] = f"ERROR: {str(e)}"

        return