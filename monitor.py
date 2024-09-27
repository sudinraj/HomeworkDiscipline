import subprocess
import threading
import time
import json
import signal
#import frontScreen

with open('games.json', 'r') as file:
    data = json.load(file)
    games = []
    for key, value in data.items():
        games = games+value

def getProcess():
    while True:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            if line.rstrip():
                # only print lines that are not empty
                # decode() is necessary to get rid of the binary string (b')
                # rstrip() to remove `\r\n`
                if(line.decode().rstrip().lower() in games):
                    print("mommmm")
                    #frontScreen.changeToAdd()
                #print(line.decode().rstrip().lower())
        time.sleep(5)

def start():
    thread.start()
thread = threading.Thread(target = getProcess, daemon = True)