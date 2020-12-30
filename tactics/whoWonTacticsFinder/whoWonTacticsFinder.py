import threading
from random import randrange
from typing import List

import chess
import chess.engine
import re

from models.whoWonTacticsModel import WhoWonTacticsModel
from util.saveListToJson import save_list_to_json

engine = chess.engine.SimpleEngine.popen_uci("../stockfish_20090216_x64")

games_found_count = 0
games_found = []
lock = threading.Lock()


def who_win_tactics_finder(games) -> List[WhoWonTacticsModel]:
    tactics_found_count = 0
    tactics_found = []
    for game in games:
        found = who_win_tactic_finder(game)
        if found is not None:
            tactics_found.append(found)
            tactics_found_count = tactics_found_count + 1
            print(tactics_found_count)
            if tactics_found_count % 100 == 0:
                save_list_to_json(tactics_found, 'tactics3.json')
    return tactics_found


def who_win_tactic_finder(game) -> WhoWonTacticsModel or None:
    board = chess.Board()
    skip_first_x_moves = randrange(len(game))
    index_move = 0
    for move in game:
        heuristic = engine.analyse(board, chess.engine.Limit(time=0.3))['score']
        if is_end_move(move):
            break
        board.push_san(move)
        eval_after = engine.analyse(board, chess.engine.Limit(time=0.3))['score']
        if index_move > skip_first_x_moves:
            tactic = find_tactic(heuristic, eval_after, board)
            if tactic is not None:
                return tactic
        index_move = index_move + 1
    return None  # No tactic found for this game


def is_end_move(move):
    return re.match('^(1|0|1/2)-(1|0|1/2)$', move) is not None


def find_tactic(
        score_before: chess.engine.PovScore,
        score_after: chess.engine.PovScore,
        board: chess.Board) -> WhoWonTacticsModel or None:
    try:
        if score_after.is_mate():
            heuristic = '#{}'.format(score_after.relative.moves)
            return WhoWonTacticsModel(board.fen(), heuristic)
        elif score_before.is_mate():  # miss force mate
            return WhoWonTacticsModel(board.fen(), str(score_after.relative.cp))
        heuristic_gap = abs(score_before.relative.cp - score_after.relative.cp)
        if heuristic_gap > 200 and abs(score_after.relative.cp) > 200:  # signification blunder or good move
            return WhoWonTacticsModel(board.fen(), str(score_after.relative.cp))
        return None
    except Exception:
        return None
