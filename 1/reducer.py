from statistics import mode
import sys

def calculateNewMedoids():
    current_medoid = None
    x_values = None
    y_values = None
    count = 0

    # input comes from STDIN
    for line in sys.stdin:

        # parse the input of mapper.py
        medoid_index, x, y = line.split('\t')

        # convert x and y (currently a string) to float
        try:
            x = float(x)
            y = float(y)
        except ValueError:
            # float was not a number, so silently
            # ignore/discard this line
            continue

        # this IF-switch only works because Hadoop sorts map output
        # by key (here: word) before it is passed to the reducer
        if current_medoid == medoid_index:
            count += 1
            x_values = x_values.append(x)
            y_values =  y_values.append(y)
        else:
            if count != 0:
                # print the mode of every cluster to get new medoids
                print(str(mode(x_values)) + ", " + str(mode(y_values)))

            current_medoid = medoid_index
            x_values = [x]
            y_values = [y]
            count = 1
    
    # print last cluster's medoids
    if current_medoid == medoid_index and count != 0:
        print(str(mode(x_values)) + ", " + str(mode(y_values)))

if __name__ == "__main__":
    calculateNewMedoids()
