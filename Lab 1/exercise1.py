import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

g = [
[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
[0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
]

g2 = [
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
]

incG = Graph.Graph(12)
# incG.adjacencyMatrix = g
# incG.visualizeGraph('adjacency11vertexes')
# print('Initialized adjacency matrix:')
# incG.printAdjacencyMatrix()

incG.incidenceMatrix = g2
incG.visualizeGraph('incidence', Graph.MatrixTypes.INCIDENCEMATRIX)
print('Initialized incidence matrix:')
incG.printIncidenceMatrix()

print('\nIncidence matrix converted to adjacency matrix:')
incG.convertIncMatrixToAdjMatrix()
incG.printAdjacencyMatrix()

print('\nIncidence matrix converted to adjacency list:')
incG.convertIncMatrixToAdjList()
incG.printAdjacencyList()

print('\nAdjacency list converted to adjacency matrix:')
incG.convertAdjListToAdjMatrix()
incG.printAdjacencyMatrix()

print('\nAdjacency list converted to incidence matrix:')
incG.convertAdjListToIncMatrix()
incG.printIncidenceMatrix()

print('\nAdjacency matrix converted to adjacency list:')
incG.convertAdjMatrixToList()
incG.printAdjacencyList()

print('\nAdjacency matrix converted to incidence matrix:')
incG.convertAdjMatrixToIncMatrix()
incG.printIncidenceMatrix()