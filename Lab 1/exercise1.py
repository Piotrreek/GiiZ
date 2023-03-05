import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

incG = Graph.Graph()
# incG.readMatrixFromCsv('exampleMatrixAdjacency.csv', Graph.MatrixTypes.ADJACENCYMATRIX)
# incG.visualizeGraph('adjacency11vertexes')
# print('Initialized adjacency matrix:')
# incG.printAdjacencyMatrix()

incG.readInitialData('exampleMatrixIncidence.csv', Graph.MatrixTypes.INCIDENCEMATRIX)
incG.visualizeGraph('incidence', Graph.MatrixTypes.INCIDENCEMATRIX)
print('Initialized incidence matrix:')
incG.printIncidenceMatrix()

# incG.readInitialData('exampleAdjacencyList.csv', Graph.MatrixTypes.ADJACENCYLIST)
# incG.printAdjacencyList()
# incG.convertAdjListToAdjMatrix()
# incG.visualizeGraph('listToMatrix')

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