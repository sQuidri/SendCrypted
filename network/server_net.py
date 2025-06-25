import socket
import os
import struct
from crypto.aes_utils import aes_utils

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
        file_name = self.recv_helper(conn)
        print(f"[Server] Receiving file: {file_name}")

        # receive the file size
        file_size = int(self.recv_helper(conn))
        print(f"[Server] File size: {file_size} bytes")

        file_path = os.path.join(self.save_dir, file_name)

        # open the file in binary write mode and receive the file data in chunks
        with open(file_path, 'wb') as f:
            bytes_received = 0
            total_encrypted_received = 0
            symmetricKeyUtils = aes_utils()
            while bytes_received < file_size:
                # read 4 bytes for the length of the encrypted chunk
                raw_len = self.recv_helper(conn, 4)
                if not raw_len:
                    break
                enc_chunk_len = struct.unpack('>I', raw_len)[0]
                if enc_chunk_len == 0:
                    break
                # read the encrypted chunk
                chunk = self.recv_helper(conn, enc_chunk_len)
                if not chunk:
                    break
                total_encrypted_received += len(chunk)
                decrypted_data = symmetricKeyUtils.decryptMessage(chunk)
                f.write(decrypted_data)
                bytes_received += len(decrypted_data)
        print(f"[Server] Total encrypted bytes received: {total_encrypted_received}")
        print(f"[Server] Total decrypted bytes written: {bytes_received}")

        # close the connection
        conn.close()
        print("[Server] Connection closed.")
        try:
            os.remove(aes_utils.symmetricFile)
            print(f"[Server] Deleted symmetric key file: {aes_utils.symmetricFile}")
        except Exception as e:
            print(f"[Server][WARNING] Could not delete symmetric key file: {e}")

    def recv_helper(self, conn, n=None):
        # helper function to receive data from the connection
        if n is None:
            # read until newline or EOF
            line = b""
            while True:
                char = conn.recv(1)
                if char == b'\n' or not char:
                    break
                line += char
            return line.decode().strip()
        else:
            # read n bytes
            data = b''
            while len(data) < n:
                packet = conn.recv(n - len(data))
                if not packet:
                    return None
                data += packet
            return data