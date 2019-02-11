import math
import random


class Node:

    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.visits = 0
        self.wins = 0
        self.to_expand = state.get_moves()
        self.children = []
        self.terminal_eval = None

    def update(self, result, player):
        if self.state.player_to_move == player:
            self.wins += abs(result-1)
        else:
            self.wins += result

        self.visits += 1

    def uct(self, child):
        const = 25
        return child.wins/child.visits + math.sqrt(const*math.log(self.visits)/child.visits)

    def select_child(self):
        return max(self.children, key=lambda c: self.uct(c))

    def add_child(self, move):
        clone_state = self.state.replicate()
        clone_state.make_move(move)
        new_child = Node(self, clone_state)
        self.children.append(new_child)
        self.to_expand.remove(move)
        return new_child

    def is_fully_expanded(self):
        return (self.to_expand == [])

    def is_terminal(self):
        return (self.children == [] and self.to_expand == [])

    def get_random_move_to_expand(self):
        return random.choice(self.to_expand)

    def back_up(self, player, result):
        if self.terminal_eval is None:
            terms = [c.terminal_eval for c in self.children]

            player_term = abs(player - self.state.player_to_move) # 0 if same, else 1

            if terms.__contains__(abs(player_term - 1)):
                self.terminal_eval = abs(player_term - 1)

            elif self.is_fully_expanded() and None not in terms:

                if terms.__contains__(0.5):
                    self.terminal_eval = 0.5
                else:
                    self.terminal_eval = player_term

        if self.terminal_eval is not None and self.parent is not None:
            self.parent.back_up(player, result)

        # could start a back-propagation from last node that doesnt have terminal_eval?

    def is_terminal_evaluated(self):
        return self.terminal_eval is not None

    def go_to_child(self, move):
        for c in self.children:
            if c.state.last_move == move:
                return c

    def get_best_child(self):
        return max(self.children, key=lambda c: c.visits)
