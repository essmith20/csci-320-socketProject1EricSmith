import socket
import os
import hashlib  # needed to verify file hash
import struct
from typing import Tuple



IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size
address = (IP, PORT)


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8],byteorder='big')


def upload_file(server_socket: socket, file_name: str, file_size: int):
    # create a SHA256 object to verify file hash
    # TODO: section 1 step 5 in README.md file
    file_hash = hashlib.sha256()

    # create a new file to store the received data











    # get hash from client to verify
    #step 7
    # TODO: section 1 step 8 in README.md file
    # TODO: section 1 step 9 in README.md file
    #steps 7-9 below
    with open(file_name + '.temp', 'wb') as file:
        file_contents = file.read()
        file_hash.update(file_contents)
        hasher = file_hash.digest()

        # Create a socket object and connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)

        # Send the file size and file name to the server
        file_size = len(file_contents)
        file_name = file_name.split('/')[-1].encode()
        message = struct.pack('Q', file_size) + file_name
        sock.sendall(message)

        # Wait for the server to acknowledge the message
        response, _ = sock.recvfrom(1024)
        if response != b'go ahead':
            raise Exception("Server did not acknowledge message")

        # Send the file contents to the server
        sock.sendall(file_contents)

        # Wait for the server to acknowledge the file upload
        response, _ = sock.recvfrom(1024)
        if response != file_hash:
            raise Exception("File upload failed: hash mismatch")

        # Close the socket
        sock.close()


def start_server():
    # create a UDP socket and bind it to the specified IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f'Server ready and listening on {IP}:{PORT}')

    try:
        while True:
            # below is step 1 which is recvfrom
            response, address = server_socket.recvfrom(BUFFER_SIZE)

            #step 3
            def get_file_info(data: bytes) -> Tuple[int, str]:
                # Extract the file size as an 8-byte integer
                file_size = struct.unpack('Q', data[:8])[0]

                # Extract the file name as a string
                file_name = data[8:].decode()

                # Return a tuple of the file size and file name
                return file_size, file_name




            #step 4
            message = b'go ahead'
            server_socket.sendto(message, address)



         # expecting an 8-byte byte string for file size followed by file name







            upload_file(server_socket, file_name, file_size)
    except KeyboardInterrupt as ki:
        pass
    except Exception as e:
        print(f'An error occurred while receiving the file:str {e}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()
