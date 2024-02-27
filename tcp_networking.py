import socket

# Define server host and port
SERVER_HOST = "172.20.10.4" # I don't know what IP this is.
SERVER_PORT = 55711

# Create a TCP socket.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # This should be while socket.Connected.
    while True:
        # Input message from the user.
        message = input("Enter message to send to server (type 'exit' to quit): ")

        # Send the message to the server
        client_socket.sendall(message.encode()) # UTF-8 encoding by default.
        if message.lower() == "exit":
            print("Exiting...")
            break

        # Receive the server's response
        server_response = client_socket.recv(1024) # Blocker
        print("Server response: ", server_response.decode())