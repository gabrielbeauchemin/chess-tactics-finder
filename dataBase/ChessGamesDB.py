import re


def extract_games(max_games, min_elo=0, offset=0):
    games = []
    nbr_games = 0
    curr_game_header = {}

    with open("lichess_db_standard.pgn", "r", encoding="utf8") as fp:
        line = fp.readline()
        index_game = 0
        while line:
            game_header = re.match('\\[.*?\\]', line)
            if game_header:
                header_split = game_header.group().replace('[', '').replace(']', '').split(' "')
                if 'Event' in header_split[0]:
                    curr_game_header = {}
                curr_game_header[header_split[0].strip()] = header_split[1].replace('"', '').strip()
            elif '1.' in line:
                index_game = index_game + 1
                if int(curr_game_header['WhiteElo']) > min_elo and int(
                        curr_game_header['BlackElo']) > min_elo and index_game > offset:
                    line = re.sub('[0-9]+\.\.\.', '', line)  # some move has this other format 1.{move} 1... {move}
                    line = re.sub('{.*?}', '', line).strip()  # remove moves annotation
                    line = line.replace('?', '').replace('!', '')
                    moves = re.compile("[0-9]+\.").split(line)
                    single_moves = []
                    for move in moves:
                        move = move.strip()
                        if move == '': continue
                        split_move = move.split(' ')
                        for s in split_move:
                            if s != '':
                                single_moves.append(s)
                    games.append(single_moves)
                    nbr_games = nbr_games + 1
            if nbr_games >= max_games:
                break
            line = fp.readline()
    return games
