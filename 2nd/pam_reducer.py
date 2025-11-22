import sys
from statistics import mean, mode

def main():
    # Initialize a variable to keep track of the current iteration
    current_iteration = None
    # Initialize a variable to keep track of the current cluster ID
    current_cluster_id = None
    # Initialize an empty list to store data points in the current cluster
    data_points = []

    for line in sys.stdin:
        # Split the input line into fields
        iteration, cluster_id, x, y = line.split('\t')
        # Check if the iteration has changed
        if current_iteration == iteration:
            # Check if the cluster ID has changed within the same iteration
            if current_cluster_id == cluster_id:
                # Add the data point to the current cluster
                data_points.append((float(x), float(y)))
            else:
                # Update the current cluster ID
                current_cluster_id = cluster_id
                # Reset data_points to store the new cluster's data
                data_points = [(float(x), float(y))]
        else:
            if current_iteration is not None: # Check if this is not the first iteration (not None)
                # Calculate the new medoid as the mean of the cluster
                new_medoid = (mode([x for x, _ in data_points]), mode([y for _, y in data_points]))

                # Print the new medoid center to standard output
                print(f"{current_iteration}\t{current_cluster_id}\t{new_medoid[0]}\t{new_medoid[1]}")

                # Write the new medoid to the medoids.txt file for the next iteration
                with open('medoids.txt', 'a') as medoids_file:
                    medoids_file.write(f"{new_medoid[0]},{new_medoid[1]}\n")
            # Update the current iteration
            current_iteration = iteration
            # Update the current cluster ID
            current_cluster_id = cluster_id
            # Reset data_points to store the new cluster's data
            data_points = [(float(x), float(y))]

    # Calculate the new medoid for the last cluster
    new_medoid = (mode([x for x, _ in data_points]), mode([y for _, y in data_points]))

    # Print the new medoid center to standard output
    print(f"{current_iteration}\t{current_cluster_id}\t{new_medoid[0]}\t{new_medoid[1]}")

    # Write the new medoid to the medoids.txt file for the next iteration
    with open('medoids.txt', 'a') as medoids_file:
        medoids_file.write(f"{new_medoid[0]},{new_medoid[1]}\n")

if __name__ == "__main__":
    main()
