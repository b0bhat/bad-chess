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

    MOBILITY_WEIGHT = -0.5
    PAWN_STRUCTURE_WEIGHT = -0.8
    CENTER_CONTROL_WEIGHT = -0.8
    DEVELOPMENT_WEIGHT = -0.6
    THREATS_WEIGHT = -0.8

    def evaluate_board(self, board):
        score = 0
        score += self.evaluate_material(self, board)
        score += self.evaluate_mobility(self, board)
        score += self.evaluate_pawn_structure(self, board)
        score += self.evaluate_center_control(self, board)
        score += self.evaluate_checkmate(self, board)
        return score

    def evaluate_material(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == board.turn:
                    score += self.PIECE_VALUES[piece.piece_type]
                else:
                    score -= self.PIECE_VALUES[piece.piece_type]
        return score

    def evaluate_mobility(self, board):
        player_mobility = len(list(board.legal_moves))
        board.turn = not board.turn
        opponent_mobility = len(list(board.legal_moves))
        board.turn = not board.turn
        return self.MOBILITY_WEIGHT * (opponent_mobility - player_mobility)
    
    def evaluate_checkmate(self, board):
        if board.is_checkmate():
            if board.turn == board.result():
                return float('inf')
            else:
                return float('-inf')
        return 0

    def evaluate_pawn_structure(self, board):
        score = 0
        player_color = board.turn
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.PAWN:
                if piece.color == player_color:
                    score -= 1
                else:
                    score += 1
        return self.PAWN_STRUCTURE_WEIGHT * score

    def evaluate_center_control(self, board):
        score = 0
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == board.turn:
                    score -= 1
                else:
                    score += 1
        return self.CENTER_CONTROL_WEIGHT * score

    def play(self, board):
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        worst_move = None
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = self.evaluate_board(board)
            if eval < min_eval:
                min_eval = eval
                worst_move = move
            board.pop()
        return worst_move
