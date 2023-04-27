from agent import AlphaBetaAgent
import minimax
from pontu_state import *
from pontu_state import PontuState

"""
Agent skeleton. Fill in the gaps.
"""

class State:
    def __init__(self, pid,coord,adj_mat):
        self.pid = pid
        self.adj_mat = adj_mat
        self.coord = coord

    def result(self, action):
        # action oponent_pawn, oponent pawn bridge to remove, ally_pawn to move, new ally_pawn position
        newpl = list(self.coord[self.pid])
        for idx,i in enumerate(newpl):
            if i == action[2]:
                newpl[idx] = action[3]
        newp = None
        newp = (self.coord[0], tuple(newpl)) if self.pid == 0 else (tuple(newpl), self.coord[1])

        nb = tuple(set(s.copy()) for s in self.adj_mat)
        nb[action[0]].remove(action[1])
        nb[action[1]].remove(action[0])
        return State(1-self.pid, nb, newp)
    def get_actions(self, action):
        al_pawns = self.coord[self.pid]
        op_pawns = [1-self.pid]
        for j, pawn in enumerate(al_pawns):
            if len(self.adj_mat[pawn]) != 0:
                for i in self.adj_mat[pawn]:
                    if i not in al_pawns and i not in op_pawns:
                        for op in op_pawns:
                            if len(self.adj_mat[op]) != 0:
                                for r in self.adj_mat[op]:
                                    yield op, r, j, i

    def game_over(self):
        any(all(not self.adj_mat[p] for p in pawns) for pawns in self.coord)


class MyAgent(AlphaBetaAgent):

    def __init__(self):

        board = (
            set((1, 5)), set((0, 2, 6)), set((1, 3, 7)), set((2, 4, 8)), set((3, 9)),
            set((0, 6, 10)), set((1, 5, 7, 11)), set((2, 6, 8, 12)), set((3, 7, 9, 13)), set((4, 8, 14)),
            set((5, 11, 15)), set((6, 10, 12, 16)), set((7, 11, 13, 17)), set((8, 12, 14, 18)), set((9, 13, 19)),
            set((10, 16, 20)), set((11, 15, 17, 21)), set((12, 16, 18, 22)), set((13, 17, 19, 23)),
            set((14, 18, 24)),
            set((15, 21)), set((16, 20, 22)), set((17, 21, 23)), set((18, 22, 24)), set((19, 23))
        )
        self.state = State( self.id, board, ((6, 7, 8), (16, 17, 18)) )

    """
    This is the skeleton of an agent to play the Tak game.
    """
    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left
        return minimax.search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    
    def successors(self, state):
        get_actions = PontuState.get_current_player_actions(state)
        for moves in get_actions:
            mov_state = deepcopy(state)
            PontuState.apply_action(mov_state, moves)
            yield moves, mov_state
    """
    def successors(self, state: State):
        for action in state.get_actions():
            yield action, state.result(action)

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state: State, depth):
        if state.game_over():
          return True
        if depth == 2:
          return True
        return False

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """


    def evaluate(self, state: State):
        # This means that if the current player's ID is 0, then opp_player will be 1, and if the current player's ID is 1, then opp_player will be 0.
        # opp_player = 0 if current_player == 1 else 1
        # current_player = state.get_cur_player()
        # opp_player = 1 - self.id

        # Checks if the current player has no pawns left on the board, and if that's the case, it returns a score of 0.
        # If a player has no pawns on the board, he cannot make any more moves, and the game is essentially over for him.
        # In this case, it doesn't matter what the score is for the other player, because they have already won the game.
        #    if len(state.cur_pos[current_player]) == 0:
        #        return 0

        # Checks if the opponent player has any pawns left on the board.
        # If the opponent has no pawns left, it means that the current player has won, and so the function returns the number of pawns that the current player has on the board as the score.
        #    if len(state.cur_pos[opp_player]) == 0:
        #        return len(state.cur_pos[current_player])


        opp_player = 1 - self.id
        us = self.id
        score = 0
        for pawn in range(3):
            score += len(state.adj_mat[state.coord[pawn]])
            score -= len(state.adj_mat[state.coord[pawn]])
        #score = sum(sum(state.adj_bridges(opp_player, pawn).values()) for pawn in range(len(state.cur_pos[1])))
        #print(score)
        return score