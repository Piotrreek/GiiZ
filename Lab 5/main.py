#!/usr/bin/env python3
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

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

flowsMatrix=[
    [0,10,3,6,0,0,0,0,0,0,0],
    [0,0,8,0,8,6,0,0,0,0,0],
    [0,0,0,0,0,2,10,0,0,0,0],
    [0,0,0,0,1,0,10,0,0,0,0],
    [0,0,0,0,0,0,0,0,5,0,0],
    [0,0,0,0,1,0,0,0,0,7,0],
    [0,0,0,0,0,0,0,9,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,7],
    [0,0,0,0,0,0,8,1,0,0,5],
    [0,0,0,0,0,0,0,0,0,0,7],
    [0,0,0,0,0,0,0,0,0,0,0]
]
EdmondsKarpAlgorithm(flowsMatrix, 0, 10, "lab5z2")
