class Connect2:

    def __init__(self):
        self.table = [0, 0, 0, 0]
        self.player_to_move = 1
        self.last_move = None

    def make_move(self, move):
        self.table[move] = self.player_to_move
        self.player_to_move = 3 - self.player_to_move
        self.last_move = move

    def get_moves(self):
        if self.result() is not None:
            return []
        return [i for i in range(4) if self.table[i] == 0]

    def __repr__(self):
        s = ""
        for n in self.table:
            s += str(n)
        return s

    def result(self, player=1):

        for (x, y) in [(0, 3), (1, 2)]:

            if self.table[x] == self.table[y]:

                if player == self.table[x]:
                    return 1
                if 3 - player == self.table[x]:
                    return 0

        if sum(self.table) == 6:
            return 0.5

        return None

    def replicate(self):
        clone = Connect2()
        clone.table = self.table[:]
        clone.player_to_move = self.player_to_move
        clone.last_move = self.last_move
        return clone

    def is_game_over(self):
        return self.get_moves() == []
