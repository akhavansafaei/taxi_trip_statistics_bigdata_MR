import sys
from math import sqrt
import random

def getRandomMedoids(data, k):
    # Randomly select k data points as initial medoids
    medoids_indices = random.sample(range(len(data)), k)
    # Create a list of data points using the selected indices
    medoids = [data[i] for i in medoids_indices]
    return medoids

#.................................................................
# get initial medoids from a txt file and add them in an array
def getMedoids(filepath):
    medoids = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line:
                try:
                    line = line.strip()
                    cord = line.split(', ')
                    # cord[0] is x and cord[1] is y point of a cmedoid
                    medoids.append([float(cord[0]), float(cord[1])])
                except:
                    break
            else:
                break
            line = fp.readline()

    fp.close()
    #print(medoids)
    return medoids

# create clusters based on initial medoids
def createClusters(medoids):
    # 
    for line in sys.stdin:
        line = line.strip()
        fields = line.split(',')
        min_dist = 100000000000000
        index = -1

        for medoid in medoids:
            try:
                pickup_x = float(fields[4])
                pickup_y = float(fields[5])
            except ValueError:
                # float was not a number, so silently
                # ignore/discard this line
                continue

            # euclidian distance from every point of dataset
            # to every medoid
            cur_dist = sqrt(pow(pickup_x - medoid[0], 2) + pow(pickup_y - medoid[1], 2))

            # find the medoid which is closer to the point
            if cur_dist <= min_dist:
                min_dist = cur_dist
                index = medoids.index(medoid)

        var = "%s\t%s\t%s" % (index, pickup_x, pickup_y)
        print(var)

if __name__ == "__main__":
    # Get the iteration number from the command-line argument
    iteration = int(sys.argv[1])  # Get the iteration number from the command-line argument
    # Get the number of clusters
    k = int(sys.argv[2])  # Get the number of clusters (k) from the command-line argument
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
    
    if iteration==1:
        # Randomly select initial medoids for the first iteration
        medoids = getRandomMedoids(data, k)  # Randomly select initial medoids for the first iteration
    else:
        medoids = getMedoids('medoids.txt')
    createClusters(medoids)
