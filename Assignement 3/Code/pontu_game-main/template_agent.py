from agent import AlphaBetaAgent
import minimax
from pontu_state import *
from pontu_state import PontuState



"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

  counter = 0
  counter_two = 0

  def __init__(self):
      self.counter = 0
      self.counter_two = 0
  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left
    if self.counter_two % 3 == 0:
        self.counter += 1
    self.counter_two += 1
    return minimax.search(state, self, True)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):

# Objectif: - virer toutes les actions ou on ne casse pas un bridge adjacent au pion adverse
      get_actions = PontuState.get_current_player_actions(state)

      #filtered_actions = []
      #for action in get_actions:
      #    if (action[2] == "h" and ((action[3], action[4] - 1) in opponent_pawns[action[0]] or (action[3] + 1, action[4] - 1) in opponent_pawns[action[0]])) or (action[2] == "v" and ((action[3] - 1, action[4]) in opponent_pawns[action[0]] or (action[3] - 1, action[4] + 1) in opponent_pawns[action[0]])):
      #        filtered_actions.append(action)

      for moves in get_actions:
          mov_state = state.copy()
          #mov_state = deepcopy(state)
          mov_state.apply_action(moves)
          #PontuState.apply_action(mov_state, moves)
          yield moves, mov_state


  """
  The cutoff function returns true if the alpha-beta/minimax2 Pontu (35 pts)
2.1 A Basic Alpha-Beta Agent (5 pts on INGInious; nothing to report)
2.2 Evaluation function (5 pts)
5. What are the weak points of the evaluation functions of your basic agent? (2 pts)
Please list your ideas using bullet points, e.g. something of the form:
• Name of your idea
Possibly a short explanation describing your idea... Go straight to the point!
•

  search has to stop and false otherwise.
  """
  def cutoff(self, state: PontuState, depth):

      if PontuState.game_over(state):
          return True

      if depth == self.counter:
          return True
      return False

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """


  def evaluate(self, state: PontuState):
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
        score += sum(state.adj_bridges(us, pawn).values())
        score -= sum(state.adj_bridges(opp_player, pawn).values())
        #current_pos = self.cur_pos[opp_player][pawn]
        #score += (current_pos[0] + current_pos[1] - 4)


    # Indicates the position of the pawns: self.cur_pos[i][j] is the (x,y) position of jth pawn of player i

    #score = sum(sum(state.adj_bridges(opp_player, pawn).values()) for pawn in range(len(state.cur_pos[1])))
    #print(score)
    return score