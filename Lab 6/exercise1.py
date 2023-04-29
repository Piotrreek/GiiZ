import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

graph = Graph.DirectedGraph(12)

#przykladowe wejscie z upela
graph.readInitialData('adjlist.csv', Graph.MatrixTypes.ADJACENCYLIST)

print("Metoda bladzenia losowego:")
graph.pageRankRandomMethod(0, 0.15, 1000000)

print("\nMetoda iteracji wektora obsadzen:")
graph.pageRankIterationMethod(12, 0.15, 1e-8)