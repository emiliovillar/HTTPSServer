import socket
import os

HOST = "127.0.0.1" #localhost
PORT = 8080        # any port

def handle_connection(client_socket):

    print("--- Connection Accepted ---")

    # 1. read on socket
    request_data = client_socket.recv(4096) # 4kb
    
    if not request_data:
        print("Received empty request, closing connection.")
        client_socket.close()
        return

    # inbound message for debugging
    print("\n[Inbound Message]\n" + request_data.decode('utf-8', 'ignore').split('\n')[0].strip())


    # 2. need httop request parsing 
    
    requested_file = "index.html" # Placeholder for requested file
    
    # 3. neef file Handling and rhttp responses
    #    - Open the requested file.
    #    - Set the Content-Type based on the file type (e.g., text/html, image/jpeg).
    #    - Construct the complete HTTP response (Status Line, Headers, Body).
    
    response_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" # Placeholder header
    response_body = b"<html><body><h1>Placeholder Content. Teammate 2 needs to load the file!</h1></body></html>" # Placeholder body
    
    full_response = response_header + response_body

    #  outbound message for debugging 
    print("\n[Outbound Message]\n" + response_header.decode('utf-8', 'ignore').split('\n')[0].strip())

    # 4. Send the content back to the browser
    client_socket.sendall(full_response)
    
    # 5. Close the connection 
    client_socket.close()
    print("--- Connection Closed ---\n")


def run_server():
    
    # open socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        
        #  start listening for connections
        server_socket.listen(5) # backlog of 5 connections
        print(f"Starting server at http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop the server.")

        while True:
          #server waits here for a connection.
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            
            #processing the request
            handle_connection(client_socket)
            
            #  server now waiting for a new connection (back to while True)

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the server socket 
        server_socket.close()
        print("Server stopped.")

if __name__ == '__main__':
    run_server()