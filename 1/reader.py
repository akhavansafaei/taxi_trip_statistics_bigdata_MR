from mapper import getMedoids

#check if medoids and medoids1 are the same
def checkMedoidsDistance(medoids, medoids1):

    if medoids==medoids1:
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    medoids = getMedoids('medoids.txt')
    medoids1 = getMedoids('medoids1.txt')
    
    checkMedoidsDistance(medoids, medoids1)
