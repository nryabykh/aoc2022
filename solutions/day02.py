from common import get_data


def solve(is_test: bool):
    data = [d.lower().split() for d in get_data(day=2, is_test=is_test)]

    op_turns = {'a': 'rock', 'b': 'paper', 'c': 'scissors'}
    scores_turn = {'rock': 1, 'paper': 2, 'scissors': 3}
    scores_result = {'lose': 0, 'draw': 3, 'win': 6}

    # Part One
    my_turns = {'x': 'rock', 'y': 'paper', 'z': 'scissors'}
    total = 0
    for turn in data:
        op, my = turn
        op, my = op_turns.get(op), my_turns.get(my)
        result = _get_results(op, my)
        total += scores_turn.get(my) + scores_result.get(result)

    print(total)

    # Part Two
    targets = {'x': 'lose', 'y': 'draw', 'z': 'win'}
    total = 0
    for turn in data:
        op, result = turn
        op, result = op_turns.get(op), targets.get(result)
        my = _get_turn_to_result(op, result)
        total += scores_turn.get(my) + scores_result.get(result)

    print(total)


def _get_results(op_turn, my_turn):
    wins = (
        ('rock', 'scissors'),
        ('scissors', 'paper'),
        ('paper', 'rock')
    )

    if op_turn == my_turn:
        return 'draw'

    return 'lose' if (op_turn, my_turn) in wins else 'win'


def _get_turn_to_result(op_turn, result):
    wins = (
        ('rock', 'scissors'),
        ('scissors', 'paper'),
        ('paper', 'rock')
    )

    if result == 'draw':
        return op_turn
    elif result == 'lose':
        return next(my for op, my in wins if op == op_turn)
    else:
        return next(my for my, op in wins if op == op_turn)
