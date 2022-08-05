import stockfish
import chess

LEVEL = 14
PATH = r"C:\Users\sfstr\Downloads\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe"

FEN = "4k2r/3bb2p/3p1p2/1p1Pp1p1/2p1Q1P1/q3P2P/3KN3/rB1R1R2 b k - 5 29"

fish = stockfish.Stockfish(path=PATH, depth=LEVEL)
board = chess.Board(FEN)
moves = [m for m in board.legal_moves]
evals = {}

for move in moves:
    board1 = chess.Board(FEN)
    board1.push(move)
    fen = board1.fen()
    fish.set_fen_position(board1.fen())
    eval = fish.get_evaluation()
    if eval["type"] == "mate":
        evals[board.san(move)] = f"M{abs(eval['value'])}"
    else:
        evals[board.san(move)] = f"{eval['value']/100}"