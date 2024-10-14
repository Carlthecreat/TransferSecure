import socket
import ssl
from cryptography.fernet import Fernet

class TransferSecure:
    '''A class to securely transfer messages and files over a TLS-wrapped TCP connection.'''
    def __init__(self):
        # Setup for for the TLS wrapper for the main socket.
        self.ssl_sock = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_sock.load_cert_chain("cert.pem", "key.pem")    # Placeholders for the certificate and key.

        # Setup for Fernet, to be used for encrypting messages.
        self.key = Fernet.generate_key()
        self.crypt = Fernet(self.key)


    def setup_socket(self):
        '''Setup for the main socket and handles the main server loop. Uses TCP and is wrapped with TLS to ensure privacy and
        security. Keeps the socket open until 'Quit' is received from a connected device or 
        Control + C is pressed.'''
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('192.168.43.174', 44444))
        server_socket.settimeout(5.0)
        with self.ssl_sock.wrap_socket(server_socket, server_side=True) as ssl_wrap_sock:
            ssl_wrap_sock.listen(4)
            while True:
                try:
                    connection, address = ssl_wrap_sock.accept()
                    data = connection.recv(1024)
                    if data:
                        print(address)
                        print(data.decode())
                        if data.lower() == b'quit':
                            break
                    encryption, key = self.encryp_note_sender()
                    if encryption == 'break':
                        break
                    else:
                        connection.send(b'Message received')
                    connection.close()
                except socket.timeout:
                    continue
        return ssl_wrap_sock

    def get_extension(self, filepth: str)->str:
        '''Gets the extension of the path and returns it.'''
        index = filepth.rindex('.')
        return filepth[index:]
    
    def encryp_note_sender(self):
        choice = input("What would you like to do: 'Quit', 'Send Message'.")
        if choice.lower() == 'quit':
            return 'break'
        elif choice.lower() == 'send message':
            encryp_choice = input("Would you like the message to be encrypted? (Y/N) ")
            if encryp_choice.lower() == 'y':
                send_key = input("Would you like to send the key as well? (Y/N) ")
                message = input("What is the message: ").encode()
                encryp_message = self.crypt.encrypt(message)
                if send_key.lower() == 'y':
                    return encryp_message, self.key
                elif send_key.lower() == 'n':
                    return encryp_message
            elif encryp_choice.lower() == 'n':
                message = input("What is the message: ").encode()
                return message

    def split_into_parts(self, filepth: str, new_file_nme: str, num_of_bytes: int=1024)-> str:
        '''Splits a file type into byte chunks using the .txt file type. Takes three arguments:
        1. filepth- The path for the file to be split. Takes string values.
        2. new_file_nme- The prefix for the byte chunk files to be generated. They will take
        the format of 'new_file_nme[num].txt', where [num] is an integer value. The files are
        numbered sequentially, from zero upwards, and [num] represents that value. Takes string values.
        3. num_of_bytes- The size of the file chunsk, in bytes. Takes integer values.'''
        file = open(filepth, 'rb')
        extension = self.get_extension(filepth)
        bytes = file.read(num_of_bytes)

        chunks = 0

        while bytes:
            fileN = open(new_file_nme + str(chunks)+ '.txt', 'wb')
            fileN.write(bytes)         
            fileN.close()

            bytes = file.read(num_of_bytes)
            chunks += 1
        file.close()
        return extension, new_file_nme, chunks

    def reassemble(self, extension: str, file_prefix: str, num_chunks: int, new_file_name: str):
        '''Reassembles file chunks split by split_into_parts(). Takes four arguments:
        1. extension- The file type to be reassembled into. Typically returned from split_into_parts.
        Takes a string value.
        2. file_prefix- The prefix for the chunk files. Typically returned from split_into_parts().
        Takes a strong value.
        3. num_chunks- The number of chunk fies. Typically returned from split_into_parts().
        Takes an integer value.
        4. new_file_name- The name for the reassembled file. Takes a string value.'''
        file = open(new_file_name + extension, 'wb')

        chunks = range(num_chunks)

        for num in chunks:
            fileO = open(file_prefix + str(num) + '.txt', 'rb')
            data = fileO.read(1024)
            file.write(data)
            fileO.close()
        file.close()

try:
    sock = TransferSecure()
    sock.setup_socket()
except KeyboardInterrupt:
    print('Shutting down socket.')
