### bad-chess
Chess algorithms which optimize for the worst possible moves. Each engine actively seeks to lose and attempts to force the other to checkmate it. The goal is to find which algorithm is most proficient at losing games. Draws do not count as a loss. Score is calculated as (losses - wins).

Current list:
`randomEngine`: Random moves, baseline engine.
`simpleMaterialEngine`: Calculates a material cost for each legal move.
`simplePieceSquaresEngine`: Uses a piece-squares board to decide moves.
`evalFunctionsEngine`: Takes into account several evalulation functions, including checkmate, material, pawn development, and mobility.
`maximinEngine`: Minimax algorithm with alpha-beta pruning, with some move ordering.
`maximinEvalEngine`: Additional evaluation functions added to previous Minimax algorithm.

To run: `python tester.py <engine1> <engine2> <int number of rounds> <bool verbose>`