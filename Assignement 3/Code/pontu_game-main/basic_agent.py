import copy

from agent import AlphaBetaAgent
import minimax
from pontu_state import *

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

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
  """
  def successors(self, state):

      get_actions = PontuState.get_current_player_actions(state)

      for moves in get_actions:

          mov_state = deepcopy(state)
          PontuState.apply_action(mov_state, moves)

          yield moves, mov_state


  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
      if PontuState.game_over(state):
          return True
      if depth >= 1:
          return True
      return False

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """


  def evaluate(self, state):
    # This means that if the current player's ID is 0, then opp_player will be 1, and if the current player's ID is 1, then opp_player will be 0.
    #opp_player = (state.get_cur_player() + 1) % 2


    current_player = state.get_cur_player()
    opp_player = 0 if current_player == 1 else 1

# Checks if the current player has no pawns left on the board, and if that's the case, it returns a score of 0.
# If a player has no pawns on the board, he cannot make any more moves, and the game is essentially over for him.
# In this case, it doesn't matter what the score is for the other player, because they have already won the game.
    if len(state.cur_pos[current_player]) == 0:
        return 0

# Checks if the opponent player has any pawns left on the board.
# If the opponent has no pawns left, it means that the current player has won, and so the function returns the number of pawns that the current player has on the board as the score.
    if len(state.cur_pos[opp_player]) == 0:
        return len(state.cur_pos[current_player])

    score = sum(len(state.adj_bridges(opp_player, pawn)) for pawn in range(len(state.cur_pos[1])))
    return score