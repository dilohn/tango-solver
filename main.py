from read_board import parse_puzzle
from tango_algo import PuzzleSolver
from overlay_solution import fill_puzzle

IMAGE_PATH = "puzzle.png"
EQ_TMPL = "equals_template.png"
X_TMPL = "x_template.png"


def solve_image(image_path, eq_tmpl=EQ_TMPL, x_tmpl=X_TMPL):
    initial, constraints = parse_puzzle(
        image_path, eq_tmpl_path=eq_tmpl, x_tmpl_path=x_tmpl
    )
    solver = PuzzleSolver(initial, constraints)
    print(solver.constraints)
    sol = solver.solve()
    filled_path = fill_puzzle(IMAGE_PATH, initial, sol)
    if sol is None:
        return initial, None
    solution_grid = [
        [sol[(i, j)] for j in range(len(initial[0]))] for i in range(len(initial))
    ]
    return initial, solution_grid


def main():
    initial, solution = solve_image(IMAGE_PATH)

    print("Initial board:")
    for row in initial:
        print(" ".join(cell if cell is not None else "." for cell in row))

    if solution is None:
        print("\nNo solution found.")
    else:
        print("\nSolution board:")
        for row in solution:
            print(" ".join(row))


if __name__ == "__main__":
    main()
