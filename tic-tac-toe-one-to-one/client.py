"""
Client for networked Tic-Tac-Toe over TCP.
Usage: python client.py <host> <port>
"""
import socket
import sys

from tic_tac_toe import TicTacToe


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


def receive_data(sock):
    try:
        return sock.recv(1024).decode()
    except Exception as e:
        print(f"Connection error: {e}")
        return ""


def main():
    host, port = get_host_port()
    game = TicTacToe()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((host, port))
            except Exception as e:
                print(f"Could not connect to server: {e}")
                return
            welcome = receive_data(sock)
            if welcome:
                print(welcome.strip())
            print("You are O. Opponent is X.\n")
            print(game)
            while True:
                data = receive_data(sock).strip()
                if not data:
                    print("Connection lost.")
                    break
                if data.startswith("MOVE"):
                    _, pos = data.split()
                    pos = int(pos)
                    game.make_move(pos)
                    print(f"Opponent (X) moved to position {pos}")
                    print(game)
                    winner = game.winner()
                    if winner:
                        print(f"Game over: {winner}")
                        break
                    game.switch()
                elif data.startswith("END"):
                    _, winner = data.split()
                    print(game)
                    print(f"Game over: {winner}")
                    break
                pos = TicTacToe.ask_for_move(game)
                game.make_move(pos)
                sock.sendall(f"MOVE {pos}\n".encode())
                print(game)
                winner = game.winner()
                if winner:
                    print(f"Game over: {winner}")
                    sock.sendall(f"END {winner}\n".encode())
                    break
                game.switch()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
