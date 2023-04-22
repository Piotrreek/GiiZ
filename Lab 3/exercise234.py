import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

# graph = Graph.NotDirectedGraph(12)
# graph.readInitialData('adjacencyList.csv', Graph.MatrixTypes.ADJACENCYLIST)
# graph.readWeightsFromCsv('weights.csv')
graph = Graph.NotDirectedGraph.generateRegularGraph(16, 4)
Graph.NotDirectedGraph.addRandomWeightsToGraph(graph)
print("Zadanie 2")
graph.Dijkstra(0, True)
print("\nZadanie 3")
graph.getMatrixOfDistances()
print("\nZadanie 4")
graph.getCenters()