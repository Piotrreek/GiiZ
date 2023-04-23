import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

# przyklad z laboratoriow z prezentacji
g = Graph.DirectedGraph(3)
g.readInitialData('adjListEx4.csv', Graph.MatrixTypes.ADJACENCYLIST)
g.readWeightsFromCsv('ex4weights.csv')
print(Graph.DirectedGraph.johnsonAlgorithm(g))

# przyklad z https://www.javatpoint.com/johnsons-algorithm
g = Graph.DirectedGraph(4)
g.readInitialData('adjListEx4v2.csv', Graph.MatrixTypes.ADJACENCYLIST)
g.readWeightsFromCsv('ex4weights2.csv')
print(Graph.DirectedGraph.johnsonAlgorithm(g))