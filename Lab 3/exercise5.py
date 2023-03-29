import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

print('Przyklad 1:')
graph = Graph.NotDirectedGraph(12)
graph.readWeightsFromCsv('weights.csv')
print(graph.getMST())

print('\nPrzyklad 2 - z prezentacji:')
graph2 = Graph.NotDirectedGraph(7)
graph2.readWeightsFromCsv('weights2.csv')
print(graph2.getMST())

print('\nPrzyklad 3 - https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/:')
graph3 = Graph.NotDirectedGraph(9)
graph3.readWeightsFromCsv('weights3.csv')
print(graph3.getMST())  