#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import socket

class chrono_thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.etat = True
        self.chrono_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chrono_socket.connect(('127.0.0.1', 1024))


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QButtonGroup, QGridLayout
from socket import socket, AF_INET, SOCK_STREAM

class Chronometre(QWidget):

    def __init__(self):
        super().__init__()

        self.compteur = 0
        self.arret_thread = False
        self.host = "127.0.0.1"
        self.port = 1024

        self.label_compteur = QLabel("Compteur : 0", self)
        self.line_edit_compteur = QLineEdit(self)
        self.line_edit_compteur.setEnabled(False)
        self.bouton_start = QPushButton("Start", self)
        self.bouton_reset = QPushButton("Reset", self)
        self.bouton_quitter = QPushButton("Quitter", self)
        self.bouton_connect = QPushButton("Connect", self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.label_compteur, 0, 0)
        self.layout.addWidget(self.line_edit_compteur, 0, 1)
        self.layout.addWidget(self.bouton_start, 1, 0)
        self.layout.addWidget(self.bouton_reset, 1, 1)
        self.layout.addWidget(self.bouton_quitter, 2, 0)
        self.layout.addWidget(self.bouton_connect, 2, 1)

        self.bouton_start.clicked.connect(self.start)
        self.bouton_reset.clicked.connect(self.reset)
        self.bouton_quitter.clicked.connect(self.quitter)
        self.bouton_connect.clicked.connect(self.connect)

    def start(self):
        self.arret_thread = False
        self.thread = threading.Thread(target=self.__start, args=())
        self.thread.start()

    def __start(self):
        while not self.arret_thread:
            time.sleep(1)
            self.compteur += 1
            self.line_edit_compteur.setText(str(self.compteur))

            try:
                with socket(AF_INET, SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    s.send("START".encode())
            except Exception as e:
                print(e)

    def reset(self):
        self.compteur = 0
        self.line_edit_compteur.setText("0")

    def quitter(self):
        self.arret_thread = True
        self.thread.join()
        sys.exit()

    def connect(self):
        try:
            with socket(AF_INET, SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.send("CONNECT".encode())
                response = s.recv(1024).decode()
                if response == "CONNECTED":
                    print("Connected to server")
                else:
                    print("Error connecting to server")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chronometre = Chronometre()
    chronometre.show()
    sys.exit(app.exec_())
