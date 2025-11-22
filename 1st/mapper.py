import sys
import random

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
            data_point[4] = float(data_point[4])
            data_point[5] = float(data_point[5])
        except ValueError:
            continue

        # Calculate distance to the medoid
        cur_dist = sqrt(pow(data_point[4] - medoid[4], 2) + pow(data_point[5] - medoid[5], 2))

        if cur_dist < min_dist:
            min_dist = cur_dist
            cluster_id = i

    return cluster_id

def main():
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

    iteration = int(sys.argv[1])  # Get the iteration number from the command-line argument

    if iteration == 1:
        k = int(sys.argv[2])  # Get the number of clusters (k) from the command-line argument
        medoids = getRandomMedoids(data, k)  # Randomly select initial medoids
    else:
        medoids = []  # Initialize an empty medoids list

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
            cluster_id = assignToMedoid([pickup_x, pickup_y], medoids)
            print(f"{iteration}\t{cluster_id}\t{pickup_x}\t{pickup_y}")

if __name__ == "__main__":
    main()
