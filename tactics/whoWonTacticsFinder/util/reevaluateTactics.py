import json
import chess
import chess.engine

from models.whoWonTacticsModel import WhoWonTacticsModel
from util.scoreToString import score_to_string

engine = chess.engine.SimpleEngine.popen_uci("./stockfish_20090216_x64")


def reevaluate_tactics(file_path):
    new_tactics = []
    with open(file_path) as json_file:
        json_tactics = json.load(json_file)
        for tactic in json_tactics:
            print(len(new_tactics)
                  , " done.")
            board = chess.Board(tactic["fen"])
            new_score = engine.analyse(board, chess.engine.Limit(time=1))['score']
            new_score_str = score_to_string(new_score)
            new_tactics.append(WhoWonTacticsModel(board.fen(), new_score_str))
    return new_tactics
