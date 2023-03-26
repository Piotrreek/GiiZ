import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Graph

#graph = Graph.Graph(4)
#graph.readInitialData('euler.csv', Graph.MatrixTypes.ADJACENCYLIST)
# graph.convertAdjListToAdjMatrix()
# graph.visualizeGraph("ex4")
# #graph.findBridges()
# cycle = graph.findEulerCycle()
# if(cycle is not None):
#     print(cycle)
vertexNumber = 5

g = Graph.Graph.generateEulerGraph(vertexNumber)
while(g is None):
    g = Graph.Graph.generateEulerGraph(vertexNumber)
if(g is not  None):
    g.convertAdjListToAdjMatrix()
    #print(g.edges)
    g.visualizeGraph("ex4")
cycle = g.findEulerCycle()
print(cycle)