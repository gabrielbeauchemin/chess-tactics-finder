import json
import chess
import chess.engine
from models.drawTacticsModel import DrawTacticsModel

engine = chess.engine.SimpleEngine.popen_uci("./stockfish_20090216_x64")


def reevaluate_tactics(file_path):
    new_tactics = []
    with open(file_path) as json_file:
        json_tactics = json.load(json_file)
        for tactic in json_tactics:
            print(len(new_tactics)
                  , " done.")
            board = chess.Board(tactic["fen"])
            score = engine.analyse(board, chess.engine.Limit(time=1))['score']
            if score.is_mate() is False and score.relative.cp == 0:
                new_tactics.append(DrawTacticsModel(board.fen()))
    return new_tactics
