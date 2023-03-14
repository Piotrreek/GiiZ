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
            else:
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

        if Graph.checkIfDegreeSequenceIsGraphic(arr):
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

            graph = Graph()
            graph.readMatrixFromCsv('mat.csv', MatrixType=MatrixTypes.ADJACENCYMATRIX)
            graph.visualizeGraph(name)
        else:
            print("Given degree sequence is not graphic")


