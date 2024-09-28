import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QLabel
import PySide6.QtCore as QtCore
import queue
import add_game
import sys
import monitor
import signal, os
import subprocess
import threading
import time
import json

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 18pt;}")
windowMain = QtWidgets.QWidget()
windowMain.setFixedSize(300, 300)
windowMain.setWindowTitle("mom")
windowAdd = QtWidgets.QWidget()
windowAdd.setFixedSize(400, 300)
windowAdd.setWindowTitle("mom")

video = False

with open('games.json', 'r') as file:
    data = json.load(file)
    games = []
    for key, value in data.items():
        games = games+value

#code for checking if a game is being run
def getProcess():
    while True:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name"'
        cmd2 ="""powershell "gps | where {$_.MainWindowTitle -like '*Youtube*'}"""""
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        if video:
            proc2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
            x = (len(proc2.stdout.read().decode().rstrip()))
            if(x != 0):
                reminder()
                continue

        for line in proc.stdout:
            if line.rstrip():
                # only print lines that are not empty
                # decode() is necessary to get rid of the binary string (b')
                # rstrip() to remove `\r\n`
                if(line.decode().rstrip().lower() in games):
                    reminder()
                    break
                #print(line.decode().rstrip().lower())
        time.sleep(5)


thread = threading.Thread(target = getProcess, daemon = True)

def start():
    global video
    video = False
    windowMain.showMinimized()
    labelMain.setText("Mom is watching your games.")
    thread.start()

def startVideo():
    global video
    video = True
    windowMain.showMinimized()
    labelMain.setText("Mom is watching your games \nand YouTube.")
    thread.start()

#Main Laylout for main page
layoutMain = QtWidgets.QVBoxLayout()
labelMain = QLabel()
labelMain.setText("Awaken your mom.")
buttonStart = QtWidgets.QPushButton("Click to monitor games.")
buttonStart.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
buttonVideo = QtWidgets.QPushButton("Click to monitor games and YouTube.")
buttonVideo.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
buttonChange = QtWidgets.QPushButton("Click me to add games for mom to detect")
buttonChange.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
buttonStart.setToolTip("Mom will monitor if you are playing games")
buttonVideo.setToolTip("Mom will monitor if you are playing games and watching YouTube\n(It will only check if you have YouTube open actively, \nso you can turn on music and switch to a different tab)")
buttonChange.setToolTip("Click to add more games to the list of games your mom will detect")

layoutMain.addWidget(labelMain)
layoutMain.addWidget(buttonStart)
layoutMain.addWidget(buttonVideo)
layoutMain.addWidget(buttonChange)


#Layout for AddGame Page
layoutAdd = QtWidgets.QVBoxLayout()
labelAdd = QLabel()
labelAdd.setText("Find the name of the game in task\nmanager and enter here:")
textBox = QtWidgets.QLineEdit()
buttonAdd = QtWidgets.QPushButton("Add")
buttonAdd.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
buttonMain = QtWidgets.QPushButton("Back")
buttonMain.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
layoutAdd.addWidget(labelAdd)
layoutAdd.addWidget(textBox)
layoutAdd.addWidget(buttonAdd)
layoutAdd.addWidget(buttonAdd)
layoutAdd.addWidget(buttonMain)


#changes the layout to add game page
def changeToAdd():
    windowMain.hide()
    windowAdd.setLayout(layoutAdd)
    windowAdd.show()

def changeToMain():
    windowAdd.hide()
    windowMain.setLayout(layoutMain)
    windowMain.show()

def addToList():
    add_game.addGame(textBox.text().lower())
    textBox.clear()

def notifStop():
    print("a")

"""def handler(signum, frame):
    signame = signal.Signals(signum).name
    print(f'Signal handler called with signal {signame} ({signum})')

signal.signal(signal.sig, handler)"""

#the pop up window code
def reminder():
    #sys.exit()
    dlg = QtWidgets.QMessageBox()
    dlg.setWindowTitle("mom")
    dlg.setGeometry(800, 400, 300, 300)
    dlg.setText("STOP PLAYING GAMES!!!")
    dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | dlg.windowFlags() & QtCore.Qt.CustomizeWindowHint | dlg.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
    btn = dlg.addButton('YOU BETTER GET BACK TO DOING YOUR WORK OR ELSE!!!', QtWidgets.QMessageBox.DestructiveRole)
    dlg.setStyleSheet("QPushButton"
                             "{"
                             "background-color : red;"
                             "}")
    btn.setDisabled(True)
    
    #dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.NoButton)
    dlg.exec()

buttonAdd.clicked.connect(addToList)
buttonChange.clicked.connect(changeToAdd)
buttonMain.clicked.connect(changeToMain)
buttonStart.clicked.connect(start)
buttonVideo.clicked.connect(startVideo)

windowMain.setLayout(layoutMain)
windowMain.show()

app.exec()