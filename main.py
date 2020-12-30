from dataBase.ChessGamesDB import extract_games
from tactics.whoWonTacticsFinder.whoWonTacticsFinder import who_win_tactics_finder


def main():
    games = extract_games(1000)
    who_win_tactics_finder(games)

if __name__ == "__main__":
    main()
