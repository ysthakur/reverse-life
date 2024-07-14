from z3 import *

board = [
    [1],
    [1],
    [1],
]

# Add a ring of dead cells
padding = 2  # cells thick
board = [
    *[[0] * (len(board[0]) + 2 * padding)] * padding,
    *[[0] * padding + row + [0] * padding for row in board],
    *[[0] * (len(board[0]) + 2 * padding)] * padding,
]
print(board)

curr_vars = [
    [Bool(f"c[{i}][{j}]") for j in range(len(board[0]))] for i in range(len(board))
]

prev_vars = [
    [Bool(f"p[{i}][{j}]") for j in range(len(board[0]))] for i in range(len(board))
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
    for constraint in constraints:
        print(constraint)
    constraint = Or(*[And(bools) for bools in constraints])
    return constraint


def constraints_at(r: int, c: int):
    """Get constraints for curr_vars[r][c]"""

    # Neighbors of prev_vars[r][c]
    neighbors = []
    if c > 0:
        neighbors.append(prev_vars[r][c - 1])
    if c + 1 < len(board[0]):
        neighbors.append(prev_vars[r][c + 1])
    cmin = max(c - 1, 0)
    cmax = min(c + 2, len(board[0]))
    if r > 0:
        neighbors.extend(prev_vars[r - 1][cmin:cmax])
    if r + 1 < len(board):
        neighbors.extend(prev_vars[r + 1][cmin:cmax])
    print(neighbors)
    print("--- end neighbors ---")

    exactly_two = constrain_bools(neighbors, 2, 2)
    print("---")
    exactly_three = constrain_bools(neighbors, 3, 3)

    print("e")

    alive = Or(And(prev_vars[r][c], exactly_two), exactly_three)

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
