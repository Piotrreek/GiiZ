import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph
vertexNumber = 7

#h = Graph.DirectedGraph.generateGraphWithProbability(vertexNumber,0.5)
graph = Graph.DirectedGraph(vertexNumber)
graph.readInitialData('adjmatrix.csv', Graph.MatrixTypes.ADJACENCYMATRIX)
graph.convertAdjMatrixToList()
graph.visualizeGraph("skierowany graf test")
graph.Kosaraju()