# This is a client for connecting to nucpc server

import socket
address = ('192.168.0.156', 5001)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

def send_command(cli_sock, data):
    cli_sock.sendall(data.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    print(response)

if __name__ == "__main__":
    test_command = "generate_data"
    send_command(client_socket, test_command)

    
