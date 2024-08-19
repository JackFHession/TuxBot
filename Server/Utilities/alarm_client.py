import socket
import json

def send_request(request):
    server_address = "127.0.0.1"
    server_port = 2060

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    client_socket.send(request.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")

    client_socket.close()
    return json.loads(response)

if __name__ == "__main__":
    truth = True
    while truth:
        request = "check_for_alarm"
        task = send_request(request)
        print(task)
