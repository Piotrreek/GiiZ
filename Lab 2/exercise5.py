import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

vertexNumber = 7
vertexDegree = 2

g = Graph.NotDirectedGraph.generateRegularGraph(vertexNumber,vertexDegree,True,"regular")

