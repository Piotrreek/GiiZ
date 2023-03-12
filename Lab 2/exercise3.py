import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

graph = Graph.Graph()

graph.readInitialData('list.csv', Graph.MatrixTypes.ADJACENCYLIST)
#graph.printAdjacencyList()
comp = graph.components()
graph.maxComp(comp)