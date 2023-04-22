import Graph

graph = Graph.NotDirectedGraph()

sequence1 = [1, 3, 2, 3, 2, 4, 1]
print(sequence1, end=' ')
print("is graphic sequence" if Graph.NotDirectedGraph.checkIfDegreeSequenceIsGraphic(sequence1) else "is not graphic sequence")

sequence2 = [1, 3, 3, 4, 2, 3, 1]
print(sequence2, end=' ')
print("is graphic sequence" if Graph.NotDirectedGraph.checkIfDegreeSequenceIsGraphic(sequence2) else "is not graphic sequence")

sequence3 = [1, 3, 3, 7, 2, 3, 1]
print(sequence3, end=' ')
print("is graphic sequence" if Graph.NotDirectedGraph.checkIfDegreeSequenceIsGraphic(sequence2) else "is not graphic sequence")

sequence4 = [3, 3, 3, 3]
print(sequence4, end=' ')
print("is graphic sequence" if Graph.NotDirectedGraph.checkIfDegreeSequenceIsGraphic(sequence4) else "is not graphic sequence")

Graph.NotDirectedGraph.generateGraphFromDegreeSequence([1, 3, 2, 3, 2, 4, 1], True, "graph_from_sequence1")
Graph.NotDirectedGraph.generateGraphFromDegreeSequence([4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2], True, "graph_from_sequence2")