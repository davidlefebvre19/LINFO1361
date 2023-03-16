from search import *
import copy
import time


#################
# Problem class #
#################

class SoftFlow(Problem):

    def __init__(self, source: dict, dest: dict, hashtag: set,nodes = []):
        head = {k: v for k, v in source.items()}
        super().__init__(State(source, set(source.values()), head))
        self.hashtag = hashtag
        self.nodes = nodes
        # My excuses for this
        numtoalpha = {
            '0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e',
            '5': 'f', '6': 'g', '7': 'h', '8': 'i', '9': 'j'}
        self.target = {numtoalpha[k]: v for k, v in dest.items()}
        self.dest = {numtoalpha[k]: {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)} for k, (x, y) in dest.items()}

    def actions(self, state):
        for k, p in state.sources.items():
            if p not in self.dest[k]:
                x, y = p

                up = (x + 1, y)
                if up not in self.hashtag and not up in state.visited:
                    yield k, up

                down = (x - 1, y)
                if down not in self.hashtag and not down in state.visited:
                    yield k, down

                right = (x, y + 1)
                if right not in self.hashtag and not right in state.visited:
                    yield k, right

                left = (x, y - 1)
                if left not in self.hashtag and not left in state.visited:
                    yield k, left

    def result(self, state, action):
        k, move = action
        ncoords = {k: v for k, v in state.sources.items()}
        ncoords[k] = move
        nvisited = set(state.visited)
        nvisited.add(move)
        if(move not in self.nodes): self.nodes.append(move)
        # nhead = {k: v for k, v in state.head.items()}
        # nhead[k] = move
        return State(ncoords, nvisited, move)

    def goal_test(self, state):
        for k in state.sources:
            if state.sources[k] not in self.dest[k]:
                return False
        return True

    def h(self, node=None):
        # Manhatan's distance
        if node==None:
            return 0
        x = 0
        for k, v in node.state.sources.items():
            source_x, source_y = v
            target_x, target_y = self.target[k]
            x += abs(source_x - target_x) + abs(source_y - target_y)
        node.state.heur = x
        return x

    def load(filename):
        source = {}
        dest = {}
        hashtag = set()
        with open(filename, 'r') as f:
            for x, line in enumerate(f.readlines()):
                for y, char in enumerate(line):
                    if char == "#":
                        hashtag.add((x, y))
                    elif str.isalpha(char):
                        source[char] = (x, y)
                    elif str.isnumeric(char):
                        tmp = (x, y)
                        dest[char] = tmp
                        hashtag.add(tmp)
        return SoftFlow(source, dest, hashtag)


###############
# State class #
###############

class State:
    # BIG DEBUG
    def __init__(self, sources: dict, visited: set, head: dict):
        self.sources = sources
        self.visited = visited
        self.heur = -1
        self.head = head

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def __eq__(self, other):
        return self.sources == other.sources

    def __hash__(self):
        h = 0
        for p in self.sources.values():
            h += hash(p)
        return h

    def __lt__(self, other):
        return self.heur < other.heur

    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))


#####################
# Launch the search #
#####################

problem = SoftFlow.load(sys.argv[1])
# start = time.perf_counter()
node = astar_search(problem, problem.h(Node()))
# end = time.perf_counter()
# print(f"time elasped: {end - start}")
''' Réponse question 1 et 2
matrice = [["x" for _ in range(8)] for _ in range(8)]


for i in range(len(problem.nodes)):
    x, y = problem.nodes[i]
    matrice[x][y] = i+1
print(matrice)
'''
grid = None
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    lines = ''.join(lines)
    lines = lines.strip().splitlines()
    grid = list(map(lambda x: list(x.strip()), lines))

translate = {
    'a': '0', 'b': '1', 'c': '2', 'd': '3', 'e': '4',
    'f': '5', 'g': '6', 'h': '7', 'i': '8', 'j': '9'}
path = node.path()
print('Number of moves: ', str(node.depth))
visited = []
i = 0
for n in path:
    i += 1
    if visited:
        for let, coo in visited:
            x, y = coo
            grid[x][y] = translate[let]
    for k, (x, y) in n.state.sources.items():
        grid[x][y] = k
        if i == len(path):
            grid[x][y] = translate[k]
        visited.append((k, (x, y)))
    step = '\n'.join(''.join(row) for row in grid)
    print(step)
    print()
