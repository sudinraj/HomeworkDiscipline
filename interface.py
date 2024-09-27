import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QLabel
import PySide6.QtCore as QtCore
import add_game
import sys
import subprocess
import threading
import time
import json

pause = False

with open('games.json', 'r') as file:
    data = json.load(file)
    games = []
    for key, value in data.items():
        games = games+value

def getProcess():
    while not pause:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Name'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            if line.rstrip():
                # only print lines that are not empty
                # decode() is necessary to get rid of the binary string (b')
                # rstrip() to remove `\r\n`
                if(line.decode().rstrip().lower() in games):
                    print("mommmm")
                    reminder()
                #print(line.decode().rstrip().lower())
        time.sleep(5)

def start():
    thread.start()
thread = threading.Thread(target = getProcess, daemon = True)


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 18pt;}")
windowMain = QtWidgets.QWidget()
windowMain.setFixedSize(300, 300)
windowAdd = QtWidgets.QWidget()
windowAdd.setFixedSize(400, 300)

#Main Laylout for main page
layoutMain = QtWidgets.QVBoxLayout()
labelMain = QLabel()
labelMain.setText("Awaken your mom.")
buttonStart = QtWidgets.QPushButton("Click to turn your mom on.")
buttonStart.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
buttonChange = QtWidgets.QPushButton("Click me to add games for mom to detect")
buttonChange.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgray;"
                             "}") 
buttonChange.setToolTip("Click to add more games to the list of games your mom will detect")

layoutMain.addWidget(labelMain)
layoutMain.addWidget(buttonStart)
layoutMain.addWidget(buttonChange)

#Layout for AddGame Page
layoutAdd = QtWidgets.QVBoxLayout()
labelAdd = QLabel()
labelAdd.setText("Name of the game:")
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

def reminder():
    global pause
    #pause = True
    dlg = QtWidgets.QDialog()
    dlg.setWindowTitle("ANGRY MOM")
    dlg.setFixedSize(300,70)
    layoutWork = QtWidgets.QVBoxLayout()
    message = QLabel()
    message.setText("STOP PLAYING GAMES!!!")
    dlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    layoutWork.addWidget(message)
    dlg.setLayout(layoutWork)
    dlg.exec()

buttonAdd.clicked.connect(addToList)
buttonChange.clicked.connect(changeToAdd)
buttonMain.clicked.connect(changeToMain)
buttonStart.clicked.connect(start)

windowMain.setLayout(layoutMain)
windowMain.show()

app.exec()

"""
class main(QtWidgets.QMainWindow):
    def __init__ (self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(self)
        label.setText("Awaken your mom.")
        buttonStart = QtWidgets.QPushButton("Click me")
        layout.addWidget(label)
        layout.addWidget(buttonStart)
        buttonStart.clicked.connect(monitor.getProcess)
        self.setLayout(layout)
"""