import chess
import chess.pgn


def get_checks(fen):
    checks = []
    ck_board = chess.Board(fen)
    if not ck_board.is_check():
        for move in ck_board.legal_moves:
            board1 = chess.Board(fen)
            board1.push(move)
            if board1.is_check():
                checks.append(ck_board.san(move))
    return checks


# TODO Modify to use [board.san(capture) for capture in board.generate_legal_captures()]
def get_captures(fen):
    captures = []
    cap_board = chess.Board(fen)
    for move in cap_board.legal_moves:
        if cap_board.is_capture(move):
            captures.append(cap_board.san(move))
    return captures


def get_opp_threats(fen):
    opp_threats = []
    opp_board = chess.Board(fen)
    in_check = opp_board.is_check()
    opp_board.push(chess.Move.null())
    if not in_check:
        opp_threats.extend(get_checks(opp_board.fen()))
    captures = get_captures(opp_board.fen())
    for capture in captures:
        if capture not in opp_threats:
            opp_threats.append(capture)
    return opp_threats


# path = r'C:\Users\sfstr\OneDrive - The University of Memphis\Etc\Chess'
# fname = r'\KramnikFirouzja_Rapid2019.txt'
path = r'C:\Users\sfstr\lichess'
fname = r'\lichess_db_standard_rated_2013-01.pgn'
pgn = open(path + fname)

game = chess.pgn.read_game(pgn)
game_num = 1
cct_fens = []
while game is not None:
    board = game.board()
    for mov in game.mainline_moves():
        board.push(mov)
        FEN = board.fen()
        if FEN.count("Q") > 1 or FEN.count("q") > 1:
            continue
        Checks = get_checks(FEN)
        pChecks = {s[0] if s[0] in "QKRNB" else "P" for s in Checks}
        Captures = [c for c in get_captures(FEN) if c not in Checks]
        pCaps = {s[0] if s[0] in "QKRNB" else "P" for s in Captures}
        pieces = pCaps.union(pChecks)
        ccts = len(Checks) + len(Captures)
        if ccts >= 12 and len(pieces) >= 4:
            cct_fens.append(FEN)
            break
    # if len(cct_fens) > 100:
    #     break
    game = chess.pgn.read_game(pgn)
    game_num += 1

    if game_num > 5000:
        break

with open(path + r'\ccts_2.txt', "w") as f:
    for item in cct_fens:
        f.write("%s\n" % item)
