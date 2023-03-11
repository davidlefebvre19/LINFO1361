from search import *
import copy

#################
# Problem class #
#################

class SoftFlow(Problem):

    def __init__(self, initial, size, nb_letters, dest_coords, source_coords, letters):
        super().__init__(initial)
        self.size = size
        self.nb_letters = nb_letters
        self.source_coords = source_coords
        self.dest_coords = dest_coords
        self.letters = letters
        self.found = 0

        
    def actions(self, state):
        actions = []
        moves = [[1,0], [-1,0],[0,1],[0,-1]]
        for w, letter in enumerate(state.source_coords):
            for [i, j] in moves:
                new_coord = (state.source_coords[w][0] + i, state.source_coords[w][1]+j)
                if state.grid[new_coord[0]][new_coord[1]] != '#' or ord(state.grid[new_coord[0]][new_coord[1]]) == ord(str(w)):
                    actions.append((w,[i, j]))
        yield actions

    def result(self, state, action):
        #compute new coords
        new_coords = (state.source_coords[action[0]][0] + action[1][0], state.source_coords[action[0]][1]+action[1][1])
        new_grid = [x[:] for x in state.grid]
        #new_grid[state.source_coords[action[0]][0]][state.source_coords[action[0]][1]] = action[0]
        # update element @new_coords
        new_source_coords = state.source_coords.copy()
        if new_grid[new_coords[0]][new_coords[1]] == ' ':
            new_grid[new_coords[0]][new_coords[1]] = action[0]
            new_source_coords[action[0]] = new_coords
        else:
            # destnation has been reached
            new_source_coords.remove(new_source_coords[0])
            #del new_source_coords.source_coords[action[0]]
        return State(new_grid, new_source_coords)

    def goal_test(self, state):
        return len(state.source_coords) == 0

    def h(self, node=None):
        h = 0.0
        for i, source_coord in enumerate(node.state.source_coords):
            h+= abs(source_coord[0]-self.dest_coords[i][0]) + abs(source_coord[1]-self.dest_coords[i][1])
        return h


    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        lines = [line.rstrip('\n') for line in lines]
        grid = [[char for char in line] for line in lines]

        letter_possibilities = set("abcdefghij")
        number_possibilities = set("0123456789")
        source_coords = []
        dest_coords = []

        for w in letter_possibilities:
            for i, row in enumerate(grid):
                for j, char in enumerate(row):
                    if char == w:
                        source_coords.append((i, j))

        for w in number_possibilities:
            for i, row in enumerate(grid):
                for j, char in enumerate(row):
                    if char == w:
                        dest_coords.append((i, j))

        size = (len(grid), len(grid[0]))
        state = State(grid, source_coords)

        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        letters = letters[:len(source_coords)]

        source_coords.sort(key=lambda x: x[0])

        return SoftFlow(state, size, len(letter_possibilities), dest_coords, source_coords, letters)


###############
# State class #
###############

class State:

    def __init__(self, grid, source_coords):
        self.nbr = len(grid) # Y upper bound
        self.nbc = len(grid[0]) # X upper bound
        self.grid = grid
        self.source_coords = source_coords
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        if isinstance(other_state, State):
            return self.grid == other_state.grid
        return False

    def __hash__(self):
        grid_str = "".join("".join(str(row)) for row in self.grid)
        return hash(grid_str)
    
    def __lt__(self, other):
        return hash(self) < hash(other)

    def from_string(string):
        lines = string.strip().splitlines()
        grid = list(
            map(lambda x: list(x.strip()), lines)
        )
        letter_possibilities = set("abcdefghij")

        source_coords = []

        for w in letter_possibilities:
            for i, row in enumerate(grid):
                for j, char in enumerate(row):
                    if char == w:
                        source_coords.append((i, j))

        return State(grid, source_coords)




#####################
# Launch the search #
#####################

# Initial SoftFlow(Problem) object, state has already been initialized from load() func
problem = SoftFlow.load(sys.argv[1])

#heuristic = lambda arg : SoftFlow.h(arg)
node = astar_search(problem, h=())

# example of print
path = node.path()

print('Number of moves: ', str(node.depth))
for n in path:
    print(n.state)  # assuming that the _str_ function of state outputs the correct format
    print()

