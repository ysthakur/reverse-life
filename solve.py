from z3 import *

board = [
    [1],
    [1],
    [1],
]

curr_vars = [
    [Bool(f"c[{i}][{j}]") for j in range(len(board[0]))] for i in range(len(board))
]

prev_vars = [
    [Bool(f"p[{i}][{j}]") for j in range(len(board[0]) + 2)]
    for i in range(len(board) + 2)
]


def constrain_bools(bools, min, max):
    """
    Returns a constraint that at least `min` and at most `max` of the given variables are true (inclusive)
    """

    def helper(bools, min, max, acc):
        if len(bools) == 0:
            if min > 0:
                return []
            else:
                return acc
        true = [constraints + [bools[0]] for constraints in acc]
        false = [constraints + [Not(bools[0])] for constraints in acc]
        if max == 0:
            return helper(bools[1:], min, 0, false)
        return [
            *helper(bools[1:], min - 1, max - 1, true),
            *helper(bools[1:], min, max, false),
        ]

    constraints = helper(bools, min, max, [[]])
    constraint = Or(*[And(bools) for bools in constraints])
    print(constraint)
    return constraint


def constraints_at(r, c):
    """Get constraints for curr_vars[r][c]"""
    prev = prev_vars[r + 1][c + 1]

    # Neighbors of prev_vars[r + 1][c + 1]
    neighbors = [
        prev_vars[r + 1][c],
        prev_vars[r + 1][c + 2],
        *prev_vars[r][c : c + 3],
        *prev_vars[r + 2][c : c + 3],
    ]
    print(neighbors)

    exactly_two = constrain_bools(neighbors, 2, 2)
    exactly_three = constrain_bools(neighbors, 3, 3)

    print("e")

    alive = Or(And(prev, exactly_two), exactly_three)

    if board[r][c]:
        return alive
    else:
        return Not(alive)


constraints = [
    constraints_at(r, c) for c in range(len(board[0])) for r in range(len(board))
]
s = Solver()
s.add(*constraints)
s.check()
model = s.model()
print(
    "\n".join(
        " ".join(
            "X" if model[cell] is None else "1" if model[cell] else "0" for cell in row
        )
        for row in prev_vars
    )
)

# solve(*constraints)
