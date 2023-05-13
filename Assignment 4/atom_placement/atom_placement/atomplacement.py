#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Auguste Burlats <auguste.burlats@uclouvain.be>"""
from search import *


class AtomPlacement(Problem):

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        for i in range(len(state.sites)):
            for j in range(i + 1, len(state.sites)):
                if state.sites[i] != state.sites[j]:
                    new_state_sites = state.sites[:]
                    new_state_sites[i], new_state_sites[j] = new_state_sites[j], new_state_sites[i]
                    state_to_yield = State(
                        state.n_sites, state.n_types, state.edges, state.energy_matrix, sites=new_state_sites
                    )
                    yield ((i, j), state_to_yield)


    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def value(self, state):
        sum = 0
        for every_atom in state.edges:
            sum += state.energy_matrix[state.sites[every_atom[0]]][state.sites[every_atom[1]]]
        return sum



class State:

    def __init__(self, n_sites, n_types, edges, energy_matrix, sites=None):
        self.k = len(n_types)
        self.n_types = n_types
        self.n_sites = n_sites
        self.n_edges = len(edges)
        self.edges = edges
        self.energy_matrix = energy_matrix
        if sites is None:
            self.sites = self.build_init()
        else:
            self.sites = sites

    # an init state building is provided here but you can change it at will
    def build_init(self):
        sites = []
        for atom_type, quantity in enumerate(self.n_types):
            for i in range(quantity):
                sites.append(atom_type)

        return sites

    def __str__(self):
        s = ''
        for v in self.sites:
            s += ' ' + str(v)
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    n_sites = int(line.split(' ')[0])
    k = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    edges = []
    file.readline()

    n_types = [int(val) for val in file.readline().split(' ')]
    if sum(n_types) != n_sites:
        print('Invalid instance, wrong number of sites')
    file.readline()

    energy_matrix = []
    for i in range(k):
        energy_matrix.append([int(val) for val in file.readline().split(' ')])
    file.readline()

    for i in range(n_edges):
        edges.append([int(val) for val in file.readline().split(' ')])

    return n_sites, n_types, edges, energy_matrix


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100):
    current = LSNode(problem, problem.initial, 0)
    best = current
    l = limit
    while l > 0:
        next = current
        for node in list(next.expand()):
            if problem.value(node.state) < problem.value(next.state):
                next = node
                if problem.value(next.state) < problem.value(best.state):
                    best = next
        l -= 1
    return best


"""
    l = limit
    while l >0:
        current = None
        for node in list(current.expand()):
            if problem()
        
        l-=1
    
    front = list(current.expand())
    if front != None:
        for node in front:
            if problem.value(node.state) < problem.value(current.state):
                best = node
    
"""


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100):
    current = LSNode(problem, problem.initial, 0)
    best = current


    # Put your code here

    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2], info[3])
    ap_problem = AtomPlacement(init_state)
    step_limit = 100
    node = maxvalue(ap_problem, step_limit)
    state = node.state
    #print(ap_problem.value(state))
    #print(init_state.edges)
    #print(init_state.sites)
    #print(init_state.n_types)
    #print(node.state.sites)
    print(node.state.n_sites)
    print (state.__str__())