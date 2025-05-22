"""
Tic-Tac-Toe class.
"""
class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current = 'X'

    def make_move(self, pos):
        if 0 <= pos < 9 and self.board[pos] == ' ':
            self.board[pos] = self.current
            return True
        return False

    @staticmethod
    def ask_for_move(game):
        while True:
            try:
                move_input = input(
                    f"Your move ({game.current}). Enter row and column (0-2), separated by a space: "
                )
                row_col = move_input.strip().split()
                if len(row_col) != 2:
                    print("Please enter two numbers separated by a space (e.g., '1 2').")
                    continue
                row, col = map(int, row_col)
                if not (0 <= row <= 2 and 0 <= col <= 2):
                    print("Row and column must be between 0 and 2.")
                    continue
                pos = row * 3 + col
                if game.board[pos] != ' ':
                    print("Cell already taken, try another move.")
                    continue
                return pos
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space (e.g., '1 2').")

    def switch(self):
        self.current = 'O' if self.current == 'X' else 'X'

    def winner(self):
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        if ' ' not in self.board:
            return 'Draw'
        return None

    def __str__(self):
        b = self.board
        display = "   0   1   2\n"
        for i in range(3):
            row = f"{i}  {b[i*3]} | {b[i*3+1]} | {b[i*3+2]}"
            display += row + "\n"
            if i < 2:
                display += "  ---+---+---\n"
        return display