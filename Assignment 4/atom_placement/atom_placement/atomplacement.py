#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Auguste Burlats <auguste.burlats@uclouvain.be>"""
from search import *
import random


class AtomPlacement(Problem):

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions

    def successor(self, state):
        for i, site_i in enumerate(state.sites):
            for j, site_j in enumerate(state.sites):
                if i <= j : continue
                if site_i != site_j:
                    new_state_sites = state.sites.copy()
                    new_state_sites[i], new_state_sites[j] = new_state_sites[j], new_state_sites[i]
                    yield (i, j), State(
                        state.n_sites, state.n_types, state.edges, state.energy_matrix, sites=new_state_sites
                    )

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
    for i in range(limit):
        frontier = list(current.expand())
        if frontier is not None:
            next = frontier[0]
            for node in frontier:
                if problem.value(node.state) < problem.value(next.state):
                    next = node
            current = next
            if problem.value(current.state) < problem.value(best.state):
                best = current
    return best


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for _ in range(limit):
        frontier = list(current.expand())
        if frontier:
            frontier.sort(key=lambda node: problem.value(node.state), reverse=True)
            best5 = frontier[:min(5, len(frontier))]

            current = random.choice(best5)

            if problem.value(current.state) > problem.value(best.state):
                best = current
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
    #print(node.state.n_sites)
    print(node.value())
    #print(ap_problem.successor(state))
    #print(ap_problem.value(node.state))
    print (state.__str__())