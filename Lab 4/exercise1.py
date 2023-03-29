import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph
vertexNumber = 7

graph = Graph.DirectedGraph.generateGraphWithProbability(vertexNumber,0.3)
graph.visualizeGraph("skierowany graf 1")
