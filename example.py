from csv import reader #to open the data files
from math import sqrt #to be able to use sqrt for euclidean distance
import operator #to be able to use itemgetter
import random   #to create a random intger between two points for the split of the dataset

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

def minmax(dataset):
    min_max = list()
    for i in range(len(dataset[0])):
        column_values = [row[i] for row in dataset]
        min_value = min(column_values) #using min(), we can determine the miniumum value in the column
        max_value = max(column_values) #using max(), we can determine the max value in the clumn
        min_max.append([min_value, max_value]) #adds the min, max values in the list
    return min_max #returns the list that has min, max values for each column
            
def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)-1): #for our dataset, the last column is made up of strings, so range is 1 less than total length of list
            #normalize a single value, can normalize the data to the range 0 and 1
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0]) #scale the values ((value - min)/(max - min)) to be 0 or 1

def print_dataset(dataset):
    for i in range(len(dataset)):
        print(dataset[i], '\n')


trainingSet = []
datafile = 'example.data'
dataset = load_dataset(datafile)

print("Loaded dataset with {0} rows and {1} columns".format(len(dataset), len(dataset[0])))

for i in range(len(dataset[0])-1):
    str_to_float(dataset, i)

minmax_data = minmax(dataset)
normalize_dataset(dataset, minmax_data)
print_dataset(dataset)