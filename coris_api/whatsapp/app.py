from coris_api.utils.http import http_status_request
from coris_api.utils.middleware import decrypt_data
from coris_api.utils.jwt import validate_api
from frappe.utils import now
import frappe
import json
import time

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger()
logger_api = frappe.logger("api", allow_site=True, file_count=50)

@frappe.whitelist(allow_guest=True)
def redirect_wp(params):
    start_time = time.time()
    request = frappe.local.request
    http_method = request.method

    try:
        response_token = validate_api(request, http_method)
        if response_token['status_code'] == 200:
            end_time = time.time()

            data = decrypt_data(params)

            url = f"https://wa.me/593964039999?text=Hola%20Renzo%20Malla%20por%20favor%20elige%20en%20el%20siguiente%20menu."

            time_taken = end_time - start_time
            logger_api.info(f"API: whatsapp/redirect_wp | Time taken: {time_taken:.4f} seconds")
            http_status_request()
            return url

        frappe.log_error(message=f"{frappe.local.response}->{request}", title="Error Token APIs")
        return
    except:
        frappe.log_error(message=f"{frappe.local.response}->{request}", title="Error Token APIs")
        return
    