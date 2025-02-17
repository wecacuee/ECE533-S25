
import numpy as np
from dataclasses import dataclass
from functools import partial
from pprint import pprint

def depth_first_build_graph(
        k,
        xk,  # start state,
        Us,  # Possible control sets Uk per stage, so that uk ∈ Uk
        gs,  # Stage costs gk 
        fs,  # system dynamics fk(x, u) that predicts next state
        graph_adj_list # graph to be built as adjacency list
        ):
    assert len(Us) == len(gs) == len(fs)

    N = len(gs)
    if k >= N:
        return

    graph_adj_list.setdefault(k, {})
    graph_adj_list[k].setdefault(xk, [])
    for u in Us[k](xk):
        xkp1 = fs[k](xk, u)
        cost = gs[k](xk, u)
        # append all the information you might need
        # neighbor, cost of this edge, control of this edge, and the parent
        graph_adj_list[k][xk].append((xkp1, cost, u, xk))
        depth_first_build_graph(k+1, xkp1, Us, gs, fs, graph_adj_list)

def exactdp(x0,  # start state,
            Us,  # Possible control sets Uk per stage, so that uk ∈ Uk
            gs,  # Stage costs gk 
            fs,  # system dynamics fk(x, u) that predicts next state
            N    # Number of stages
            ):
    # forward pass to get all states as a directed graph.
    # We are going to represent graphs as adjacency lists
    k = 0
    graph_adj_list = {0 : {x0: []}}
    depth_first_build_graph(
        k,
        x0, 
        Us,
        gs,
        fs,
        graph_adj_list)
    pprint(graph_adj_list)


    COSTIDX = 1
    JN = {}
    for xN in graph_adj_list[N-1].keys():
        # there should be only one neighbor of the last state
        assert len(graph_adj_list[N-1][xN]) == 1, \
            (len(graph_adj_list),graph_adj_list[N-1],graph_adj_list[N-1][xN])
        JN[xN] = graph_adj_list[N-1][xN][0][COSTIDX]
    # Go over the directed graph backwards to apply the minimum cost-to-go
    # equation
    # Jk = min_u g(x, u)  + Jk+1(next_state)
    Js_reversed = [JN] # cost to go
    pis_reversed = [] # policy
    Js = []*N
    for k in range(N-2, -1, -1):
        Jkp1 = Js_reversed[-1] # pick the last J
        Jk = {} # Find the cost to go for each state
        pik = {} # policy
        min_so_far = np.inf
        best_u_so_far = "A"
        for xk in graph_adj_list[k].keys():
            for (xkp1, cost, u, xkrecalled) in graph_adj_list[k][xk]:
                assert xkrecalled == xk # should be the same
                costtogo = cost + Jkp1[xkp1]
                if min_so_far > costtogo:
                    min_so_far = costtogo
                    best_u_so_far = u
            Jk[xk] = min_so_far
            pik[xk] = best_u_so_far
        Js_reversed.append(Jk)
        pis_reversed.append(pik)
    #
    pis = list(reversed(pis_reversed))
    xk = x0
    us = []
    for k in range(N-1):
        print(pis[k], k, xk)
        uk = pis[k][xk]
        xkp1 = fs[k](xk, uk)
        us.append(uk)
        xk = xkp1
    return us

def next_state(allcities, xk, u):
    if len(xk) == len(allcities):
        return "A"
    else:
        return xk + u

def get_cost(travelling_costs, name2idx, xk, u):
    lastcity = xk[-1]
    lastcityidx = name2idx[lastcity]
    nextcity = u
    nextcityidx = name2idx[nextcity]
    return travelling_costs[lastcityidx][nextcityidx]

def remaining_controls(allcities, terminalcity, xk):
    # Find the possible cities that can be visited given that the state is xk
    if len(allcities) == len(xk): # visited all cities
        return terminalcity
    # Use Python setminus
    # https://docs.python.org/3/library/stdtypes.html#set.difference
    return list(set(allcities) - set(xk)) # return it as list

def make_travelling_salesman_problem():
    # all cities
    allcities = "ABCDE"
    # City names
    name2idx = dict(zip("ABCDE", [0, 1, 2, 3, 4]))
    # City travel matrix
    travelling_costs = [
            [0, 5, 1, 20, 10],
             [20, 0, 1, 4, 10],
             [1, 20, 0, 3, 10],
             [18, 4, 3, 0, 10],
             [30, 10, 0, 10, 0]
             ]
    N = 5
    x0 = "A"
    terminalcity = "A"
    Us = [partial(remaining_controls, allcities, terminalcity)]*(N)
    gs = [partial(get_cost, travelling_costs, name2idx)]*(N)
    fs = [partial(next_state, allcities)]*(N)
    exactdp(x0,  # start state,
            Us,  # Possible control sets Uk per stage, so that uk ∈ Uk
            gs,  # Stage costs gk 
            fs,  # system dynamics fk(x, u) that predicts next state
            N    # Number of stages
            )

if __name__ == '__main__':
    make_travelling_salesman_problem()
