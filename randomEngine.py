import random
import chess

class Engine:
    def play(self, board):
        legal_moves = list(board.legal_moves)
        random_move = random.choice(legal_moves)
        return random_move
