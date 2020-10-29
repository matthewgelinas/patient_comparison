import csv
import copy
import statistics

def getcsv(file):
    filename = file
    # initializing the titles and rows list 
    fields = [] 
    rows = [] 

    f = open(filename, 'r')
    
    # reading csv file 
    with f as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        
        # extracting field names through first row 
        fields = next(csvreader) 
    
        # extracting each data row one by one 
        for row in csvreader: 
            rows.append(row) 
    
        # get total number of rows 
        #print("Total no. of rows: %d"%(csvreader.line_num)) 

    return [rows,fields]

#normalizes an array excluding selected categories
def normalize(arr2d,titles,include):

    #creates coppy of arr2d
    normarray = copy.deepcopy(arr2d)
    
    for i in range(len(titles)):
        tempmax = 0
        tempmin = 10000
        temprange = 0

        #finds the range of max and min value in each category
        for j in range(len(arr2d)):
            #finds max value for each category
            if (j == 0 or (float(tempmax) < float(arr2d[j][i]))):
                tempmax = arr2d[j][i]
            
            #finds min alue for each category
            if (j == 0 or (float(tempmin) > float(arr2d[j][i]))):
                tempmin = arr2d[j][i]
        
        #calculates the range of each category
        temprange = float(tempmax) - float(tempmin)

        #normalizes all the values and stores them in new normalized array
        for j in range(len(arr2d)):
            #excludes PatientId's and medicine number from normalization
            if (any(i == x for x in include)):
                normvalue = ((float(arr2d[j][i]) - float(tempmin))/temprange)
                normarray[j][i] = normvalue
            else:
                normarray[j][i] = int(arr2d[j][i])

    #returns the array normalized to main
    return normarray

#finds the euclidian distance between vectors
def euclidDis(w,v):

    sum = 0
    
    #calculates the euclidean distance between 2 patients
    for iw,iv in zip(w,v):
        sum += (iw-iv)**2

    #returns the euclidean distance
    return sum

#compares patients in desired categories and returns euclidian Distance from these categories
def comparePat(patient1, patient2, categories):
    
    temppatient1 = []
    temppatient2 = []

    for i in categories:
        temppatient1.append(patient1[i])
        temppatient2.append(patient2[i])

    return euclidDis(temppatient1,temppatient2)

# Function to insert element
def insert(list, n, k): 
      
    (nscore,npatient) = n
    index = 0
    placed = False

    #if you want the top 0 items you get an empty list
    if k == 0:
        return []

    #if list is empty add the item return the list
    if not list:
        list.insert(0,n)
        return list

    # Searching for the position 
    for i in range(len(list)): 
        (listscore,listpatient) = list[i]
        #print("%d\t%d\t%f\t%f" %(len(list),i,listscore,nscore))
        if listscore > nscore: 
            index = i 
            placed = True
            break

    
    #patient score is not lower than items on the list but list is shorter than k
    if (len(list) < k and placed == False):
        list.insert(i+1,n)
        return list
    #patient score was not lower than lowest k scores so we return list of k
    elif(placed == False):
        return list
      
    #print(index)
    #if it is not in the bottom k of the scores it isn't added
    if(index < k):
        # Inserting n in the list 
        list = list[:i] + [n] + list[i:] 
        #removing items out of the top k
        list = list[:k]
        return list
    else:
        print('If you see this something went wrong')

      
    (nscore,npatient) = n
    index = 0
    placed = False

    #if you want the top 0 items you get an empty list
    if k == 0:
        return []

    #if list is empty add the item return the list
    if not list:
        list.insert(0,n)
        return list

    # Searching for the position 
    for i in range(len(list)): 
        (listscore,listpatient) = list[i]
        if listscore > nscore: 
            index = i 
            placed = True
            break

    
    #patient score is not lower than items on the list but list is shorter than k
    if (len(list) < k and placed == False):
        list.insert(i+1,n)
        return list
    #patient score was not lower than lowest k scores so we return list of k
    elif(placed == False):
        return list
      
    #print(index)
    #if it is not in the bottom k of the scores it isn't added
    if(index < k):
        # Inserting n in the list 
        list = list[:i] + [n] + list[i:] 
        #removing items out of the top k
        list = list[:k]
        return list
    else:
        print('If you see this something went wrong')

