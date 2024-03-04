import random

class Engine:
    def play(self, board):
        return random.choice(list(board.legal_moves))
