"""
Server for networked Tic-Tac-Toe (one-on-one) over TCP.
Usage: python server.py <host> <port>
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


if __name__ == '__main__':
    host, port = get_host_port()
    game = TicTacToe()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    print(f"Server listening on {host}:{port}")
    conn, addr = sock.accept()
    print(f"Connected by {addr}")
    conn.sendall(b"WELCOME You are O\n")
    print("You are X. Opponent is O.\n")
    print(game)
    try:
        while True:
            # X move (Server)
            pos = TicTacToe.ask_for_move(game)
            game.make_move(pos)
            conn.sendall(f"MOVE {pos}\n".encode())
            print(game)
            winner = game.winner()
            if winner:
                print(f"Game over: {winner}")
                conn.sendall(f"END {winner}\n".encode())
                break
            game.switch()

            # O move (Client)
            data = conn.recv(1024).decode().strip()
            if not data:
                print("Connection lost.")
                break

            if data.startswith("MOVE"):
                _, pos = data.split()
                pos = int(pos)
                game.make_move(pos)
                print(f"Opponent (O) moved to position {pos}")
                print(game)
                winner = game.winner()
                if winner:
                    print(f"Game over: {winner}")
                    conn.sendall(f"END {winner}\n".encode())
                    break

                game.switch()
            elif data.startswith("END"):
                _, winner = data.split()
                print(game)
                print(f"Game over: {winner}")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
