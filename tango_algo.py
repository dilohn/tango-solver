from copy import deepcopy


class PuzzleSolver:
    def __init__(self, initial, constraints):
        self.initial = initial
        self.constraints = constraints
        self.cells = [(i, j) for i in range(6) for j in range(6)]
        self.domains = {}
        for i, j in self.cells:
            v = initial[i][j]
            if v in ("C", "M"):
                self.domains[(i, j)] = {v}
            else:
                self.domains[(i, j)] = {"C", "M"}

    def solve(self):
        if not self.propagate():
            return None
        if all(len(self.domains[c]) == 1 for c in self.cells):
            return {c: next(iter(self.domains[c])) for c in self.cells}
        c = min(
            (c for c in self.cells if len(self.domains[c]) > 1),
            key=lambda x: len(self.domains[x]),
        )
        for v in list(self.domains[c]):
            new = deepcopy(self)
            new.domains[c] = {v}
            sol = new.solve()
            if sol:
                return sol
        return None

    def propagate(self):
        changed = True
        while changed:
            changed = False
            for (c1, c2), t in self.constraints.items():
                if t == "=":
                    a = self.domains[c1] & self.domains[c2]
                    if a != self.domains[c1]:
                        self.domains[c1] = a
                        changed = True
                    if a != self.domains[c2]:
                        self.domains[c2] = a
                        changed = True
                elif t == "X":
                    if len(self.domains[c1]) == 1:
                        v = next(iter(self.domains[c1]))
                        if v in self.domains[c2]:
                            self.domains[c2].discard(v)
                            changed = True
                    if len(self.domains[c2]) == 1:
                        v = next(iter(self.domains[c2]))
                        if v in self.domains[c1]:
                            self.domains[c1].discard(v)
                            changed = True
            for i in range(6):
                if self.apply_no_three([(i, j) for j in range(6)]):
                    changed = True
                if self.apply_count([(i, j) for j in range(6)]):
                    changed = True
            for j in range(6):
                if self.apply_no_three([(i, j) for i in range(6)]):
                    changed = True
                if self.apply_count([(i, j) for i in range(6)]):
                    changed = True
            if any(len(self.domains[c]) == 0 for c in self.cells):
                return False
        return True

    def apply_no_three(self, line):
        changed = False
        for k in range(4):
            a, b, c = line[k], line[k + 1], line[k + 2]
            if (
                len(self.domains[a]) == 1
                and len(self.domains[b]) == 1
                and next(iter(self.domains[a])) == next(iter(self.domains[b]))
            ):
                v = next(iter(self.domains[a]))
                if v in self.domains[c]:
                    self.domains[c].discard(v)
                    changed = True
            if (
                len(self.domains[b]) == 1
                and len(self.domains[c]) == 1
                and next(iter(self.domains[b])) == next(iter(self.domains[c]))
            ):
                v = next(iter(self.domains[b]))
                if v in self.domains[a]:
                    self.domains[a].discard(v)
                    changed = True
        return changed

    def apply_count(self, line):
        changed = False
        vals = [next(iter(self.domains[c])) for c in line if len(self.domains[c]) == 1]
        for v in ("C", "M"):
            if vals.count(v) == 3:
                for c in line:
                    if v in self.domains[c] and len(self.domains[c]) > 1:
                        self.domains[c].discard(v)
                        changed = True
        return changed


if __name__ == "__main__":
    initial = [
        ["C", None, None, None, None, "M"],
        [None, "M", None, "C", None, None],
        [None, None, "C", None, None, None],
        [None, None, None, "M", None, None],
        [None, None, None, None, "M", None],
        ["M", None, None, None, None, "C"],
    ]
    constraints = {
        ((0, 0), (1, 0)): "=",
        ((2, 2), (2, 3)): "X",
    }
    solver = PuzzleSolver(initial, constraints)
    solution = solver.solve()
    if solution:
        grid = [[solution[(i, j)] for j in range(6)] for i in range(6)]
        for row in grid:
            print(" ".join(row))
    else:
        print("No solution found")
