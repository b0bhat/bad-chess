import chess
import evalFunctionsEngine
import random

class Engine:
    def __init__(self, depth=5):
        self.depth = depth
        self.transposition_table = {}
        self.visited_positions = set()
        self.killer_moves = [[None for _ in range(2)] for _ in range(depth)]
    
    def alpha_beta(self, board, depth, alpha, beta, minimizing_player):
        if depth == 0 or board.is_game_over():
            return evalFunctionsEngine.Engine.evaluate_board(evalFunctionsEngine.Engine, board)

        key = board.fen()
        if key in self.transposition_table:
            return self.transposition_table[key]

        legal_moves = list(board.legal_moves)

        if self.killer_moves[depth]:
            legal_moves = [move for move in self.killer_moves[depth] if move in legal_moves] + legal_moves

        if minimizing_player:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = min_eval

            if min_eval < beta:
                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                self.killer_moves[depth][0] = legal_moves[0]

            return min_eval
        else:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = max_eval

            # Update killer moves
            if max_eval > alpha:
                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                self.killer_moves[depth][0] = legal_moves[0]

            return max_eval


    def play(self, board):
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        ordered_moves = self.order_moves(board, legal_moves)
        worst_move = None  
        worst_eval = float('inf')  
        alpha = float('inf')
        beta = float('-inf')
        for move in ordered_moves:
            board.push(move)
            if board.fen() not in self.visited_positions and not board.is_fivefold_repetition():  
                eval = self.alpha_beta(board, self.depth - 1, alpha, beta, True)
                if eval < worst_eval:  
                    worst_eval = eval
                    worst_move = move
                alpha = max(alpha, eval)
            board.pop()
        if worst_move is None:
            return legal_moves[0] if legal_moves else None
        self.visited_positions.add(board.fen())  
        return worst_move

    def order_moves(self, board, moves):
        ordered_moves = []
        for move in moves:
            if board.is_capture(move):
                ordered_moves.insert(0, move)
            elif board.piece_at(move.from_square).piece_type == chess.PAWN:
                ordered_moves.append(move)
            else:
                ordered_moves.insert(1, move)
        return ordered_moves
