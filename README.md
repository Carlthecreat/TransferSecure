# TransferSecure

TransferSecure is a Python-based utility designed for securely transferring messages and files over a TCP connection, wrapped with Transport Layer Security (TLS). This tool leverages the `ssl` library for secure socket communication and the `cryptography` library's `Fernet` encryption for message encryption.

## Features

* **TLS Secure Communication**: Establishes a secure connection between the server and client using TLS.
* **Message Encryption**: Provides an option to encrypt messages using Fernet encryption.
* **File Splitting and Reassembly**: Ability to split large files into chunks and reassemble them later.
* **Custom Key Exchange**: Optionally send an encryption key along with the message for secure decryption on the recipient side.

## Requirements

* Python 3.6+
* `cryptography` library (`pip install cryptography`)
* SSL certificates (`cert.pem` and `key.pem`)

## Setup

Before using TransferSecure, you must have SSL certificates (`cert.pem` and `key.pem`). You can generate these certificates using OpenSSL:

```bash
openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes
```

Install the required libraries:

```bash
pip install cryptography
```

## How To Use
### 1. Running the Server
To run the server:
```python
try:
    sock = TransferSecure()
    sock.setup_socket()
except KeyboardInterrupt:
    print('Shutting down socket.')
```

This will start a TLS-wrapped TCP server that listens for incoming connections on the specified IP and port (default is 192.168.43.174:44444). The server will stay active until it receives the command 'quit' or you terminate it with Ctrl + C.

### 2. Sending Encrypted Messages
The server allows you to send messages with optional encryption. During message transmission, you can:

* Choose to encrypt the message (Y/N).
* Optionally send the encryption key along with the encrypted message.

The server prints any received messages and confirms receipt.

### 3. File Splitting
The split_into_parts method allows you to split large files into smaller chunks. The chunks are saved as .txt files and numbered sequentially.

```python
extension, file_prefix, chunks = split_into_parts('file_path', 'prefix', num_of_bytes=1024)
```

### 4. File Reassembly
The reassemble method takes the file chunks and reassembles them into their original form.

```python
reassemble(extension, file_prefix, num_chunks, new_file_name)
```

## Methods
* setup_socket(): Sets up the server socket and wraps it with TLS for secure communication.

* encryp_note_sender(): Handles message input, encryption options, and sending.

* split_into_parts(filepth, new_file_nme, num_of_bytes): Splits a file into byte chunks.

* reassemble(extension, file_prefix, num_chunks, new_file_name): Reassembles a file from its chunks.

## Error Handling
* A KeyboardInterrupt gracefully shuts down the server.

* The server handles socket timeouts and continues listening for connections.

## Future Enhancements
* Client Implementation: A client-side implementation for sending and receiving messages.

* Multi-Client Handling: Support for concurrent client connections.

* Authentication: Adding authentication for enhanced security during communication.

## License
This project is licensed under the MIT License.