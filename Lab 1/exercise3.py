import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

g = Graph.Graph.generateGraph(7, 10)
g.visualizeGraph("graph-1")
g = Graph.Graph.generateGraphWithProbability(7, 0.5)
g.visualizeGraph("graph-2")