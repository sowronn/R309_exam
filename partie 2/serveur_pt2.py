import socket
etat = True

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 1024))
server_socket.listen(1)

print('Waiting connection...')
conn, address = server_socket.accept()
print(f'Connected')


def start_compteur():
    global compteur
    while True:
        compteur += 1

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.send(str(compteur).encode())

                self.line_edit_compteur.setText(str(compteur))
        except Exception as e:
            print(e)

def stop_compteur():
    global compteur
    compteur = 0

def connect():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send("CONNECT".encode())
            response = s.recv(1024).decode()
            if response == "CONNECTED":
                print("Connected to server")
            else:
                print("Error connecting to server")
    except Exception as e:
        print(e)

def main():
    connect()

    start_compteur()

if __name__ == "__main__":
    main()