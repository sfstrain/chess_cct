import chess

# starting FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# board.attacks(sq) -- gives SquareSet of all squares that attack sq
# board.is_attacked_by(col, sq) -- checks if col attacks sq
# board.attackers(col, sq) -- gives SquareSet of col's attackers of sq
# board.is_pinned(col, sq) -- checks if col's piece on sq is absolutely pinned
# board.pin(col, sq) -- returns SquareSet that masks rank, file or diagonal of pin
# board.is_capture(move) -- checks if move is a capture
# board.is_checkmate() -- checks if current position is checkmate
# board.is_check() -- checks if side to move is in check
# board.gives_check(move) -- checks if move puts opponent in check
# board.checkers() -- gives SquareSet of pieces currently giving check

# board.parse_san(san) -- gives Move on board that corresponds to san, ValueError if not legal or ambiguous


def get_checks(fen):
    checks = []
    board = chess.Board(fen)
    if not board.is_check():
        for mv in board.legal_moves:
            board1 = chess.Board(fen)
            board1.push(mv)
            if board1.is_check():
                checks.append(board.san(mv))
    return sorted(checks)


def get_captures(fen):
    captures = []
    board = chess.Board(fen)
    for mv in board.legal_moves:
        if board.is_capture(mv):
            captures.append(board.san(mv))
    return sorted(captures)


def get_opp_threats(fen):
    opp_threats = []
    board = chess.Board(fen)
    in_check = board.is_check()
    board.push(chess.Move.null())
    if not in_check:
        opp_threats.extend(get_checks(board.fen()))
    captures = get_captures(board.fen())
    for capture in captures:
        if capture not in opp_threats:
            opp_threats.append(capture)
    return opp_threats


def get_pieces(fen):
    board = chess.Board(fen)
    pieces = []
    pmap = board.piece_map()
    for sq, piece in pmap.items():
        pieces.append(piece.symbol() + chess.square_name(sq))
    return sorted(pieces)


def piece_loc(piece):
    return piece[1:]


def get_new_threats(fen, mv):
    board = chess.Board(fen)
    old_threats = get_checks(fen)
    old_threats.extend(get_captures(fen))
    old_threats = set(old_threats)
    n_threats = []  # new_threats
    board.push(mv)
    for threat in get_opp_threats(board.fen()):
        if threat not in old_threats and threat[0:-1] not in old_threats and threat not in n_threats:
            n_threats.append(threat)
    return n_threats


def clean(dirty, k):
    cleaned = []
    for nt in dirty:
        if nt[-1] == '+' or nt[-1] == '#':
            nt = nt[0:-1]
        if nt[-2:] != k:
            cleaned.append(nt)
    return cleaned


# FEN = "2r2r1k/p6p/6p1/2Q5/4Rn2/8/Pq3PPP/2R2BK1 w - - 0 1"
FEN = input("Enter the FEN: ")
# board = chess.Board(fen)

# moves = [board.uci(m) for m in board.legal_moves]
# player = board.turn
# opponent = not player
#
# oppKing = board.king(opponent)

Checks = get_checks(FEN)
Captures = [ c for c in get_captures(FEN) if c not in Checks ]
OppThreats = get_opp_threats(FEN)
OppChecks = [ o for o in OppThreats if o.endswith("+")]
OppCaptures = [o for o in OppThreats if not o.endswith("+")]


Board = chess.Board(FEN)
Threats = {}
for move in Board.legal_moves:
    new_threats = get_new_threats(FEN, move)
    smove = Board.san(move)
    if len(new_threats):
        if smove[-1] == '+':
            king = chess.square_name(Board.king(not Board.turn))
            new_threats = clean(new_threats, king)
        Threats[smove] = new_threats

print("Checks: " + ", ".join(Checks))
print("Captures: " + ", ".join(Captures))
print("Opponent checks: " + ", ".join(OppChecks))
print("Opponent captures: " + ", ".join(OppCaptures))
