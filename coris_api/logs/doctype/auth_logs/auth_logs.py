# Copyright (c) 2025, Coris del Ecuador and contributors
# For license information, please see license.txt

import uuid
import frappe
from frappe.model.document import Document


class AuthLogs(Document):
	def autoname(self):
		self.name = str(uuid.uuid4())
