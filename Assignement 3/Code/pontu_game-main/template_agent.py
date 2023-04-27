from agent import AlphaBetaAgent
import minimax
from pontu_state import *
from pontu_state import PontuState

"""
Agent skeleton. Fill in the gaps.
"""

DIR_TO_VAL = {
    'NORTH': -1,
    'SOUTH': 1,
    'WEST': -1,
    'EAST': 1
}

# Constantes pour la fonction d'évaluation heuristique
BONUS_SHARED_BRIDGES = 2
BONUS_DISTANCE = 4
BONUS_ISOLATED_PAWN = 6




class MyAgent(AlphaBetaAgent):
    """
    This is the skeleton of an agent to play the Tak game.
    """

    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left
        return minimax.search(state, self)

    def is_bridge_adjacent_to_enemy(self, player, action, state):
        bridge_type, x, y = action[-3], action[-2], action[-1]
        enemy_player = 1 - player

        if bridge_type == 'h':
            bridge_coords = [(x, y), (x + 1, y)]
        else:  # bridge_type == 'v'
            bridge_coords = [(x, y), (x, y + 1)]

        for pawn in range(3):
            pawn_position = state.get_pawn_position(enemy_player, pawn)
            if pawn_position in bridge_coords:
                return True

        return False

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """

    def successors(self, state):
        get_actions = PontuState.get_current_player_actions(state)
        for moves in get_actions:
            if self.is_bridge_adjacent_to_enemy(self.id, moves, state):
                mov_state = deepcopy(state)
                PontuState.apply_action(mov_state, moves)

                yield moves, mov_state

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """

    def cutoff(self, state: PontuState, depth):
        if PontuState.game_over(state):
            return True
        if depth == 2:
            return True
        return False

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """

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
    def Xevaluate(self, state: PontuState):

        opp_player = 1 - self.id
        us = self.id
        score = 0
        for pawn in range(3):
            score += sum(state.adj_bridges(us, pawn).values())
            score -= sum(state.adj_bridges(opp_player, pawn).values())
        # score = sum(sum(state.adj_bridges(opp_player, pawn).values()) for pawn in range(len(state.cur_pos[1])))
        # print(score)
        return score





    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def evaluate(self, state: PontuState):
        opp_player = 1 - self.id
        us = self.id
        score = 0

        for pawn in range(3):
            our_moves = state.adj_bridges(us, pawn)
            opp_moves = state.adj_bridges(opp_player, pawn)

            # Mobilité
            score += sum(our_moves.values())
            score -= sum(opp_moves.values())

            # shared_bridges
            shared_bridges = 0
            for key, value in state.adj_pawns(us, pawn).items():
                if value:
                    adj_p_c = state.get_pawn_position(us, pawn)
                    print(adj_p_c)
                    if key == 'NORTH' or 'SOUTH':
                        adj_p_c = (adj_p_c[0]+DIR_TO_VAL[key], adj_p_c[1])
                    if key == 'WEST' or 'EAST':
                        adj_p_c = (adj_p_c[0] , adj_p_c[1]+ DIR_TO_VAL[key])
                    if adj_p_c in state.cur_pos[us]:
                        shared_bridges += 1

            # Favorise les ponts partagés
            score += shared_bridges * BONUS_SHARED_BRIDGES

            # Distance des pions adverses
            for opp_pawn in range(3):
                distance = self.manhattan_distance(state.get_pawn_position(us, pawn), state.get_pawn_position(opp_player, opp_pawn))
                score -= int(BONUS_DISTANCE / distance)

            # Isolement
            if sum(our_moves.values()) == 1:
                score -= BONUS_ISOLATED_PAWN

        # if state.game_over():
        #    score+=100

        return score
