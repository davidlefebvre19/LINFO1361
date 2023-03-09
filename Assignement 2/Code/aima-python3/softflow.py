from search import *

#################
# Problem class #
#################

class SoftFlow(Problem):


    def __init__(self, initial):
        super().__init__(initial)

        
    def actions(self, state):

        possible_actions = []

        number_possibilities = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        letter_possibilities = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

        pos = [
            [1, 0], # Down
            [-1, 0], # Up
            [0, 1], # Right
            [0, -1] # Left
        ]

        #current_number = 0
        init_pos = state.letter_coords[0]
        #for h in range(10):
        #    if(init_pos[0] == letter_possibilities[h]):
        #        current_number = number_possibilities[h]

        #number_possibilities.remove(current_number)
        column = init_pos[1] # x
        row = init_pos[2] # y
        new_init_pos = [init_pos[1], [init_pos[2]]]

        for [i, j] in pos:
            new_x = column + i
            new_y = row + j

            for w in range(9):
                if(state.grid[new_y][new_x] != '#' and new_y < len(state.grid) and new_x < len(state.grid[0]) and state.grid[new_y][new_x] != number_possibilities[w]):
                    possible_actions.append([new_y, new_x, new_init_pos])
        return possible_actions

    def result(self, state, action):
        copy_grid = [x[:] for x in state.grid]
        new_r, new_col, last_pos = action

        nb_cables = state.nb_cables
        letter_coords = state.letter_coords.copy()
        if(copy_grid[new_r][new_col] == state.letter_coords[0][0]):
            nb_cables-=1
            state.letter_coords.remove(letter_coords[0])
        goal = state.goal

        to_go = len(state.letter_coords)
        if(to_go == 0):
            goal = True

        return State(copy_grid, problem.list_to_tuple(copy_grid), goal, letter_coords, state.number_coords, nb_cables, state.Astar)

    def goal_test(self, state):
        return state.goal

    def list_to_tuple(self, grid):
        list_grid = []
        for i in range(len(grid)):
            list_grid.append(tuple(grid[i]))
        return tuple(list_grid)

# Should use the Manhattan distance heuristic.
# This heuristic calculates the sum of the distances between each cable's current position and its destination position.
# Since the cables cannot overlap,
# this heuristic provides an accurate estimate of the minimum number of cable movements required to reach the goal state.
    def h(self, node):
        h = 0.0
        k = node.state.nb_cables
        for i in range(k):
            entry = node.state.letter_coords[i]
            exit = node.state.number_coords[i]
            h += abs(entry[1] - exit[1]) + abs(entry[2] - exit[2])
        return h
        

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            
        state = State.from_string(''.join(lines))
        return SoftFlow(state)



###############
# State class #
###############

class State:

    def __init__(self, grid, grid_tuple = None, goal = None, letter_coords = None, number_coords = None, nb_cables = None, Astar = None):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

        self.grid_tuple = grid_tuple
        self.goal = goal
        self.letter_coords = letter_coords
        self.number_coords = number_coords
        self.nb_cables = nb_cables
        self.Astar = Astar
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        if isinstance(other_state, State):
            return self.grid == other_state.grid
        return False

    def __hash__(self):
        return hash(self.grid_tuple)
    
    def __lt__(self, other):
        return hash(self) < hash(other)

    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


def find_infos(grid):
    letter_possibilities = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    number_possibilities = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    nb_cables = 0
    letter_coords = []
    number_coords = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for x in range(len(letter_possibilities)):
                if(grid[i][j] == letter_possibilities[x]):
                    nb_cables+=1
                    letter_coords.append([letter_possibilities[x], i, j])
                if(grid[i][j] == number_possibilities[x]):
                    number_coords.append([number_possibilities[x], i, j])
                    ord(grid[i][j])
    letter_coords.sort(key=lambda x: x[0])
    number_coords.sort(key=lambda x: x[0])
    return nb_cables, letter_coords, number_coords

def print_info(problem):
    print("grid ")
    print(problem.initial.grid)
    print("grid_list")
    print(problem.initial.grid_tuple)
    print("number of cables left")
    print(problem.initial.nb_cables)
    print("letter coords")
    print(problem.initial.letter_coords)
    print("number coords")
    print(problem.initial.number_coords)

#####################
# Launch the search #
#####################

problem = SoftFlow.load(sys.argv[1])
print(problem.initial)

problem.initial.nb_cables, problem.initial.letter_coords, problem.initial.number_coords = find_infos(problem.initial.grid)

print(problem.initial)

problem.initial.grid_tuple = problem.list_to_tuple(problem.initial.grid)

print_info(problem)

node, explored, frontier = breadth_first_graph_search(problem)
print(node)
print(explored)
print(frontier)

#path = node.path()

#node = astar_search(problem)

# example of print
#path = node.path()

#print('Number of moves: ', str(node.depth))
#for n in path:
#    print(n.state)  # assuming that the _str_ function of state outputs the correct format
#    print()

