import numpy as np
from itertools import permutations
import os
import pandas as pd
import matplotlib.pyplot as plt

def shortest_path(points):
    """
    Calculates the shortest possible path through a set of 2D points using brute force.

    Args:
        points (np.ndarray): A NumPy array where each row represents a point (x, y).

    Returns:
        tuple: A tuple containing:
            - best_path (list): The ordered list of indices representing the shortest path.
            - total_distance (float): The total distance of the shortest path.
    """

    num_points = len(points)
    best_path = None
    shortest_distance = float('inf')  # Initialize with a very large value

    for perm in permutations(range(num_points)):  # Iterate through all possible orderings (permutations)
        current_distance = 0.0
        for i in range(num_points - 1):
            p1_index = perm[i]
            p2_index = perm[i+1]
            x1, y1 = points[p1_index]
            x2, y2 = points[p2_index]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)  # Euclidean distance
            current_distance += distance

            if current_distance < shortest_distance:
                shortest_distance = current_distance
                best_path = list(perm)

    return best_path, shortest_distance

def calc_distances(points):
    distances = np.zeros((len(points), len(points)))

    for n, (x1, y1)in enumerate(points):
        for m, (x2, y2) in enumerate(points):
            distances[n, m] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    plt.imshow(distances)
    plt.show()

def main(points):

    best_path, total_distance = shortest_path(points)

    print("Best Path (indices):", best_path)
    print("Total Distance:", total_distance)


    import matplotlib.pyplot as plt

    # Plot the points and the optimal path
    plt.figure(figsize=(8, 6))
    plt.plot(points[:, 0], points[:, 1], 'o', label='Points')  # Plot all points

    for i in range(len(best_path) - 1):
        p1_index = best_path[i]
        p2_index = best_path[i+1]
        x1, y1 = points[p1_index]
        x2, y2 = points[p2_index]
        plt.plot([x1, x2], [y1, y2], '-', label='Path')  # Plot the line segments

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Shortest Path Through Points')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    path = r"E:\JGS\Willowstick\Processing\25789 - Watertech - Thames -Knight&Bessborough Reservoir - COMPARE - 2025\Willowstick UK__25789 - Knight&Bessborough Reservoir - COMPARE - Group 1__wst"

    dfs = []

    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_path = os.path.join(path, file)
            dfs.append(pd.read_csv(file_path))

    xy = np.column_stack((dfs[0]["EASTING"].to_numpy(), dfs[0]["NORTHING"].to_numpy()))
    randxy = xy.copy()
    np.random.shuffle(randxy)

    main(xy)
    main(randxy)

    # calc_distances(randxy)

    # Example Usage:
    # points = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])  # Your set of xy points

