# DeCloud

DeCloud is a revolutionary project that aims to democratize computing resources by connecting unused personal computers and computational units into a network of servers. This project is designed to empower diversity and sustainability in the world of computing. It is divided into two main components:

1. Server (Node 1): Codes for the Server Software
2. Proxy (Node 2): Codes for the Client Web Application and Communication between Server and Proxy

## Server (Node 1)

The Server component of DeCloud is responsible for managing the unused computers or computational units that users can rent to other clients when they're not using them. By installing the server app, individuals can register their devices into the DeCloud network and rent their computational units to others. The server app downloads Docker files from clients, sets them up on the server, and makes the server available to the public internet through a proxy server.

### Technologies Used

- Python
- Requests Library
- Docker Library
- Docker Engine (Docker Desktop for Windows)
- (Additional libraries/platforms for future development)

### Features

- Installing Docker Engine and its requirements
- Downloading and running Docker files from the proxy server (Node 2)
- Keeping the connection alive with the proxy server (Node 2)
- Graphical User Interface (GUI) for registration, login, and managing the renting service

## Proxy (Node 2)

The Proxy component acts as a gateway between clients and servers, connecting them and ensuring secure communication. It runs a web application to receive Docker files from clients and distribute them among available servers. The proxy also serves as a reverse tunneling system, enhancing security and privacy by anonymizing the location, IP address, and identity of the servers.

### Technologies Used

- Python
- Taipy Library
- Flask Library
- (Additional libraries/platforms for future development)

### Features

- Logging of all servers (Node 1)
- Receiving Docker files from clients (Node 3)
- Sending Docker files to the servers (Node 1)
- Redirecting clients to their server's IP address
- (Additional features for future development)

## Getting Started


