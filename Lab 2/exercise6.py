import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

graph = Graph.NotDirectedGraph()
print(Graph.NotDirectedGraph.isHamiltonian({0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}, Graph.MatrixTypes.ADJACENCYLIST)) #hamiltonowski

graph.readInitialData('list.csv', Graph.MatrixTypes.ADJACENCYLIST)
print(Graph.NotDirectedGraph.isHamiltonian(graph.adjacencyList, Graph.MatrixTypes.ADJACENCYLIST))

graph.readInitialData('exampleAdjacencyList.csv', Graph.MatrixTypes.ADJACENCYLIST)
print(Graph.NotDirectedGraph.isHamiltonian(graph.adjacencyList, Graph.MatrixTypes.ADJACENCYLIST))

print(Graph.NotDirectedGraph.isHamiltonian({0: [2, 4, 5], 1: [3,4,5], 2: [0,4], 3: [1,4], 4: [0,1,2,3], 5:[0,1]}, Graph.MatrixTypes.ADJACENCYLIST)) #hamiltonowski

print(Graph.NotDirectedGraph.isHamiltonian({0: [1,2,3], 1:[0,2,3], 2:[0,1,3], 3:[0,1,2,4,5], 4:[3,5], 5:[3,4]}, Graph.MatrixTypes.ADJACENCYLIST)) #niehamiltonowski

print(Graph.NotDirectedGraph.isHamiltonian({0: [1,3,4], 1: [0, 2, 4], 2: [1, 3, 4, 5], 3: [0, 2, 4], 4: [0, 1, 2, 3], 5: [2]}, Graph.MatrixTypes.ADJACENCYLIST)) #niehamiltonowski