import sys
import random
from math import sqrt

def getRandomMedoids(data, k):
    # Randomly select k data points as initial medoids
    medoids_indices = random.sample(range(len(data)), k)
    medoids = [data[i] for i in medoids_indices]
    return medoids

def assignToMedoid(data_point, medoids):
    min_dist = float('inf')
    cluster_id = -1

    for i, medoid in enumerate(medoids):
        try:
            data_point[0] = float(data_point[0])
            data_point[1] = float(data_point[1])
        except ValueError:
            continue

        # Calculate distance to the medoid
        cur_dist = sqrt(pow(data_point[0] - medoid[0], 2) + pow(data_point[1] - medoid[1], 2))

        if cur_dist < min_dist:
            min_dist = cur_dist
            cluster_id = i

    return cluster_id

if __name__ == "__main__":
    data = []  # Store data points for random medoid selection
    for line in sys.stdin:
        line = line.strip()
        fields = line.split(',')
        # Check if the line contains the expected number of fields
        if len(fields) == 8:
            try:
                pickup_x = float(fields[4])
                pickup_y = float(fields[5])
            except ValueError:
                continue
            data.append([pickup_x, pickup_y])


    # Get the iteration number from the command-line argument
    iteration = int(sys.argv[1])  # Get the iteration number from the command-line argument
    # Get the number of clusters
    k = int(sys.argv[2])  # Get the number of clusters (k) from the command-line argument
    #Initial Random Medoid Selection (Iteration 1)
    if iteration == 1:
        # Randomly select initial medoids for the first iteration
        medoids = getRandomMedoids(data, k)  # Randomly select initial medoids for the first iteration
    else:
        medoids = []  # Initialize an empty medoids list

    if iteration > 1:
        # Read medoids from the previous iteration's medoids.txt file
        with open('medoids.txt', 'r') as medoids_file:
            for line in medoids_file:
                x, y = line.strip().split(',')
                medoids.append((float(x), float(y)))

    for line in sys.stdin:
        line = line.strip()
        fields = line.split(',')
        # Check if the line contains the expected number of fields
        if len(fields) == 8:
            try:
                pickup_x = float(fields[4])
                pickup_y = float(fields[5])
            except ValueError:
                continue
            # Calculate the cluster assignment for each data point
            cluster_id = assignToMedoid([pickup_x, pickup_y], medoids)
            print(f"{iteration}\t{cluster_id}\t{pickup_x}\t{pickup_y}")
