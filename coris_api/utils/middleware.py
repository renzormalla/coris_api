from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import base64
import frappe
import json

KEY_AES = 'pymZmDl1JoIfrL1558CVXN2LqsDiTYaj'

@frappe.whitelist()
def encrypted(data=None):
    key = KEY_AES
    key = base64.b64decode(key)

    data = json.loads(data)

    plaintext = json.dumps(data)
    iv = get_random_bytes(AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)

    encrypted = {
        'iv': base64.b64encode(iv).decode('utf-8'),
        'value': base64.b64encode(ciphertext).decode('utf-8')
    }

    return base64.b64encode(json.dumps(encrypted).encode('utf-8')).decode('utf-8')


def decrypt_data(data):
    encrypted_data = data
    key = KEY_AES
    key = base64.b64decode(key)

    decoded_data = json.loads(base64.b64decode(encrypted_data).decode('utf-8'))

    iv = base64.b64decode(decoded_data['iv'])
    ciphertext = base64.b64decode(decoded_data['value'])
    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return json.loads(decrypted_data.decode('utf-8'))