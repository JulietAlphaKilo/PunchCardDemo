import socket

def receive_scan_from_server(server_ip, port, new_filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, port))
        print("Connected to server...")

        with open(new_filename, 'wb') as received:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    received.write(data)

    finally:
        client.close()
