from dataBase.ChessGamesDB import extract_games
from tactics.drawTacticsFinder.drawTacticsFinder import draw_tactics_finder
from util.saveListToJson import save_list_to_json


def main():
    games = extract_games(50000)
    tactics = draw_tactics_finder(games)
    save_list_to_json(tactics, "tactics.json")


if __name__ == "__main__":
    main()
