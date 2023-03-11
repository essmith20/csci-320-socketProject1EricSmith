import socket
import hashlib  # needed to calculate the SHA256 hash of the file
import sys  # needed to get cmd line parameters
import os.path as path  # needed to get size of file in bytes
import struct


IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str):
    # get the file size in bytes
    # TODO: section 2 step 2 in README.md file
    file_size = path.get_size(filename)


    # convert the file size to an 8-byte byte string using big endian
    # TODO: section 2 step 3 in README.md file
    file_size_bytes = struct.pack('>Q', file_size)




    # create a SHA256 object to generate hash of file
    # TODO: section 2 step 4 in README.md file
    file_hash = hashlib.sha256()

    # create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        # TODO: section 2 step 6 in README.md file
        file_name = 'myfile.txt'.encode('utf-8')
        message = file_size_bytes + file_name


        # TODO: section 2 step 7 in README.md file
        response, address = client_socket.recvfrom(BUFFER_SIZE)
        if response != b'go ahead':
            raise Exception('Bad server response - was not go ahead!')


        # open the file to be transferred
        with open(file_name, 'rb') as file:
            # read the file in chunks and send each chunk to the server
            # TODO: section 2 step 8 a-d in README.md file
            while True:
                # read a chunk of data from file
                chunk = f.read(1024)

                # if chunk length is greater than 0, update hash and send chunk to server
                if len(chunk) > 0:
                    # update hash with chunk data
                    file_hash.update(chunk)

                    # send chunk to server
                    client_socket.sendto(chunk, address)

                    # wait for 'received' acknowledgment from server
                    data, address = client_socket.recvfrom(1024)
                    if data != b'received':
                        raise Exception('Bad server response - was not received')
                else:
                    # no more data to send
                    break


        # send the hash value so server can verify that the file was
        # received correctly.
        # TODO: section 2 step 9 in README.md file
        finalhash = file_hash.digest()
        client_socket.sendto(finalhash, address)

        # TODO: section 2 steps 10 in README.md file
        status, address = client_socket.recvfrom(BUFFER_SIZE)


        # TODO: section 2 step 11 in README.md file
        #step 11 below
        # check status and raise exception if failed
        if status == b'failed':
            raise Exception('Transfer failed!')
        else:
            print('Transfer completed!')
    except Exception as e:
        print(f'An error occurred while sending the file: {e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename>')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    send_file(file_name)
