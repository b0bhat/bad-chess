import chess
import importlib.util
import sys
import asyncio
import concurrent.futures
import time
import multiprocessing

def load_engine(engine_file):
    spec = importlib.util.spec_from_file_location("engine", engine_file)
    engine_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine_module)
    return engine_module.Engine

def material_balance(board):
    white = board.occupied_co[chess.WHITE]
    black = board.occupied_co[chess.BLACK]
    return (
        chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
        3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
        3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
        5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
        9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
    )

def play_game(engine_file1, engine_file2):
    engine_class1 = load_engine(engine_file1)
    engine_class2 = load_engine(engine_file2)
    engine1 = engine_class1()
    engine2 = engine_class2()
    board = chess.Board()
    engines = [engine1, engine2]
    engine_scores = [0, 0]
    moves = 0
    
    while not board.is_game_over():
        turn = board.turn
        move = engines[int(turn)].play(board)
        board.push(move)
        moves += 1
        
        if board.is_fivefold_repetition():
            print("Game Over: Draw by fivefold repetition.")
            break
        elif board.is_insufficient_material():
            print("Game Over: Draw due to insufficient material.")
            break
        elif board.is_seventyfive_moves():
            print("Game Over: Draw by seventy-five moves rule.")
            break
        elif board.is_checkmate():
            winner = int(not turn)
            engine_scores[winner] += 1
            print(f"Game Over: {engine_file1 if winner == 0 else engine_file2} wins in {moves} moves.")
            break
        elif board.is_stalemate():
            print(f"Game Over: Draw by stalemate in {moves} moves.")
            break

    material_difference = material_balance(board)
    print(f"Game Over: Game ended in {moves} moves with {material_difference} difference")
    return engine_scores

async def run_games(engine_file1, engine_file2, num_games):
    total_scores = [0, 0]  # Total scores for engine1 and engine2
    game_args = [(engine_file1, engine_file2) for _ in range(num_games)]
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(executor, map, play_game, *zip(*game_args))
        for scores in results:
            total_scores[0] += scores[0]
            total_scores[1] += scores[1]

    print(f"Total scores for {engine_file1}: {total_scores[0]}")
    print(f"Total scores for {engine_file2}: {total_scores[1]}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tester.py <engine1.py> <engine2.py> [num_games]")
        sys.exit(1)
    
    engine_file1 = sys.argv[1]
    engine_file2 = sys.argv[2]
    num_games = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
    
    start_time = time.time()
    asyncio.run(run_games(engine_file1, engine_file2, num_games))
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds.")
