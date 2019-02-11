class TicTacToe:

    def __init__(self):
        self.table = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.player_to_move = 1
        self.last_move = None

    def make_move(self, move):
        if(self.table[move] == 0):
            self.table[move] = self.player_to_move
            self.player_to_move = 3 - self.player_to_move
            self.last_move = move

    def get_moves(self):
        if self.result() is not None:
            return []
        return [i for i in range(9) if self.table[i] == 0]

    def __repr__(self):
        s = ""
        for i in range(9):
            s += "-XO"[self.table[i]]
            if i % 3 == 2:
                s += "\n"
        return s

    def __str__(self):
        s = ""
        for i in range(9):
            s += "-XO"[self.table[i]]
            if i % 3 == 2:
                s += "\n"
        return s

    def result(self, player=1):

        for (x, y, z) in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if self.table[x] == self.table[y] == self.table[z]:

                if player == self.table[x]:
                    return 1
                if 3-player == self.table[x]:
                    return 0

        zeros = 0
        for i in range(9):
            if self.table[i] == 0:
                zeros += 1

        if zeros == 0:
            return 0.5

        return None

    def replicate(self):
        clone = TicTacToe()
        clone.table = self.table[:]
        clone.player_to_move = self.player_to_move
        clone.last_move = self.last_move
        return clone

    def is_game_over(self):
        return self.get_moves() == []