import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import csv

class MatrixTypes(Enum):
    ADJACENCYMATRIX = 1
    INCIDENCEMATRIX = 2
    ADJACENCYLIST = 3
class Graph:
    def __init__(self, vertexNumber = 0):
        self.vertexNumber = vertexNumber
        self.vertexList = [n for n in range(vertexNumber)]
        # uzupelniam macierze zerami
        self.adjacencyMatrix = [[0 for _ in range(vertexNumber)] for _ in range(vertexNumber)]
        self.incidenceMatrix = [[0 for _ in range(vertexNumber)] for _ in range(vertexNumber)]
        # lista sasiedztwa zainicjalizowana jako mapa z kolejnymi wierzcholkami jako klucze
        # oraz pustymi listami jako wartosci
        self.adjacencyList = dict.fromkeys(range(vertexNumber), [])
        self.edges = []
        # tworzę macierz wag zainicjalizowaną wartoscia NaN
        self.weights = [["NaN" for _ in range(self.vertexNumber)] for _ in range(self.vertexNumber)]
    
    def readMatrixFromCsv(self, filePath, MatrixType):
        matrix = []
        with open(filePath, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                matrix.append([int(elem) for elem in row])
        self.vertexNumber = len(matrix)
        if MatrixType == MatrixTypes.ADJACENCYMATRIX:
            self.adjacencyMatrix = matrix
            if not self.incidenceMatrix:
                self.incidenceMatrix = [[0 for _ in range(self.vertexNumber)] for _ in range(self.vertexNumber)]
        elif MatrixType == MatrixTypes.INCIDENCEMATRIX:
            self.incidenceMatrix = matrix
            if not self.adjacencyMatrix:
                self.adjacencyMatrix = [[0 for _ in range(self.vertexNumber)] for _ in range(self.vertexNumber)]
     # WAZNE!
    # pierwszy element rzedu w pliku csv dla listy to numer krawedzi, reszta elementow to sasiedzi
    def readListFromCsv(self, filePath):
        adjacencyList = {}
        with open(filePath, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                key = int(row[0])
                values = [int(elem) for elem in row[1:]]
                adjacencyList[key] = values
        self.vertexNumber = len(adjacencyList)
        self.adjacencyList = adjacencyList

    def readInitialData(self, filePath, MatrixType):
        if MatrixType == MatrixTypes.ADJACENCYLIST:
            self.readListFromCsv(filePath)
        else:
            self.readMatrixFromCsv(filePath, MatrixType)
        self.weights = [["NaN" for _ in range(self.vertexNumber)] for _ in range(self.vertexNumber)]

    def addEdge(self, vertexFirst, vertexSecond):
        # dodaje krawedz do macierzy sasiedztwa
        self.adjacencyMatrix[vertexFirst][vertexSecond] = 1
        self.adjacencyMatrix[vertexSecond][vertexFirst] = 1

    def printAdjacencyMatrix(self):
        for row in self.adjacencyMatrix:
            print(row)

    def printAdjacencyList(self):
        for i in self.adjacencyList:
            print(i, self.adjacencyList[i])

    def printIncidenceMatrix(self):
        for row in self.incidenceMatrix:
            print(row)
    # macierz sasiedztwa -> lista sasiedztwa
    def convertAdjMatrixToList(self):
        adjacencyListRow = []
        for row in range(self.vertexNumber):
            for col in range(self.vertexNumber):
                if self.adjacencyMatrix[row][col] == 1:
                    adjacencyListRow.append(col)
            self.adjacencyList[row] = adjacencyListRow
            adjacencyListRow = []
    # macierz incydencji -> lista sasiedztwa
    def convertIncMatrixToAdjList(self):
        self.convertIncMatrixToAdjMatrix()
        self.convertAdjMatrixToList()
    # lista sasiedztwa -> macierz sasiedztwa
    def convertAdjListToAdjMatrix(self):
        for rowNum in self.adjacencyList:
            for colNum in self.adjacencyList[rowNum]:
                self.adjacencyMatrix[rowNum][colNum] = 1
    # lista sasiedztwa -> macierz incydencji
    def convertAdjListToIncMatrix(self):
        self.convertAdjListToAdjMatrix()
        self.convertAdjMatrixToIncMatrix()
    # wyliczanie krawedzi z poszczegolnych macierzy
    def getEdgesInIncidenceMatrix(self):
        for i in range(len(self.incidenceMatrix[0])):
            edge = []
            for j in range(len(self.incidenceMatrix)):
                if self.incidenceMatrix[j][i] == 1:
                    edge.append(j)
            if len(edge) == 2:
                self.edges.append(tuple(edge))

    def getEdgesInAdjacencyList(self):
        self.convertAdjListToAdjMatrix()
        self.getEdgesInAdjacencyMatrix()

    def getEdges(self, matrixType):
        if not self.edges:
            if matrixType == MatrixTypes.INCIDENCEMATRIX:
                self.getEdgesInIncidenceMatrix()
            elif matrixType == MatrixTypes.ADJACENCYLIST:
                self.getEdgesInAdjacencyList()
            else:
                self.getEdgesInAdjacencyMatrix()
    # zamiana w macierz sasiedztwa dowolnego z dwoch pozostalych typow w celu zwizualizowania macierzy
    def transformToAdjacencyMatrix(self, matrixType):
        if matrixType == MatrixTypes.INCIDENCEMATRIX:
            self.convertIncMatrixToAdjMatrix()
        elif matrixType == MatrixTypes.ADJACENCYLIST:
            self.convertAdjListToAdjMatrix()

class NotDirectedGraph(Graph):
   
    def readWeightsFromCsv(self, filePath):
        with open(filePath, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            r = -1
            for row in reader:
                w = -1 
                r += 1
                for weight in row:
                    w += 1
                    if weight != "NaN":
                        self.weights[r][w] = int(weight)
    # macierz sasiedztwa -> macierz incydencji
    def convertAdjMatrixToIncMatrix(self):
        if not self.edges:
            self.getEdgesInAdjacencyMatrix()
        self.incidenceMatrix = np.zeros([self.vertexNumber + 1, len(self.edges)], dtype="int")
        for i, edge in enumerate(self.edges):
            l, r = edge
            self.incidenceMatrix[l][i] = 1
            self.incidenceMatrix[r][i] = 1
        self.incidenceMatrix = self.incidenceMatrix[0:-1]
    # macierz incydencji -> macierz sasiedztwa
    def convertIncMatrixToAdjMatrix(self):
        num_edges = len(self.incidenceMatrix[0])
        for i in range(num_edges):
            edgeVertices = []
            for j in range(self.vertexNumber):
                if self.incidenceMatrix[j][i] == 1:
                    edgeVertices.append(j)
            self.adjacencyMatrix[edgeVertices[0]][edgeVertices[1]] = 1
            self.adjacencyMatrix[edgeVertices[1]][edgeVertices[0]] = 1
    # rysowanie jest na podstawie macierzy sasiedztwa robione wiec trzeba zaimplementowac wszystkie algorytmy zamiany
    # i jakoś dodać przekazywanie do programu wartosci z pliku ktore utworza graf z macierza sasiedztwa
    def visualizeGraph(self, name, matrixType=MatrixTypes.ADJACENCYMATRIX):
        self.getEdges(matrixType)
        self.transformToAdjacencyMatrix(matrixType)
        graph = nx.Graph()
        graph.add_nodes_from(self.vertexList)
        for edge in self.edges:
            graph.add_edge(edge[0], edge[1])
        nx.draw_circular(graph, with_labels = True)
        plt.savefig(name + ".png")
        plt.clf()
    def getEdgesInAdjacencyMatrix(self):
        for n in range(self.vertexNumber):
            for k in range(n + 1, self.vertexNumber):
                if self.adjacencyMatrix[n][k] == 1:
                        self.edges.append((n, k))

    # generowanie grafu z zadana liczba wierzcholkow i krawedzi
    @staticmethod
    def generateGraph(vertexNumber, edgeNumber):
        if edgeNumber < 0 or edgeNumber > vertexNumber * (vertexNumber - 1) / 2:
            print("Number of edges is incorrect")
            exit()
        graph = NotDirectedGraph(vertexNumber)
        possibilities = []
        for n in range(vertexNumber):
            for k in range(vertexNumber - 1, n, -1):
                if n != k:
                    possibilities.append((n, k))
        for n in range(edgeNumber):
            possibilitiesLength = len(possibilities)
            r = random.randint(0, possibilitiesLength - 1)
            (vertexFirst, vertexSecond) = possibilities.pop(r)
            graph.addEdge(vertexFirst, vertexSecond)
        return graph

    # generowanie grafu z zadania liczba wierzcholkow i danym prawdopodobienstwwem dla kazdej krawedzi
    @staticmethod
    def generateGraphWithProbability(vertexNumber, probability):
        if not (0 <= probability <= 1):
            print("Probabillity is wrong")
            exit()
        graph = NotDirectedGraph(vertexNumber)
        for n in range(vertexNumber):
            for k in range(vertexNumber - 1, n, - 1):
                if n == k:
                    continue
                if random.random() <= probability:
                    graph.addEdge(n, k)
        return graph

    # spójne składowe tworzymy z pomocą listy sąsiedztwa
    def components(self):
        nr = 0
        comp = [-1 for n in range(self.vertexNumber)]
        for n in range(self.vertexNumber):
            if comp[n] == -1:
                nr += 1
                comp[n] = nr
                self.components_R(nr, n, comp)
        return comp

    def components_R(self, nr, n, comp):
        for k in self.adjacencyList[n]:
            if comp[k] == -1:
                comp[k] = nr
                self.components_R(nr, k, comp)

    def maxComp(self, comp):
        numberOfComponents = max(comp)
        components = {}
        for n in range(numberOfComponents):
            components[n + 1] = []
        for n in range(self.vertexNumber):
            components[comp[n]].append(n)
        for key in components:
            print(str(key) + ")", components[key])
        maxComponent = max((len(v), k) for k,v in components.items())
        print("Najwieksza skladowa ma numer " + str(maxComponent[1]) + ".")
    
    def findBridges(self):
        visited = set()
        parent = {}
        dfs_numbers={}
        low = {}
        bridges = []

        def dfs(node, counter=0):
            visited.add(node)
            dfs_numbers[node] = counter
            low[node] = counter
            counter += 1
            for neighbor in self.adjacencyList[node]:
                if neighbor not in visited:
                    parent[neighbor] = node
                    dfs(neighbor, counter)
                    low[node] = min(low[node], low[neighbor])
                    if(low[node] == dfs_numbers[node] and parent[node] != None):
                        bridges.append((node,parent[node]))
                elif neighbor != parent.get(node, None):
                    low[node] = min(low[node], low[neighbor])
                elif (len(self.adjacencyList[node]) == 1 and low[node] == dfs_numbers[node] and parent[node] != None):
                        bridges.append((node,parent[node]))  

        counter = 1
        #in theory might be working on only one function call - but testing proves otherwise
        for node in self.adjacencyList:
            if node not in visited:
                parent[node] = None
                dfs(node, counter)
        return bridges
    
    def edgeIsBridge(self,edge):
            bridges = self.findBridges()
            for bridge in bridges:
                if(edge[0] == bridge[0] and edge[1] == bridge[1] or edge[0] == bridge[1] and edge[1] == bridge[0]):
                    return True
            return False
    
    def getEdgesFromVertex(self,vertex,edges):
        founded_edges =[]
        for edge in edges:    
            if(edge[0] == vertex or edge[1] == vertex):
                founded_edges.append(edge)
        return founded_edges
    #checks requirements on adjList works on edges
    def findEulerCycle(self):
        eulerCycle = []
        copyOfGraph = Graph(4)
        copyOfGraph = self
        #Checking requirements
        comp = self.components()
        if(max(comp) != 1):
            print("Graf nie jest spójny --> nie jest eulerowski")
            return
        for i in range(0,self.vertexNumber):
            if len(self.adjacencyList[i]) % 2 != 0:
                print("Nieparzysty stopień wierzchołka - graf nie jest eulerowski.")
                return
        
        start_vertex = 0
        current_vertex = start_vertex
        while(True):
            eulerCycle.append(current_vertex)
            if(len(self.getEdgesFromVertex(current_vertex,copyOfGraph.edges)) == 0):
                if(eulerCycle[0] == current_vertex):
                    print("Znaleziono cykl eulera")
                    return eulerCycle
                else:
                    print("Ten graf nie ma cyklu eulera")
                    return None
            for edge in self.getEdgesFromVertex(current_vertex,copyOfGraph.edges):
                if(copyOfGraph.edgeIsBridge(edge)):
                    if(len(self.getEdgesFromVertex(current_vertex,copyOfGraph.edges)) == 1):
                        if(current_vertex == edge[0]):
                            current_vertex = edge[1]
                        else:
                            current_vertex = edge[0]
                        copyOfGraph.edges.remove(edge)
                        copyOfGraph.transformToAdjacencyMatrix(MatrixTypes.ADJACENCYLIST)
                        copyOfGraph.adjacencyMatrix[edge[0]][edge[1]] = 0
                        copyOfGraph.adjacencyMatrix[edge[1]][edge[0]] = 0
                        copyOfGraph.convertAdjMatrixToList()
                        break
                else:
                    if(current_vertex == edge[0]):
                        current_vertex = edge[1]
                    else:
                        current_vertex = edge[0]
                    copyOfGraph.edges.remove(edge)
                    copyOfGraph.transformToAdjacencyMatrix(MatrixTypes.ADJACENCYLIST)
                    copyOfGraph.adjacencyMatrix[edge[0]][edge[1]] = 0
                    copyOfGraph.adjacencyMatrix[edge[1]][edge[0]] = 0
                    copyOfGraph.convertAdjMatrixToList()
                    break
    def isInTheList(self,list,firstElem,secondElem):
        for tup in list:
            if firstElem in tup and secondElem in tup:
                return True
        return False
    
    def init(self, vertexId):
        # definiuje tablice najkrotszych sciezek miedzy wierzcholkami oraz poprzednikow dla kazdego wierzcholka
        lengths = [1e10 for _ in range(self.vertexNumber)]
        predecessors = ["NIL" for _ in range(self.vertexNumber)] 
        # dlugosc wierzcholka do samego siebie jest rowna 0
        lengths[vertexId] = 0
        return lengths, predecessors
    
    def relax(self, u, v, weights, lengths, predecessors):
        if lengths[v] > lengths[u] + weights[u][v]:
            lengths[v] = lengths[u] + weights[u][v]
        predecessors[v] = u

    def Dijkstra(self, vertexId, shouldPrint = False):
        lengths, predecessors = self.init(vertexId)
        S = []
        while len(S) != self.vertexNumber:
            notReadyVertexes = [vertex for vertex in self.vertexList if vertex not in S]
            u = min(notReadyVertexes, key=lambda x: lengths[x])
            S.append(u)
            neighboursOfVertexU = [vertex for vertex in self.adjacencyList[u] if vertex not in S]
            for vertex in neighboursOfVertexU:
                self.relax(u, vertex, self.weights, lengths, predecessors)
        if shouldPrint:
            print(f'START: s = {vertexId}')
            for vertex in range(self.vertexNumber):
                print(f'd({vertex}) = {lengths[vertex]} ==>', end=' ')
                print('[', end='')
                path = [vertex]
                precedessor = predecessors[vertex]
                while precedessor != "NIL":
                    path.append(precedessor)
                    precedessor = predecessors[precedessor]
                path = path[::-1]
                for val in path:
                    if(val != path[-1]):
                        print(f'{val} - ', end='')
                    else:
                        print(f'{val}]')
        return lengths

    def getMatrixOfDistances(self):
        distances = []
        for vertex in range(self.vertexNumber):
            distancesRow = self.Dijkstra(vertex)
            distances.append(distancesRow)
        for row in distances:
            for dist in row:
                print("%2d " % (dist), end='')
            print()
            
    def getCenters(self):
        distances = []
        for vertex in range(self.vertexNumber):
            distancesRow = self.Dijkstra(vertex)
            distances.append(distancesRow)
        center = distances.index(min(distances, key=lambda x: sum(x)))
        print(f'Centrum = {center} (suma odleglosci: {sum(distances[center])})')
        minimax = distances.index(min(distances, key=lambda x: max(x)))
        print(f'Centrum minimax = {minimax} (odleglosc od najdalszego: {max(distances[minimax])})')

    def getMST(self):
        edgesToWeightsOfEdges = self.getEdgesToWeightsOfEdgesDict()
        sets = {v: set([v]) for edge in edgesToWeightsOfEdges for v in edge}
        mst = []
        for edge in edgesToWeightsOfEdges:
            # sprawdzamy czy wierzcholki nalezace do krawedzi naleza do roznych zbiorow
            if sets[edge[0]] != sets[edge[1]]:
                mst.append(edge)
                # laczymy zbiory wierzcholkow
                set1 = sets[edge[0]]
                set2 = sets[edge[1]]
                union = set1.union(set2)
                for v in union:
                    sets[v] = union
        return mst


    def getEdgesToWeightsOfEdgesDict(self):
        edgesToWeightsOfEdges = {}
        for j in range(len(self.weights)):
            for i in range(len(self.weights[j])):
                if (not (j,i) in edgesToWeightsOfEdges) and j!=i and self.weights[i][j] != 0:
                    edgesToWeightsOfEdges[(i,j)] = self.weights[i][j]
        return {k: v for k, v in sorted(edgesToWeightsOfEdges.items(), key=lambda item: item[1])}

    @staticmethod
    def isHamiltonian(adjList, matrixType):
        vertexNum = len(adjList) 
        visited = [False] * vertexNum 
        path = [] 
        graph = Graph()
        graph.setAdjList(adjList, matrixType, graph)

        def dfs(vertex):
            visited[vertex] = True
            path.append(vertex)

            if len(path) == vertexNum:
                if path[-1] in graph.adjacencyList[path[0]]: 
                    return True
                else:
                    visited[vertex] = False
                    path.pop()
                    return False

            for neighbor in graph.adjacencyList[vertex]:
                if not visited[neighbor]:
                    if dfs(neighbor):
                        return True

            visited[vertex] = False
            path.pop()
            return False

        for startVertex in range(vertexNum):
            if dfs(startVertex):
                return True

        return False
    @staticmethod
    def generateEulerGraph(vertexNumber):
        graph = NotDirectedGraph(vertexNumber)
        edges = []
        vertDeg = []
        for vertex in range(0,vertexNumber): 
            random_even_number = random.randint(1,(vertexNumber-1)//2) * 2
            vertDeg.append(random_even_number)
        vertDegCopy = vertDeg.copy()
        for vertex in range(0,vertexNumber):
            for k in range(vertDeg[vertex]):
                counter = 0
                for i in range(0,vertexNumber):
                    if(not graph.isInTheList(edges,vertex,i) and vertDeg[i] >= 1 and i != vertex):
                        counter += 1
                if(counter == 0):
                    print("tego grafu nie da się stworzyć - reset")
                    return None
                while True:
                    random_vertex = random.randint(0, vertexNumber-1)
                    if(graph.isInTheList(edges,vertex,random_vertex)):
                      continue
                    if(random_vertex != vertex and vertDeg[random_vertex] >= 1):
                        edges.append((vertex, random_vertex))
                        vertDeg[vertex] -= 1
                        vertDeg[random_vertex] -= 1
                        break         
        for n in range(len(edges)):
            graph.addEdge(edges[n][0],edges[n][1])
        graph.getEdgesInAdjacencyMatrix()
        graph.convertAdjMatrixToList()
        print("Stworzono graf Eulerowski")
        print("Stopnie wierzchołków: ",vertDegCopy)
        return graph
    @staticmethod
    def generateRegularGraph(vertexNumber,vertexDegree,name):
        #Checking requirements
        if(vertexNumber <= vertexDegree or (vertexDegree % 2 == 1 and vertexNumber % 2 ==1)):
            print("Warunki nie są spełnione")
            return 
        sequence = []
        for i in range (vertexNumber):
            sequence.append(vertexDegree)
        NotDirectedGraph.generateGraphFromDegreeSequence2(sequence,name)
        #randomizacja
        #brak kodu
    @staticmethod
    def setAdjList(adjList, matrixType, graph):
        if matrixType == MatrixTypes.ADJACENCYMATRIX:
            graph.adjacencyMatrix = adjList
            graph.getEdges(matrixType)
            graph.convertAdjMatrixToList()
        elif matrixType == MatrixTypes.INCIDENCEMATRIX:
            graph.incidenceMatrix = adjList
            graph.getEdges(matrixType)
            graph.convertIncMatrixToList()
        else: 
            graph.adjacencyList = adjList

    @staticmethod
    def checkIfDegreeSequenceIsGraphic(arr, show=False):
        while True:

            arr.sort(reverse=True)

            if show:
                print(arr)

            if arr[0] == 0 and arr[len(arr)-1] == 0:
                return True

            first = arr[0]
            arr = arr[1:]

            if first > len(arr):
                return False

            for i in range(first):
                arr[i] -= 1

                if arr[i] < 0:
                    return False

    @staticmethod
    def generateGraphFromDegreeSequence(arr, name):
        if NotDirectedGraph.checkIfDegreeSequenceIsGraphic(arr):
            n = len(arr)
            arr.sort(reverse=True)
            mat = [[0] * n for i in range(n)]

            for i in range(n):
                for j in range(i + 1, n):

                    # For each pair of vertex decrement
                    # the degree of both vertex.
                    if (arr[i] > 0 and arr[j] > 0):
                        arr[i] -= 1
                        arr[j] -= 1
                        mat[i][j] = 1
                        mat[j][i] = 1

            with open('mat.csv', 'w', newline='') as file:
                writer = csv.writer(file)

                for i in range(n):
                    row = []
                    for j in range(n):
                        row.append(mat[i][j])
                    writer.writerow(row)

            graph = NotDirectedGraph()
            graph.readMatrixFromCsv('mat.csv', MatrixType=MatrixTypes.ADJACENCYMATRIX)
            graph.visualizeGraph(name)
        else:
            print("Given degree sequence is not graphic")
    #new version old examples now working this is overcomplicated because I didn't see error earlier and I am to tired to go back to easier implementations
    @staticmethod 
    def generateGraphFromDegreeSequence2(arr, name):
        if NotDirectedGraph.checkIfDegreeSequenceIsGraphic(arr):
            n = len(arr)
            arr.sort(reverse=True)
            mat = [[0] * n for i in range(n)]
            
            vertexValue = []
            for i in range (n):
                vertexValue.append((i,arr[i]))
            max_tuple = vertexValue[0]
            while(True):
                for j in range(1, n):

                    # For each pair of vertex decrement
                    # the degree of both vertex.
                    if (arr[0] > 0 and arr[j] > 0):
                        arr[0] -= 1
                        arr[j] -= 1
                        for tup in vertexValue:
                            if (tup[1] == (arr[j]+1) and tup[0] != max_tuple[0]):
                                tuple_number = tup[0]
                                break
                        mat[max_tuple[0]][tuple_number] = 1
                        mat[tuple_number][max_tuple[0]] = 1
                        vertexValue[tuple_number] = (vertexValue[tuple_number][0],vertexValue[tuple_number][1]-1)
                vertexValue[max_tuple[0]] = (vertexValue[max_tuple[0]][0],0)
                arr.sort(reverse=True)
                max_value = -1
                for tup in vertexValue:
                    if tup[1] > max_value:
                        max_value = tup[1]
                        max_tuple = tup
                if(arr[0] == 0):
                    break
            with open('mat.csv', 'w', newline='') as file:
                writer = csv.writer(file)

                for i in range(n):
                    row = []
                    for j in range(n):
                        row.append(mat[i][j])
                    writer.writerow(row)

            graph = NotDirectedGraph()
            graph.readMatrixFromCsv('mat.csv', MatrixType=MatrixTypes.ADJACENCYMATRIX)
            graph.visualizeGraph(name)
        else:
            print("Given degree sequence is not graphic")
class DirectedGraph(Graph):
    # macierz incydencji -> macierz sasiedztwa
    def convertIncMatrixToAdjMatrix(self):
        num_edges = len(self.incidenceMatrix[0])
        for i in range(num_edges):
            edgeVertices = [0,0]
            for j in range(self.vertexNumber):
                if (self.incidenceMatrix[j][i] == -1 ):
                    edgeVertices[0] = j
                elif (self.incidenceMatrix[j][i] == 1 ):
                    edgeVertices[1] = j
                
            self.adjacencyMatrix[edgeVertices[0]][edgeVertices[1]] = 1
    #macierz sąsiedztwa -> macierz incydencji
    def convertAdjMatrixToIncMatrix(self):
        if not self.edges:
            self.getEdgesInAdjacencyMatrix()
        self.incidenceMatrix = np.zeros([self.vertexNumber + 1, len(self.edges)], dtype="int")
        print(f'Edges:\n{self.edges}')
        for i, edge in enumerate(self.edges):
            l, r = edge
            self.incidenceMatrix[l][i] = -1
            self.incidenceMatrix[r][i] = 1
        self.incidenceMatrix = self.incidenceMatrix[0:-1]
    def getEdgesInAdjacencyMatrix(self):
        for n in range(self.vertexNumber):
            for k in range(self.vertexNumber):
                if self.adjacencyMatrix[n][k] == 1:
                        self.edges.append((n, k))
     # rysowanie jest na podstawie macierzy sasiedztwa robione wiec trzeba zaimplementowac wszystkie algorytmy zamiany
    #różni się tylko jedną linijką od nieskierowanego można wrzucić do części wspólnej z argumentem który decyduje czy skierowany czy nie
    def visualizeGraph(self, name, matrixType=MatrixTypes.ADJACENCYMATRIX):
        self.getEdges(matrixType)
        self.transformToAdjacencyMatrix(matrixType)
        graph = nx.DiGraph()
        graph.add_nodes_from(self.vertexList)
        for edge in self.edges:
            graph.add_edge(edge[0], edge[1])
        nx.draw_circular(graph, with_labels = True)
        plt.savefig(name + ".png")
        plt.clf()
    #wymaga adjlist
    def Kosaraju(self):
        visit = [] #czas odwiedzenia
        final = []  #czas przetworzen
        comp = [] # numer silnie spójnej składowej 
        order = [] # wierczhołki w kolejności przetworzenia w dół
        for i in range (self.vertexNumber):
            visit.append(-1)
            final.append(-1)

        t = [0]
        for i in range (self.vertexNumber):
            if(visit[i] == -1):
                self.DFS_visit(visit,final,i,t)
       
        graphInverted = DirectedGraph(self.vertexNumber)
        for i in range(self.vertexNumber):
            for j in range(self.vertexNumber):
                if(self.adjacencyMatrix[i][j] == 1):
                    graphInverted.adjacencyMatrix[j][i] = 1   
        #graphInverted.visualizeGraph("skierowany graf odwrotny")
        nr = 0
        for i in range(graphInverted.vertexNumber):
            comp.append(-1)

        graphInverted.convertAdjMatrixToList()
        indeksy = sorted(range(len(final)), key=lambda i: final[i], reverse=True)
        for i in indeksy:
            if(comp[i] == -1):
                nr += 1
                comp[i] = nr
                graphInverted.components_r(nr,i,comp)
        
        components = {}
        for i, x in enumerate(comp):
            if x not in components:
                components[x] = []
            components[x].append(i)
        print("Ten graf ma {} składowe:".format(len(components)))
        print(components)
    #works on adjlist      
    def DFS_visit(graph,visit,final,vert,t2):
            t2[0] += 1
            visit[vert] = t2[0]
            for vertex in graph.adjacencyList[vert]:
                if(visit[vertex] == -1):
                    graph.DFS_visit(visit,final,vertex,t2)
            t2[0] += 1
            final[vert] = t2[0]
    #works on adjlist  
    def components_r(graph,nr,vert,comp):
        for vertex in graph.adjacencyList[vert]:
            if(comp[vertex] == -1):
                comp[vertex] = nr
                graph.components_r(nr,vertex,comp)
    @staticmethod
    def generateGraphWithProbability(vertexNumber, probability):
        if not (0 <= probability <= 1):
            print("Probabillity is wrong")
            exit()
        graph = DirectedGraph(vertexNumber)
        for n in range(vertexNumber):
            for k in range(vertexNumber - 1, n, - 1):
                if n == k:
                    continue
                if random.random() <= probability:
                    graph.addEdge(n, k)
        #print(graph.edges)
        #graph.printAdjacencyMatrix()
        return graph