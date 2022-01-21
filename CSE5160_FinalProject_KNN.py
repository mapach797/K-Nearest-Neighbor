from csv import reader #to open the data files
from math import sqrt #to be able to use sqrt for euclidean distance
import operator #to be able to use itemgetter
import random   #to create a random intger between two points for the split of the dataset

#load the dataset 
def load_dataset(filename):
    data_set = list()
    with open(filename, 'r') as training: #opens the file the user has provided in the main function
        csv_reader = reader(training) #reads the datafile
        for row in csv_reader: #reads each row in the dataset
            if not row:
                continue #if what it reads is not a row, it continues on reading the next row
            data_set.append(row)    #adds the row into the list
    return data_set

#convert string column to float for test data
def str_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())
        #.strip() removes leading and trailing characters and whitespaces

#finding the min and max of each column
def minmax(dataset):
    min_max = list()
    for i in range(len(dataset[0])):
        column_values = [row[i] for row in dataset]
        min_value = min(column_values) #using min(), we can determine the miniumum value in the column
        max_value = max(column_values) #using max(), we can determine the max value in the clumn
        min_max.append([min_value, max_value]) #adds the min, max values in the list
    return min_max #returns the list that has min, max values for each column

#rescale the dataset columns to 0 or 1
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)-1): #for our dataset, the last column is made up of strings, so range is 1 less than total length of list
            #normalize a single value, can normalize the data to the range 0 and 1
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0]) #scale the values ((value - min)/(max - min)) to be 0 or 1
            
def split_dataset(dataset, training_set, test_set):
    #x_rand = random.randint(120,130) #selects a random number to determine how many are going to be in the training set
    for i in range(len(dataset)):
        if(i < 128):#x_rand): #appends the datapoints to training set if i is less than the random number
            training_set.append(dataset[i])
        else:
            test_set.append(dataset[i]) #else it appends to the test set

def print_dataset(dataset):
    for i in range(len(dataset)):
        print(dataset[i], '\n')
            
#calcualte the Euclidean distance between two vectors
def euclidean_distance(instance1, instance2, length):
    distance = 0.0
    for i in range(length):
        distance += (instance1[i] - instance2[i])**2 #subtracts the two instances and then squares the result
        #adds the result to the distance variable
    return sqrt(distance) #returns the sqrt of the value

#locate similar nieghbors
def locate_neighbors(training_set, test_instance, num_neighbors):
    distances = list()
    length = len(test_instance)-1
    for x in range(len(training_set)):
        how_far = euclidean_distance(test_instance, training_set[x], length) #calls the euclidean distance function for each i in range of the length of the test instance - 1
        distances.append((training_set[x], how_far)) #adds the solution to the euclidean istance to the distance list for each i in the range of the length of the test instance - 1
    distances.sort(key = operator.itemgetter(1)) #contructs a callable (can be called) that assumes the list as input, and gets distance[1]
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0]) #for distances[i][0], it starts at the row index 0, and i defines the column index
    return neighbors

def KNN_Classification(neighbors):
    hit = {} #defines an associative array of pairs
    for x in range(len(neighbors)):
        response = neighbors[x][-1] 
        if response in hit:
            hit[response] += 1
        else:
            hit[response] = 1
    respond_sorted = sorted(hit.items(), key=operator.itemgetter(1), reverse = True) #sorts the list by values backwards
    return respond_sorted[0][0] #returns the single element at index 0

#the accuracy in which the testset is compared to the training set
def Accuracy(test_Set, predictions):
    correct = 0
    wrong = 0
    for i in range(len(test_Set)):
        if test_Set[i][-1] in predictions[i]: #starts at the back of the list that was called, and calculates if there was a hit for nearest neighbors
            correct += 1
        else:
            wrong += 1
    result = (correct / len(test_Set) *100)
    print("\nKNN correct: ", correct, "KNN wrong: ", wrong)
    return result

#
#====================================== main function ===========================================
#

def main():
    trainingSet = []
    testSet = []
    #get value of k
    k = int(input("Enter the value of k: "))
    datafile = 'iris.data'
    
    dataset = load_dataset(datafile)

    for i in range(len(dataset[0])-1): #converts the datafile from string to float
        str_to_float(dataset, i)
        
    minmax_train = minmax(dataset) #finds the minimum and maximum values in each column
    normalize_dataset(dataset, minmax_train)#normalizes the values in the dataset
    
    split_dataset(dataset, trainingSet, testSet) #splits the training set into two sets
                                                       #training set and test set 

    dataset_length = len(dataset)
    print("\nTotal amount of instances in the dataset is:" ,dataset_length)

    normal_training_set = len(trainingSet)
    print("\nLength of training set after splitting is: ", normal_training_set)

    normal_test_set = len(testSet)
    print("\nLength of test set after splitting is: ", normal_test_set)
    
    print("Attributes of the Iris dataset are: Sepal Length, Sepal Width, Petal Length, Petal Width, and Class")

    print("\n\nThese are the normalized instances in the training set: \n")
    print_dataset(trainingSet)

    print("\n\nThese are the normalized instances in the test set: \n")
    print_dataset(testSet)
    
    predictions = []
    for x in range(len(testSet)):
        neighbors = locate_neighbors(trainingSet, testSet[x], k)
        result = KNN_Classification(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])) #displays the predicted and actual result
    
    print("\nValue of K entered is: "+ repr(k))
    
    accuracy = Accuracy(testSet, predictions) #Accuracy of testset and training set
    round_accuracy = round(accuracy, 3)
    print("Accuracy: "+ repr(round_accuracy) + '%')

#main function is callled
main()
