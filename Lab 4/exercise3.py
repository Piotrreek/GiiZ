import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph


vertexNumber = 7

# graph = Graph.DirectedGraph.generateGraphWithProbability(vertexNumber,0.5)
# while(graph.Kosaraju(True) != 1):
#     #print("Ten digraf nie jest silnie spójny")
#     graph = Graph.DirectedGraph.generateGraphWithProbability(vertexNumber,0.3)
# graph.assignRandomWeightsToEdges(-1,10)
# graph.visualizeGraph("skierowany graf silnie spójny",withWeights= True)
# graph.BellmanFord(0) # czesto wyrzuca że w grafie jest cykl o ujemnej wadze

#przykłądowy graf z labow
graph = Graph.DirectedGraph(vertexNumber)
graph.readInitialData('adjmatrix.csv', Graph.MatrixTypes.ADJACENCYMATRIX)
graph.convertAdjMatrixToList()

graph.assignRandomWeightsToEdges(-5,10)
graph.visualizeGraph("skierowany graf z zad 1 wagi",withWeights= True)
graph.BellmanFord(0)
    