#finds the k most similar patients to the selected patient from all patients using defined categories and returns them
def findSimPat(patient, patientlist, categories, k):
    rankedlist = []
    temp = []
    count = 0

    for eachpatient in patientlist:
        score = comparePat(patient,eachpatient,categories)
        temp = (score,eachpatient)
        rankedlist = insert(rankedlist,temp,k)

    #returns the smallest k scores (closest to the target patient)
    return rankedlist

#displays the results in an organized table
def displayresults(titles, scores, Opatient, Npatients, k, orderedid):
    print('\nOriginal Patient is at the top followed by the', k, 'most similar patients.')
    print("%-15s%-10s%-20s%-20s%-10s%-10s%-15s%-10s" %(titles[0],titles[1],titles[2],titles[3],titles[4],titles[5],titles[6],"Score"))
    print("%-15s%-10s%-20s%-20s%-10s%-10s%-15s%-10s" %(Opatient[0],Opatient[1],Opatient[2],Opatient[3],Opatient[4],Opatient[5],Opatient[6],"Original"))

    count = 0
    for i in orderedid:
        if count == len(orderedid):
            break
        print("%-15s%-10s%-20s%-20s%-10s%-10s%-15s%-10s" %(Npatients[i][0],Npatients[i][1],Npatients[i][2],Npatients[i][3],Npatients[i][4],Npatients[i][5],Npatients[i][6],scores[count]))
        count += 1

#organizes the non normalized list by returning the array indicies in the correct order
def orderids(topmatches,Odata):
    #getting non normalized lists order of indexes
    orderedid = []
    index = 0

    #PATIENTS IN THE DATASET CAN HAVE MORE THAN 1 ENTRY PATIENTIDS ARE NOT UNIQUE
    #I compared the ID's and the ages to not accidentally include duplicates
    for test in topmatches:
        count = 0
        for row in Odata: 
            if((int(row[0]) == int(test[0])) and (int(row[6]) == int(test[6]))):
                orderedid.insert(index,count)
                index += 1
            count += 1
    
    return orderedid

def commonmedicine(patients, matchindexes, k):
    
    medicine = []
    count = 0

    for i in matchindexes:
        medicine.insert(count, patients[i][6])
        count += 1

    modes = statistics.multimode(medicine)
    biggest = medicine.count(modes[0])

    #TODO
    if(len(modes) == k):
        print("Each of the %d patients were given a different medication" %k)
    elif(biggest >= float(k/2)):
        print("Medicine %d was given to %d of the %d patients (a majority of the patients)" %(int(modes[0]),biggest,k))
    elif(len(modes) == 1):
        print("Medicine %d was given to %d of the %d patients (not a majority of the patients)" %(int(modes[0]),biggest,k))
    else:
        print("Medicines %s were each given to %d of the %d patients (not a majority of the patients)" %(modes, biggest, k))

def main():

    #imports csv files and separates them
    [patients, titles] = getcsv("query.csv")
    query = copy.deepcopy(patients)

    [patients1, titles1] = getcsv("Datasetsmall.csv")
    dataset = copy.deepcopy(patients1)

    #these are the desired categories to be compared excluding PatientID's and Medicine numbers
    #Assuming they are numbered in order from 0 to n
    categories = [1,2,3,4,5]

    #normalizes the desired categories excluding PatientID's and Medicine numbers
    normquery = normalize(query,titles,categories)
    normdataset = normalize(dataset,titles,categories)

    #checks top 3,5, and 7 similar patients in the dataset for each patient in query
    for (q,nq) in zip(query,normquery):
        for kval in [3,5,7]:

            #finds the k top matches in for the submitted patient and their similarity scores
            [scores,topmatches] = zip(*findSimPat(nq,normdataset,categories,kval))

            #finds the arrays of the closest ranked patients in the non normalized data set so we can display the data
            #in the step above we organized the normalized data set
            matchindexes = orderids(topmatches,dataset)

            #displays the results in a clear list for comparison
            displayresults(titles,scores,q,dataset, kval, matchindexes)

            #prints information about medicine given to similar patients
            commonmedicine(dataset,matchindexes, kval)

if __name__ == "__main__":
    main()