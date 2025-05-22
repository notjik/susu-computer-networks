"""
Server for networked UDP Chat.
Usage: python server.py <host> <port>
"""
import sys
import socket
import time


def get_host_port():
    host = '127.0.0.1'
    port = 12345
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number, using default 12345.")
    return host, port


if __name__ == "__main__":
    host, port = get_host_port()
    buffer_size = 1024
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.settimeout(0.5)
    print(f"[*] UDP Server started on {host}:{port}")
    clients = {}
    try:
        while True:
            try:
                message, client_address = server_socket.recvfrom(buffer_size)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                message_str = message.decode('utf-8')
                if client_address not in clients:
                    clients[client_address] = current_time
                    print(f"[+] New client connected: {client_address}, Total clients: {len(clients)}")
                print(f"[{current_time}] {client_address}: {message_str}")
                if message_str.strip().lower() == "exit":
                    if client_address in clients:
                        del clients[client_address]
                        print(f"[-] Client disconnected: {client_address}, Total clients: {len(clients)}")
                    continue
                formatted_message = f"[{client_address[0]}:{client_address[1]}]: {message_str}"
                clients_copy = clients.copy()
                for client in clients_copy:
                    try:
                        server_socket.sendto(formatted_message.encode('utf-8'), client)
                    except Exception as e:
                        print(f"[!] Error sending to {client}: {e}")
                        clients.pop(client)
            except ConnectionResetError as e:
                print(f"[!] Connection reset: {e}")
            except socket.timeout:
                pass
            except OSError as e:
                print(f"[!] Socket error: {e}")
            except Exception as e:
                print(f"[!] Unexpected error: {e}")
    except (KeyboardInterrupt, EOFError) as e:
        print("\n[*] Server shutting down...")
    finally:
        server_socket.close()
        print("[*] Server closed")
