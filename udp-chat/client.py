"""
Client for networked UDP Chat.
Usage: python client.py <host> <port>
"""
import sys
import socket
import threading
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


def receive_messages(client_socket, running):
    while running[0]:
        try:
            client_socket.settimeout(0.5)
            message, _ = client_socket.recvfrom(1024)
            print(message.decode('utf-8'))
        except socket.timeout:
            pass
        except ConnectionResetError:
            print("[!] Connection reset. Server might be down.")
            running[0] = False
            break
        except OSError as e:
            if running[0]:
                print(f"[!] Socket error: {e}")
            break
        except Exception as e:
            if running[0]:
                print(f"[!] Error receiving message: {e}")
            break


if __name__ == "__main__":
    host, port = get_host_port()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', 0))
    running = [True]
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, running))
    receive_thread.daemon = True
    receive_thread.start()
    print(f"[*] UDP Client started, connecting to {host}:{port}")
    print("[*] Type your messages. Type 'exit' to quit.")
    try:
        client_socket.sendto("Connected to the chat".encode('utf-8'), (host, port))
        while True:
            message = input()
            if message.strip().lower() == "exit":
                break
            client_socket.sendto(message.encode('utf-8'), (host, port))
    except (KeyboardInterrupt, EOFError) as e:
        print("\n[*] Interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        running[0] = False
        time.sleep(0.5)
        print("[*] Closing connection...")
        client_socket.sendto("exit".encode('utf-8'), (host, port))
        client_socket.close()
