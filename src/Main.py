import random
import time
from node import Node
from tictactoe import TicTacToe
from connect2 import Connect2
from connect43D import Connect43D


def perform_uct_search(time_allowed, game, max_n=10000):
    time_start = time.time()

    count = 0
    root = Node(None, game)
    player = root.state.player_to_move

    time_used = 0
    while time_used < time_allowed:

        count += 1
        if count >= max_n:
            break

        node = root

        # select node to expand
        while node.is_fully_expanded() and not node.is_terminal_evaluated() and not node.is_terminal():
            node = node.select_child()

        # expand node if possible
        if node.is_terminal_evaluated():
            if node.state.player_to_move == 1 and node.terminal_eval == 1 and False:
                print("terminal state:")
                print("to move:", node.state.player_to_move)
                print("eval:", node.terminal_eval)
                print(node.state)
                print(node.visits, node.wins)

            # back-propagate
            to_update = node
            result = node.terminal_eval

            while to_update is not None:
                to_update.update(result, player)
                to_update = to_update.parent

        elif node.is_terminal():
            expanded_node = node
            result = node.state.result(player)
            expanded_node.terminal_eval = result
            expanded_node.parent.back_up(player, result)

        else:
            random_move = node.get_random_move_to_expand()
            expanded_node = node.add_child(random_move)

            # simulate
            simulation_state = expanded_node.state.replicate()
            h = []

            sim_depth = 100
            while simulation_state.result() is None and sim_depth >= 0:
                rand_move = random.choice(simulation_state.get_moves())
                h.append(simulation_state.replicate())
                simulation_state.make_move(rand_move)
                sim_depth -= 1
            result = simulation_state.result(player)

            if result is None:
                print(simulation_state)

            # back-propagate
            to_update = expanded_node
            while to_update is not None:
                to_update.update(result, player)
                to_update = to_update.parent

        time_used = time.time() - time_start

    print("\nRoll-outs performed: "+str(count))
    return max(root.children, key=lambda c: c.wins/c.visits if c.terminal_eval is None else c.visits*c.terminal_eval)


def test(n):

    wins = 0
    for i in range(n):

        m = Connect2()
        hist = []
        children = []
        while not m.is_game_over():
            move = perform_uct_search(0.5, m)
            hist.append(move.state)
            children.append(
                [(c.state.last_move, c.wins / c.visits, c.visits, c.terminal_eval) for c in move.parent.children])
            # print(move)
            m.make_move(move.state.last_move)

        if m.result() != 0.5:
            wins += 1
            for n in hist:
                print(children[hist.index(n)])
                print(n)
            break

        print("simulating", i + 1, "th game")

    print(wins, "win in", n + 1, "games")


def play_uct_move(game):
    c = perform_uct_search(10, game, 100000000)
    game.make_move(c.state.last_move)
    s = "Children: \n"
    for i in range(len(c.parent.children)):
        if i == 8:
            s += "\n"
        child = c.parent.children[i]
        s += "("+str(round(child.wins/child.visits,2))+", "+str(child.terminal_eval)+", "+str(child.state.last_move)+") "
    print(s)
    print("\nMove Made: "+str(c.state.last_move))
    s = "Current Evaluation: " + str(round(c.parent.wins/c.parent.visits,2))
    print(s)


def automatic_game(first):
    game = TicTacToe()
    print(game)

    if not first:
        play_uct_move(game)
        print(game)

    while not game.is_game_over():
        num = int(input("choose move: "))
        game.make_move(num)

        print(game)

        if not game.is_game_over():
            play_uct_move(game)
            print(game)

    evaluation = game.result()

    if first:
        if evaluation == 1:
            print("You Win")
        elif evaluation == 0:
            print("You Lose")
        else:
            print("Draw")
    else:
        if evaluation == 1:
            print("You Lose")
        elif evaluation == 0:
            print("You Win")
        else:
            print("Draw")


def main():

    m = Connect43D()

    for n in [0, 4, 1, 5, 2, 13, 12]:
        m.make_move(n)

    c = perform_uct_search(5, m, 50000)
    s = ""
    for i in range(len(c.parent.children)):
        if i == 8:
            s += "\n"
        child = c.parent.children[i]
        s += "("+str(round(child.wins/child.visits,2))+", "+str(child.terminal_eval)+", "+str(child.state.last_move)+")"
    # print([(round(child.wins/child.visits,2), child.terminal_eval, child.state.last_move)
    # for child in c.parent.children])
    print(s)
    print(m)
    print(c.state.last_move)


if __name__ == "__main__":
    automatic_game(False)
    

