import numpy as np
import random
import math
import matplotlib.pyplot as plt


def Plot_path(points, path,title):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'bo') 

    #rysuje ścieżki
    for i in range(len(path) - 1):
        plt.plot([points[path[i]][0], points[path[i+1]][0]], [points[path[i]][1], points[path[i+1]][1]], 'r-') 

    #łączy ostatni z pierwszym
    plt.plot([points[path[-1]][0], points[path[0]][0]], [points[path[-1]][1], points[path[0]][1]], 'r-')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.grid(True)
    plt.show()

def Calculate_distance(points, path):
    final_distance = 0
    for i in range(len(path) - 1):
        point1 = points[path[i]]
        point2 = points[path[i+1]]
        distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        final_distance += distance
    return final_distance

def Two_opt_swap(path, i, j):
    new_path = path[:]
    new_path[i:j+1] = reversed(path[i:j+1])
    return new_path

def Simulated_annealing(points, max_iterations):
    num_points = len(points)
    initial_path = list(range(num_points))

    # print("Początkowa ścieżka",initial_path)
    Plot_path(points, initial_path,"Startowa ścieżka")
    print("Długość startowej ścieżki:", Calculate_distance(points, initial_path))

    best_path = initial_path
    current_path = initial_path
    best_distance = Calculate_distance(points, initial_path)
    current_distance = best_distance

    #pętla chłodzenia
    for i in range(1000, 0, -1): 
        temperature = 0.001 * i**2  

        for it in range(max_iterations):
            a, b = random.sample(range(num_points), 2)
            c, d = random.sample(range(num_points), 2)

            # Sprawdzennie warunków
            while b == a or d == c or b == c or d == a:
                a, b = random.sample(range(num_points), 2)
                c, d = random.sample(range(num_points), 2)

            new_path = Two_opt_swap(current_path, min(a, b), max(a, b))
            new_path = Two_opt_swap(new_path, min(c, d), max(c, d))

            new_distance = Calculate_distance(points, new_path)

            if new_distance < current_distance:
                current_path = new_path
                current_distance = new_distance

                if new_distance < best_distance:
                    best_path = new_path
                    best_distance = new_distance
            else:
                acceptance_probability = math.exp((current_distance - new_distance) / temperature)
                if random.random() < acceptance_probability:
                    current_path = new_path
                    current_distance = new_distance

    return best_path





filename = "points.txt"
try:
    points = np.loadtxt(filename)
except IOError:
    print("Nie można wczytać danych z pliku", filename)
    exit()

# points = [(5, 6), (10, 2), (3, 4), (0, 0)]  
#print(points)


max_iterations = 1000

best_path = Simulated_annealing(points, max_iterations)

print("Najkrótsza znaleziona ścieżka:", best_path)
print("Długość najkrótszej ścieżki:", Calculate_distance(points, best_path))
Plot_path(points, best_path,"Najkrótsza ścieżka")