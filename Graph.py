import random
import networkx as nx
import matplotlib.pyplot as plt

class Graph:    
    def __init__(self, vertexNumber):
        self.vertexNumber = vertexNumber
        self.vertexList = [n for n in range(vertexNumber)]
        # uzupelniam macierz sasiedztwa zerami
        self.adjacencyMatrix = [[0 for i in range(vertexNumber)] for j in range(vertexNumber)]
    def addEdge(self, vertexFirst, vertexSecond):
        # dodaje krawedz do macierzy sasiedztwa
        self.adjacencyMatrix[vertexFirst][vertexSecond] = 1
        self.adjacencyMatrix[vertexSecond][vertexFirst] = 1
    def printAdjacencyMatrix(self):
        for row in self.adjacencyMatrix:
            print(row)
    # rysowanie jest na podstawie macierzy sasiedztwa robione wiec trzeba zaimplementowac wszystkie algorytmy zamiany
    # i jakoś dodać przekazywanie do programu wartosci z pliku ktore utworza graf z macierza sasiedztwa
    def visualizeGraph(self, name):
        graph = nx.Graph()
        graph.add_nodes_from(self.vertexList)
        for n in range(self.vertexNumber):
            for k in range(n + 1, self.vertexNumber):
                if self.adjacencyMatrix[n][k] == 1:
                    graph.add_edge(n, k)
        nx.draw_circular(graph, with_labels = True)
        plt.savefig(name + ".png")
        plt.clf()
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
    