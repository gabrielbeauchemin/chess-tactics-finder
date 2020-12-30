def score_to_string(score):
    if score.is_mate():
        return '#{}'.format(score.relative.moves)
    return str(score.relative.cp)
