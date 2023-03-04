import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

class MatrixTypes(Enum):
    ADJACENCYMATRIX = 1
    INCIDENCEMATRIX = 2
    ADJACENCYLIST = 3

class Graph:    
    def __init__(self, vertexNumber):
        self.vertexNumber = vertexNumber
        self.vertexList = [n for n in range(vertexNumber)]
        # uzupelniam macierze zerami
        self.adjacencyMatrix = [[0 for _ in range(vertexNumber)] for _ in range(vertexNumber)]
        self.incidenceMatrix = [[0 for _ in range(vertexNumber)] for _ in range(vertexNumber)]
        # lista sasiedztwa zainicjalizowana jako mapa z kolejnymi wierzcholkami jako klucze
        # oraz pustymi listami jako wartosci
        self.adjacencyList = dict.fromkeys(range(vertexNumber), [])
        self.edges = []

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

    # macierz sasiedztwa -> macierz incydencji
    def convertAdjMatrixToIncMatrix(self):
        if not self.edges:
            self.getEdgesInAdjacencyMatrix()
        self.incidenceMatrix = np.zeros([self.vertexNumber + 1, len(self.edges)], dtype="int")
        print(f'Edges:\n{self.edges}')
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

    # wyliczanie krawedzi z poszczegolnych macierzy
    def getEdgesInIncidenceMatrix(self):
        for i in range(len(self.incidenceMatrix[0])):
            edge = []
            for j in range(len(self.incidenceMatrix)):
                if self.incidenceMatrix[j][i] == 1:
                    edge.append(j)
            if len(edge) == 2:
                self.edges.append(tuple(edge))

    def getEdgesInAdjacencyMatrix(self):
        for n in range(self.vertexNumber):
            for k in range(n + 1, self.vertexNumber):
                if self.adjacencyMatrix[n][k] == 1:
                        self.edges.append((n, k))
    
    def getEdgesInAdjacencyList(self):
        self.convertAdjListToAdjMatrix()
        self.getEdgesInAdjacencyMatrix()

    def getEdges(self, matrixType):
        if not self.edges:
            if matrixType == MatrixTypes.INCIDENCEMATRIX:
                self.getEdgesInIncidenceMatrix()
            elif matrixType == MatrixTypes.ADJACENCYLIST:
                self.getEdgesInAdjacencyList()
            self.getEdgesInAdjacencyMatrix()

    # zamiana w macierz sasiedztwa dowolnego z dwoch pozostalych typow w celu zwizualizowania macierzy
    def transformToAdjacencyMatrix(self, matrixType):
        if matrixType == MatrixTypes.INCIDENCEMATRIX:
            self.convertIncMatrixToAdjMatrix()
        elif matrixType == MatrixTypes.ADJACENCYLIST:
            self.convertAdjListToAdjMatrix()

    # generowanie grafu z zadana liczba wierzcholkow i krawedzi
    @staticmethod
    def generateGraph(vertexNumber, edgeNumber):
        if edgeNumber < 0 or edgeNumber > vertexNumber * (vertexNumber - 1) / 2:
            print("Number of edges is incorrect")
            exit()
        graph = Graph(vertexNumber)
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
        graph = Graph(vertexNumber)
        for n in range(vertexNumber):
            for k in range(vertexNumber - 1, n, - 1):
                if n == k:
                    continue
                if random.random() <= probability:
                    graph.addEdge(n, k)
        return graph