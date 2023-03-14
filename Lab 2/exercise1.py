import Graph

graph = Graph.Graph()

sequence1 = [1, 3, 2, 3, 2, 4, 1]
print(sequence1, end=' ')
print("is graphic sequence" if Graph.Graph.checkIfDegreeSequenceIsGraphic(sequence1) else "is not graphic sequence")

sequence2 = [1, 3, 3, 4, 2, 3, 1]
print(sequence2, end=' ')
print("is graphic sequence" if Graph.Graph.checkIfDegreeSequenceIsGraphic(sequence2) else "is not graphic sequence")

sequence3 = [1, 3, 3, 7, 2, 3, 1]
print(sequence3, end=' ')
print("is graphic sequence" if Graph.Graph.checkIfDegreeSequenceIsGraphic(sequence2) else "is not graphic sequence")

sequence4 = [3, 3, 3, 3]
print(sequence4, end=' ')
print("is graphic sequence" if Graph.Graph.checkIfDegreeSequenceIsGraphic(sequence4) else "is not graphic sequence")

Graph.Graph.generateGraphFromDegreeSequence([1, 3, 2, 3, 2, 4, 1], "graph1")
Graph.Graph.generateGraphFromDegreeSequence([1, 3, 3, 4, 2, 3, 1], "graph2")
Graph.Graph.generateGraphFromDegreeSequence([3, 3, 3, 3], "graph3")