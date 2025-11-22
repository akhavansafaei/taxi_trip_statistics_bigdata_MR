import sys
from math import sqrt

# Retrieve the convergence threshold from the configuration
convergence_threshold = float(sys.argv[1])  # Get the convergence threshold from the command-line argument

def calculateNewMedoids():
    current_cluster_id = None
    current_cluster_points = []

    for line in sys.stdin:
        cluster_id, x, y = line.split('\t')

        cluster_id = int(cluster_id)
        x = float(x)
        y = float(y)

        if current_cluster_id is None:
            current_cluster_id = cluster_id

        if cluster_id == current_cluster_id:
            current_cluster_points.append((x, y))
        else:
            # Calculate the new medoid for the current cluster
            new_medoid = calculateMedoid(current_cluster_points)

            # Print the new medoid center to standard output
            print(f"{current_cluster_id}\t{new_medoid[0]}\t{new_medoid[1]}")

            # Check if the change in medoid position is below the threshold
            if not hasConverged(new_medoid, current_cluster_points):
                current_cluster_points = [(x, y)]
            else:
                # If the cluster has converged, print a flag to indicate convergence
                print(f"{current_cluster_id}\tCONVERGED")

            current_cluster_id = cluster_id

    # Calculate the new medoid for the last cluster
    new_medoid = calculateMedoid(current_cluster_points)

    # Print the new medoid center to standard output
    print(f"{current_cluster_id}\t{new_medoid[0]}\t{new_medoid[1]}")

    # Check if the change in medoid position is below the threshold
    if not hasConverged(new_medoid, current_cluster_points):
        current_cluster_points = [(x, y)]
    else:
        # If the last cluster has converged, print a flag to indicate convergence
        print(f"{current_cluster_id}\tCONVERGED")

def calculateMedoid(points):
    # Calculate the medoid as the point with the minimum total distance to all other points
    best_medoid = None
    min_total_distance = float('inf')

    for point in points:
        total_distance = sum(sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2) for x, y in points)

        if total_distance < min_total_distance:
            min_total_distance = total_distance
            best_medoid = point

    return best_medoid

def hasConverged(new_medoid, cluster_points):
    # Calculate the change in medoid position compared to the previous medoid
    prev_medoid = calculateMedoid(cluster_points)
    delta_x = abs(new_medoid[0] - prev_medoid[0])
    delta_y = abs(new_medoid[1] - prev_medoid[1])

    # Check if both coordinates have changed less than the convergence threshold
    return delta_x < convergence_threshold and delta_y < convergence_threshold

if __name__ == "__main__":
    calculateNewMedoids()
