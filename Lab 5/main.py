#!/usr/bin/env python3
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


import random
import numpy as np


def generate_flow_matrix(N, draw=False, file_name=""):
    # generowanie ilości węzłów w warstwie
    layers_size = [random.randint(2, 5) for _ in range(N)]

    # tworzenie macierzy o rozmiarze (N+2) x (N+2) (dodatkowo 2 dla źródła i ujścia)
    size = sum(layers_size) + 2
    flow_matrix = np.zeros((size, size), dtype=int)

    # tworenie połączeń pomiędzy żródłem a pierwszą warstwą
    for i in range(1, layers_size[0] + 1):
        capacity = random.randint(1, 10)
        flow_matrix[0][i] = capacity

    # tworzenie połączeń pomiędzy poszczególnymi warstwami
    node_counter = 1
    iter_num = 1
    for k in range(N):
        down = node_counter
        up = sum(layers_size[0:iter_num]) + 1
        for i in range(down, up):
            _down = sum(layers_size[0:iter_num]) + 1
            _up = sum(layers_size[0:iter_num + 1]) + 1
            for j in range(_down, _up):
                capacity = random.randint(1, 10)
                flow_matrix[i][j] = capacity

        node_counter += layers_size[iter_num-1]
        iter_num += 1

    # tworzenie połączeń między ostatnią warstwą a żródłem
    for i in range(sum(layers_size) - layers_size[N-1] + 1, sum(layers_size) + 1):
        capacity = random.randint(1, 10)
        flow_matrix[i][size - 1] = capacity

    # usuwanie losowych 2*N połączeń
    down = 1
    up = sum(layers_size) - 1
    deleted_connections_count = 0
    while deleted_connections_count <= 2 * N:

        random_node_one = random.randint(down, up)
        random_node_two = random.randint(down, up)

        if flow_matrix[random_node_one][random_node_two] != 0:
            flow_matrix[random_node_one][random_node_two] = 0
            deleted_connections_count += 1

    # generowanie 2*N dodatkowych połączeń
    down = 1
    up = sum(layers_size) - 1
    new_connections_count = 0
    while new_connections_count <= 2*N:

        random_node_one = random.randint(down, up)
        random_node_two = random.randint(down, up)

        if random_node_one == random_node_two:
            continue

        if flow_matrix[random_node_one][random_node_two] == 0 and flow_matrix[random_node_two][random_node_one]:
            capacity = random.randint(1, 10)
            flow_matrix[random_node_one][random_node_two] = capacity
            new_connections_count += 1

    # generowanie obrazka
    if draw:
        Graph = nx.DiGraph()
        labels = {}

        for i in range(0, len(flow_matrix)):
            Graph.add_node(i)

        for i in range(len(flow_matrix)):
            for j in range(len(flow_matrix)):
                if (flow_matrix[i][j] > 0 and Graph.has_edge(j, i) == False):
                    Graph.add_edge(i, j)

        nx.draw(Graph, pos=nx.circular_layout(Graph), with_labels=True)

        for i in range(len(flow_matrix)):
            for j in range(len(flow_matrix)):
                if (flow_matrix[i][j] > 0):
                    labels[(i, j)] = str(str(flow_matrix[i][j]))

        nx.draw_networkx_edge_labels(Graph, nx.circular_layout(Graph), labels)
        plt.savefig(file_name + ".png")
        plt.clf()

    return flow_matrix


def bfs(flows, s, t, parents):
    visited = []
    for _ in range(len(flows)):
        visited.append(False)

    Q = deque()
    Q.append(s)
    visited[s] = True

    while Q:
        u=Q.popleft()
        for v in range(len(flows)):
            if visited[v] == False and flows[u][v] > 0:
                Q.append(v)
                visited[v] = True
                parents[v] = u
                if v == t:
                    return True

    return False

def EdmondsKarpAlgorithm(flows, s, t, fileName):
    parents = []
    residual_capacity = [[0] * len(flows) for _ in range(len(flows))]

    for u in range(len(flows)):
        for v in range(len(flows)):
            residual_capacity[u][v] = flows[u][v]

    for i in range(len(flows)):
        parents.append(-1)

    maxFlow = 0

    while (bfs(residual_capacity,s,t,parents)):
        flowPath = float("Inf")
        val = t
        while val != s:
            flowPath = min(flowPath, residual_capacity[parents[val]][val])
            val = parents[val]
        maxFlow = maxFlow + flowPath

        vertex = t
        while vertex != s:
            u = parents[vertex]
            residual_capacity[u][vertex] = residual_capacity[u][vertex] - flowPath
            residual_capacity[vertex][u] = residual_capacity[vertex][u] + flowPath
            vertex = parents[vertex]

    print("Maksymalny przepływ wynosi:" + str(maxFlow))

    for i in range(len(residual_capacity)):
        print(residual_capacity[i])

    Graph = nx.DiGraph()
    labels = {}

    for i in range(0, len(flows)):
        Graph.add_node(i)

    for i in range(len(flows)):
        for j in range(len(flows)):
            if(flows[i][j] > 0 and Graph.has_edge(j,i) == False):
                Graph.add_edge(i, j)

    nx.draw(Graph, pos = nx.circular_layout(Graph), with_labels = True)

    for i in range(len(flows)):
        for j in range(len(flows)):
            if(flows[i][j] > 0):
                labels[(i, j)]=str(str(residual_capacity[j][i]) + "/" + str(flows[i][j]))

    nx.draw_networkx_edge_labels(Graph,nx.circular_layout(Graph), labels)
    plt.savefig(fileName + ".png")
    plt.clf()

    return maxFlow

# flowsMatrix=[
#     [0,10,3,6,0,0,0,0,0,0,0],
#     [0,0,8,0,8,6,0,0,0,0,0],
#     [0,0,0,0,0,2,10,0,0,0,0],
#     [0,0,0,0,1,0,10,0,0,0,0],
#     [0,0,0,0,0,0,0,0,5,0,0],
#     [0,0,0,0,1,0,0,0,0,7,0],
#     [0,0,0,0,0,0,0,9,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,7],
#     [0,0,0,0,0,0,8,1,0,0,5],
#     [0,0,0,0,0,0,0,0,0,0,7],
#     [0,0,0,0,0,0,0,0,0,0,0]
# ]


EdmondsKarpAlgorithm(generate_flow_matrix(3), 0, 10, "test")
