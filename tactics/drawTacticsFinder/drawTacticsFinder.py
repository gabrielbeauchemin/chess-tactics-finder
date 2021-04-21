import threading
from typing import List

import chess
import chess.engine
import re

from models.drawTacticsModel import DrawTacticsModel
from util.saveListToJson import save_list_to_json

engine = chess.engine.SimpleEngine.popen_uci("./tactics/stockfish_20090216_x64")

games_found_count = 0
games_found = []
lock = threading.Lock()


def draw_tactics_finder(games) -> List[DrawTacticsModel]:
    tactics_found_count = 0
    tactics_found = []
    for game in games:
        found = draw_tactic_finder(game)
        if found is not None:
            tactics_found.append(found)
            tactics_found_count = tactics_found_count + 1
            save_list_to_json(tactics_found, 'tactics3.json')
    return tactics_found


def draw_tactic_finder(game) -> DrawTacticsModel or None:
    board = chess.Board()
    skip_first_x_moves = 0.66666 * len(game)
    index_move = 0
    for move in game:
        if is_end_move(move):
            break
        board.push_san(move)
        evaluation = engine.analyse(board, chess.engine.Limit(time=0.1))['score']
        if index_move > skip_first_x_moves:
            tactic = find_tactic(evaluation, board)
            if tactic is not None:
                return tactic
        index_move = index_move + 1
    return None  # No tactic found for this game


def is_end_move(move):
    return re.match('^(1|0|1/2)-(1|0|1/2)$', move) is not None


def find_tactic(
        score: chess.engine.PovScore,
        board: chess.Board) -> DrawTacticsModel or None:
    try:
        if score.is_mate():
            return None
        if score.relative.cp == 0:
            return DrawTacticsModel(board.fen())
        return None
    except Exception:
        return None
