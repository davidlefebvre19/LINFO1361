from search import *

#################
# Problem class #
#################

class SoftFlow(Problem):

    def __init__(self, initial, size, nb_letters, dest_coords, source_coords):
        super().__init__(initial)
        self.size = size
        self.nb_letters = nb_letters
        self.source_coords = source_coords
        self.dest_coords = dest_coords
        
    def actions(self, state):
        pass

    def result(self, state, action):
        pass

    def goal_test(self, state):
        pass

    def h(self, node):
        h = 0.0
        # ...
        # compute an heuristic value
        # ...
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

        return SoftFlow(state, size, len(letter_possibilities), dest_coords, source_coords)


###############
# State class #
###############

class State:

    def __init__(self, grid, source_coords):
        self.nbr = len(grid) # Y upper bound
        self.nbc = len(grid[0]) # X upper bound
        self.grid = grid
        self.source_cord = source_coords
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other_state):
        if isinstance(other_state, State):
            return self.grid == other_state.grid
        return False

    def __hash__(self):
        grid_str = "".join("".join(row) for row in self.grid)
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



node = astar_search(problem, problem.h(), True)

# example of print
path = node.path()

print('Number of moves: ', str(node.depth))
for n in path:
    print(n.state)  # assuming that the _str_ function of state outputs the correct format
    print()

