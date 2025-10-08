import socket
import os
import argparse

HOST = "127.0.0.1" #localhost
DEFAULT_PORT = 8080        # default port

def parse_http_request(request_data):
    """
    Parse HTTP request to extract the requested file path.
    
    Args:
        request_data (bytes): Raw HTTP request data
        
    Returns:
        str: The requested file path (sanitized)
    """
    try:
        # Decode the request data to string
        request_str = request_data.decode('utf-8', 'ignore')
        
        # Split into lines and get the first line (request line)
        lines = request_str.split('\r\n')
        if not lines:
            return "index.html"  # Default fallback
            
        request_line = lines[0].strip()
        print(f"[DEBUG] Request line: {request_line}")
        
        # Parse the request line: METHOD PATH HTTP/VERSION
        parts = request_line.split()
        if len(parts) < 2:
            return "index.html"  # Default fallback
            
        method = parts[0]
        path = parts[1]
        
        # Only handle GET requests for now
        if method.upper() != 'GET':
            print(f"[DEBUG] Unsupported method: {method}")
            return "index.html"  # Default fallback for unsupported methods
            
        # Handle root path
        if path == '/':
            return "index.html"
            
        # Remove leading slash and sanitize path
        if path.startswith('/'):
            path = path[1:]
            
        # Basic security: prevent directory traversal
        if '..' in path or path.startswith('/'):
            print(f"[DEBUG] Suspicious path detected: {path}")
            return "index.html"  # Default fallback for security
            
        # Remove query string if present
        if '?' in path:
            path = path.split('?')[0]
            
        print(f"[DEBUG] Parsed file path: {path}")
        return path
        
    except Exception as e:
        print(f"[ERROR] Failed to parse HTTP request: {e}")
        return "index.html"  # Default fallback

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


    # 2. HTTP request parsing - 
    requested_file = parse_http_request(request_data)
    print(f"[DEBUG] Requested file: {requested_file}")
    
    # 3. File Handling and HTTP responses 
    #    
    #    Required implementation:
    #    - Import mimetypes library at the top of the file
    #    - Create generate_http_response(file_path) function that:
    #      * Checks if file exists using os.path.exists()
    #      * If file exists: read file in binary mode, determine MIME type, 
    #        build HTTP/1.1 200 OK response with proper headers
    #      * If file missing: return HTTP/1.1 404 Not Found with HTML error page
    #    - Replace the placeholder code below with: full_response = generate_http_response(requested_file)
    #    
    #    Headers needed for 200 OK:
    #    - Content-Type: (use mimetypes.guess_type() based on file extension)
    #    - Content-Length: (exact byte length of file content)
    #    - Connection: close
    #    
    #    Headers needed for 404:
    #    - Content-Type: text/html
    #    - Content-Length: (length of error HTML)
    #    - Connection: close
    
    # PLACEHOLDER: replace this with actual file serving
    response_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" # Placeholder header
    response_body = b"<html><body><h1>Placeholder Content. Teammate 2 needs to load the file!</h1><p>Requested file: " + requested_file.encode() + b"</p></body></html>" # Placeholder body
    
    full_response = response_header + response_body

    #  outbound message for debugging 
    print("\n[Outbound Message]\n" + response_header.decode('utf-8', 'ignore').split('\n')[0].strip())

    # 4. Send the content back to the browser
    client_socket.sendall(full_response)
    
    # 5. Close the connection 
    client_socket.close()
    print("--- Connection Closed ---\n")


def run_server(port):
    
    # open socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # bind the socket to the host and port
        server_socket.bind((HOST, port))
        
        #  start listening for connections
        server_socket.listen(5) # backlog of 5 connections
        print(f"Starting server at http://{HOST}:{port}")
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
    # Command-line argument parsing - 
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, 
                       help=f'Port number to listen on (default: {DEFAULT_PORT})')
    
    args = parser.parse_args()
    
    print(f"[DEBUG] Starting server on port {args.port}")
    run_server(args.port)