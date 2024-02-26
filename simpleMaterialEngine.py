import random
import chess

class Engine:
   
    def evaluate_board(self, board):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 100
        }
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    score += piece_values[piece.piece_type]
                else:
                    score -= piece_values[piece.piece_type]

        return score
    
    def play(self, board):
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        best_move = None
        best_value = float('-inf')
        for move in legal_moves:
            board.push(move)
            value = self.evaluate_board(board)
            if value > best_value:
                best_value = value
                best_move = move
            board.pop()
        return best_move