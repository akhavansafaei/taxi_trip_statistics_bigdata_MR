import sys

def checkClusters(data, centroids, threshold):
    # Check if the distance between centroids and centroids1 is less than the threshold for all clusters
    f_distance = True
    for i, centroid in enumerate(centroids):
        centroid_x, centroid_y = centroid
        for j, (x, y) in enumerate(data):
            distance = ((float(x) - float(centroid_x)) ** 2 + (float(y) - float(centroid_y)) ** 2) ** 0.5
            if distance >= threshold:
                f_distance = False
                break

    if f_distance:
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    centroids = []  # Store centroids from the current iteration
    data = []  # Store all data points

    # Read centroids from the reducer's output
    for line in sys.stdin:
        cluster_id, x, y = line.split('\t')
        centroids.append((x, y))

    # Read all data points
    for line in sys.stdin:
        x, y = line.split('\t')[1:]
        data.append((x, y))

    threshold = 1.0  # Set your desired threshold here
    checkClusters(data, centroids, threshold)
