import random
import chess

class Engine:
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 100
    }

    MOBILITY_WEIGHT = -0.1  # Changed to negative
    PAWN_STRUCTURE_WEIGHT = -0.2  # Changed to negative
    CENTER_CONTROL_WEIGHT = -0.2  # Changed to negative
    KING_SAFETY_WEIGHT = -0.15  # Changed to negative
    DEVELOPMENT_WEIGHT = -0.15  # Changed to negative
    THREATS_WEIGHT = -0.2  # Changed to negative

    def evaluate_board(self, board):
        score = 0
        score += self.evaluate_material(board)
        score += self.evaluate_mobility(board)
        score += self.evaluate_pawn_structure(board)
        score += self.evaluate_center_control(board)
        return score

    def evaluate_material(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    score -= self.PIECE_VALUES[piece.piece_type]  # Changed to negative
                else:
                    score += self.PIECE_VALUES[piece.piece_type]  # Changed to negative
        return score

    def evaluate_mobility(self, board):
        white_mobility = len(list(board.legal_moves))
        board.turn = not board.turn  # switch to opponent's turn
        black_mobility = len(list(board.legal_moves))
        board.turn = not board.turn  # switch back
        return self.MOBILITY_WEIGHT * (black_mobility - white_mobility)  # Changed the order and sign

    def evaluate_pawn_structure(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    score -= 1  # Changed to negative
                else:
                    score += 1  # Changed to negative
        return self.PAWN_STRUCTURE_WEIGHT * score

    def evaluate_center_control(self, board):
        score = 0
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    score -= 1  # Changed to negative
                else:
                    score += 1  # Changed to negative
        return self.CENTER_CONTROL_WEIGHT * score

    def play(self, board):
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        worst_move = None
        worst_value = float('inf')
        for move in legal_moves:
            board.push(move)
            value = self.evaluate_board(board)
            if value < worst_value:
                worst_value = value
                worst_move = move
            board.pop()
        return worst_move


