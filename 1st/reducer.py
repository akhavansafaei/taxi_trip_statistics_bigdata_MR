import sys
from statistics import mean

def main():
    current_iteration = None
    current_cluster_id = None
    data_points = []

    for line in sys.stdin:
        iteration, cluster_id, x, y = line.split('\t')
        if current_iteration == iteration:
            if current_cluster_id == cluster_id:
                data_points.append((float(x), float(y)))
            else:
                current_cluster_id = cluster_id
                data_points = [(float(x), float(y))]
        else:
            if current_iteration is not None:
                # Calculate the new medoid as the mean of the cluster
                new_medoid = (mean([x for x, _ in data_points]), mean([y for _, y in data_points]))
                print(f"{current_iteration}\t{current_cluster_id}\t{new_medoid[0]}\t{new_medoid[1]}")

            current_iteration = iteration
            current_cluster_id = cluster_id
            data_points = [(float(x), float(y))]

    # Calculate the new medoid for the last cluster
    new_medoid = (mean([x for x, _ in data_points]), mean([y for _, y in data_points]))
    print(f"{current_iteration}\t{current_cluster_id}\t{new_medoid[0]}\t{new_medoid[1]}")

if __name__ == "__main__":
    main()
