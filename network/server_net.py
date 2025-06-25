import socket
import os

class server_net:
    def __init__(self, port, save_dir="received_files"):
        # store the port and directory for received files
        self.port = port
        self.save_dir = save_dir
        # make the directory only if it doesnt exist
        os.makedirs(save_dir, exist_ok=True)
        # make a tcp socket and bind to all interfaces on the specified port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        # listen for one connection
        self.server_socket.listen(1)
        print(f"[Server] Listening on port {port}...")

    def accept_and_receive_file(self):
        # accept a connection and store the connection and address
        conn, addr = self.server_socket.accept()
        print(f"[Server] Connected by {addr[0]}:{addr[1]}")

        # receive the file name
        file_name = self.receive_line(conn)
        print(f"[Server] Receiving file: {file_name}")

        # receive the file size
        file_size = int(self.receive_line(conn))
        print(f"[Server] File size: {file_size} bytes")

        file_path = os.path.join(self.save_dir, file_name)

        # open the file in binary write mode and receive the file data in chunks
        with open(file_path, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                chunk = conn.recv(min(1024, file_size - bytes_received))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)
        print(f"[Server] File saved to {file_path}")

        # close the connection
        conn.close()
        print("[Server] Connection closed.")

    def receive_line(self, conn):
        # helper function for receiving a line of text from the connection
        line = b""
        while True:
            char = conn.recv(1)
            # check for newline character or end of stream
            if char == b'\n' or not char:
                break
            line += char
        return line.decode().strip()