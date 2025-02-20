import math
from kivy.app import App
from gui import TicTacToeGUI

class TicTacToeGame:
    def __init__(self):
        self.board_size = 3
        self.current_player = "X"
        self.board = None
        self.reset_game(self.board_size)

    def reset_game(self, size):
        """Resets the game board."""
        self.board_size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.current_player = "X"

    def make_move(self, row, col):
        """Processes a player's move if valid."""
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            return True
        return False

    def switch_player(self):
        """Switches turns between X and O."""
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Checks for a winning condition dynamically based on board size."""
        win_count = self.board_size  

        # Check rows
        for row in self.board:
            if row.count(self.current_player) == win_count:
                return True

        # Check columns
        for col in range(self.board_size):
            if all(self.board[row][col] == self.current_player for row in range(self.board_size)):
                return True

        # Check main diagonal
        if all(self.board[i][i] == self.current_player for i in range(self.board_size)):
            return True

        # Check anti-diagonal
        if all(self.board[i][self.board_size - 1 - i] == self.current_player for i in range(self.board_size)):
            return True

        return False

    def is_draw(self):
        """Checks if the game is a draw."""
        return all(self.board[row][col] != "" for row in range(self.board_size) for col in range(self.board_size))

    def evaluate(self):
        """Evaluates the board: +10 for AI win, -10 for player win, 0 for draw."""
        if self.check_winner():
            return 10 if self.current_player == "O" else -10
        return 0

    def get_empty_cells(self):
        """Returns a list of available cells."""
        return [(row, col) for row in range(self.board_size) for col in range(self.board_size) if self.board[row][col] == ""]

    def get_best_move(self):
        """Finds the best move for 3x3 using an improved Minimax approach, keeping larger boards unchanged."""
        if self.board_size == 3:
            return self.get_best_move_3x3()
        return self.get_best_move_generic()

    def get_best_move_3x3(self):
        """Optimized AI for 3x3 board with strategic prioritization."""
        # 1. Check for winning move
        for row, col in self.get_empty_cells():
            self.board[row][col] = "O"
            if self.check_winner():
                self.board[row][col] = ""
                return row, col  # Play the winning move
            self.board[row][col] = ""

        # 2. Check for blocking move
        self.switch_player()
        for row, col in self.get_empty_cells():
            self.board[row][col] = "X"
            if self.check_winner():
                self.board[row][col] = ""
                self.switch_player()
                return row, col  # Block the opponent
            self.board[row][col] = ""
        self.switch_player()

        # 3. Prioritize center, then corners, then edges
        priority_moves = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]
        for move in priority_moves:
            if move in self.get_empty_cells():
                return move

        # 4. Fallback to Minimax
        return self.get_best_move_generic()

    def get_best_move_generic(self):
        """Finds the best move using Minimax with depth control for larger boards."""
        best_val = -math.inf
        best_move = (-1, -1)

        empty_cells = self.get_empty_cells()
        moves_left = len(empty_cells)

        # 🚀 Adaptive depth control
        if self.board_size == 3:
            max_depth = 6  # Full depth
        elif self.board_size == 4:
            max_depth = 4 if moves_left > 8 else 6  # Early game = 4, Late game = 6
        elif self.board_size == 5:
            max_depth = 3 if moves_left > 12 else 5  # Early game = 3, Late game = 5

        for row, col in empty_cells:
            self.board[row][col] = "O"
            move_val = self.minimax(0, False, -math.inf, math.inf, max_depth)
            self.board[row][col] = ""

            if move_val > best_val:
                best_move = (row, col)
                best_val = move_val

        return best_move if best_move != (-1, -1) else empty_cells[0]

    def minimax(self, depth, is_maximizing, alpha, beta, max_depth):
        """Minimax algorithm with depth limit & Alpha-Beta Pruning."""
        score = self.evaluate()

        if score == 10:  # AI Wins
            return score - depth
        if score == -10:  # Player Wins
            return score + depth
        if self.is_draw():  # Draw
            return 0
        if depth >= max_depth:  # Stop searching deeper
            return 0  

        if is_maximizing:
            best = -math.inf
            for row, col in self.get_empty_cells():
                self.board[row][col] = "O"
                best = max(best, self.minimax(depth + 1, False, alpha, beta, max_depth))
                self.board[row][col] = ""
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = math.inf
            for row, col in self.get_empty_cells():
                self.board[row][col] = "X"
                best = min(best, self.minimax(depth + 1, True, alpha, beta, max_depth))
                self.board[row][col] = ""
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

class TicTacToeApp(App):
    def build(self):
        self.game_controller = TicTacToeGame()
        return TicTacToeGUI(self.game_controller)

if __name__ == "__main__":
    TicTacToeApp().run()
