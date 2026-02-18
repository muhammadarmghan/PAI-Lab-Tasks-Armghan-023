import random

class NQueensSolver:
    def __init__(self, n):
        self.n = n

    def show(self, board):
        for r in range(self.n):
            row = ['.'] * self.n
            row[board[r]] = 'Q'
            print(' '.join(row))
        print(board)
        print()

    def backtracking(self):
        board = [-1] * self.n

        def valid(r, c):
            for i in range(r):
                if board[i] == c or abs(board[i] - c) == abs(i - r):
                    return False
            return True

        def dfs(row):
            if row == self.n:
                return True
            for col in range(self.n):
                if valid(row, col):
                    board[row] = col
                    if dfs(row + 1):
                        return True
            return False

        dfs(0)
        self.show(board)

    def hill_climbing(self):
        board = [random.randint(0, self.n - 1) for _ in range(self.n)]

        def conflicts(b):
            c = 0
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    if b[i] == b[j] or abs(b[i] - b[j]) == abs(i - j):
                        c += 1
            return c

        steps = 0
        while conflicts(board) != 0 and steps < 1000:
            steps += 1
            improved = False
            for r in range(self.n):
                old = board[r]
                for c in range(self.n):
                    board[r] = c
                    if conflicts(board) < conflicts(board[:r] + [old] + board[r+1:]):
                        improved = True
                        break
                if not improved:
                    board[r] = old

            if not improved:
                board = [random.randint(0, self.n - 1) for _ in range(self.n)]

        self.show(board)

    def genetic(self):
        def fitness(b):
            score = 0
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    if b[i] != b[j] and abs(b[i] - b[j]) != abs(i - j):
                        score += 1
            return score

        pop = [[random.randint(0, self.n - 1) for _ in range(self.n)] for _ in range(100)]

        for _ in range(1000):
            pop.sort(key=fitness, reverse=True)
            if fitness(pop[0]) == (self.n * (self.n - 1)) // 2:
                break

            next_gen = pop[:50]
            while len(next_gen) < 100:
                a, b = random.sample(next_gen, 2)
                cut = random.randint(1, self.n - 1)
                child = a[:cut] + b[cut:]
                if random.random() < 0.1:
                    child[random.randint(0, self.n - 1)] = random.randint(0, self.n - 1)
                next_gen.append(child)
            pop = next_gen

        self.show(pop[0])


solver = NQueensSolver(8)
solver.backtracking()
solver.hill_climbing()
solver.genetic()
