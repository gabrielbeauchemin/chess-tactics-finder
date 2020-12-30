class WhoWonTacticsModel:
    def __init__(self, fen, heuristic):
        self.fen = fen
        self.eval = heuristic
