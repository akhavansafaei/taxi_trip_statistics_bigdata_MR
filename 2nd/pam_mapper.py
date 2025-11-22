import sys
import random
from math import sqrt

def getRandomMedoids(data, k):
    # Randomly select k data points as initial medoids
    medoids_indices = random.sample(range(len(data)), k)
    # Create a list of data points using the selected indices
    medoids = [data[i] for i in medoids_indices]
    return medoids

def assignToMedoid(data_point, medoids):
    # Initialize the minimum distance to positive infinity
    min_dist = float('inf')
    # Initialize the cluster ID to -1 (indicating no cluster assigned)
    cluster_id = -1

    for i, medoid in enumerate(medoids):
        try:
            # Convert data_point's x-coordinate to a float
            data_point[0] = float(data_point[0])
            # Convert data_point's y-coordinate to a float
            data_point[1] = float(data_point[1])
        except ValueError:
            # Skip this data point if conversion to float fails
            continue

        # Calculate distance to the medoid
        # Calculate the Euclidean distance between data_point and the current medoid
        cur_dist = sqrt(pow(data_point[0] - medoid[0], 2) + pow(data_point[1] - medoid[1], 2))

        if cur_dist < min_dist:
            min_dist = cur_dist # Update the minimum distance
            cluster_id = i  # Update the cluster ID to the current medoid's index

    return cluster_id # Return the cluster ID assigned to data_point

def main():
    data = []  # Store data points for random medoid selection
    for line in sys.stdin:
        line = line.strip()
        fields = line.split(',')
        # Check if the line contains the expected number of fields
        if len(fields) == 8:
            try:
                # Extract the x-coordinate of the pickup location
                pickup_x = float(fields[4])
                # Extract the y-coordinate of the pickup location
                pickup_y = float(fields[5])
            except ValueError:
                # Skip this line if coordinate conversion to float fails
                continue
            # Store the pickup location as a data point (x, y)
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
                pickup_x = float(fields[4])# Extract the x-coordinate of the pickup location
                pickup_y = float(fields[5])# Extract the y-coordinate of the pickup location
            except ValueError:
                 # Skip this line if coordinate conversion to float fails
                continue
            # Calculate the cluster assignment for each data point using the current medoids
            cluster_id = assignToMedoid([pickup_x, pickup_y], medoids)
            # Print the results: Iteration, Cluster ID, Pickup_x, Pickup_y
            print(f"{iteration}\t{cluster_id}\t{pickup_x}\t{pickup_y}")

if __name__ == "__main__":
    main()
