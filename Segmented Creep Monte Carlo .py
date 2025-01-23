
import math
import random
import csv
import pandas
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# ------- User sets the initial values for these -------------------------

# Initial Estimate for Average Segment Length in minutes
#  Code:   seg[Current Segment ID][Next Segment ID][Temperaure][Humidity]
#  Example:  seg02LH -- current segmentis 0, next segment is 2, temperaure
#            is low, humidity is high

#  seg 0 is a low creep rate segment
#  seg 1 is  medium creep rate segment
#  seg 2 is a high creep rate segment

seg01LL = [160]
seg01HL = [140] 
seg01LH = [150]
seg01HH = [100]
seg02LL = [190]
seg02HL = [170]
seg02LH = [165]
seg02HH = [140]

seg10LL = [20]
seg10HL = [50] 
seg10LH = [30]
seg10HH = [80]
seg12LL = [150]
seg12HL = [140]
seg12LH = [145]
seg12HH = [120]

seg20LL = [20]
seg20HL = [40] 
seg20LH = [30]
seg20HH = [60]
seg21LL = [70]
seg21HL = [90]
seg21LH = [95]
seg21HH = [120]

# When the optimal value is sought, by how many minutes should each of
#  the above segments been changed?
interval = 10

# How many intervals above and below the startign value
#   shoud be investigated.
numintervals = 6

# Minimum segement length allowed.  If the intervals below the starting value
#  would result in a negaive segment length, what is the minimum value to
#  stop at?
minseg = 5

#Lenth of time to use for the first interval.  Other intervals are determed from the actual sample data time.
tinit = 10

#MonteCarlo Itterations
monteCarlo = 500

#Temperature High/Low Threshold
tempThresh = 74

#Humidity Hihg/Low Threhold
humidThresh = 56

#Slope for each segment type
slope0 = .00000001
slope1 = .0000004
slope2 = .0000009


#Folder name to store output in.  A number will be attached to the end of the filename automatically so results do not overwrite
foldername = "results"

# ------- User sets the initial values for the above variables -----------




#  ------- Open Data File ------
#
#  Data is in .csv format, first row is time with 0 minutes at the beginning of phase II creep,
#  the secodn row is travel starting with 0, the third row is temperature in F, and
#  the fourth row is relative humidity

Tk().withdraw()
filename = askopenfilename()

with open(filename, newline='',encoding='utf-8-sig') as csvfilein:

    filein = csv.reader(csvfilein,  quoting=csv.QUOTE_NONNUMERIC) #delimiter=',', quotechar='"',

    time = filein.__next__()
    travel = filein.__next__()
    temperature = filein.__next__()
    humidity = filein.__next__()

# ----------- End Open Data File --------

# Set values for lambda
lam01LL = [1/seg01LL[0]]
lam01HL = [1/seg01HL[0]] 
lam01LH = [1/seg01LH[0]]
lam01HH = [1/seg01HH[0]]
lam02LL = [1/seg02LL[0]]
lam02HL = [1/seg02HL[0]]
lam02LH = [1/seg02LH[0]]
lam02HH = [1/seg02HH[0]]

lam10LL = [1/seg10LL[0]]
lam10HL = [1/seg10HL[0]] 
lam10LH = [1/seg10LH[0]]
lam10HH = [1/seg10HH[0]]
lam12LL = [1/seg12LL[0]]
lam12HL = [1/seg12HL[0]]
lam12LH = [1/seg12LH[0]]
lam12HH = [1/seg12HH[0]]

lam20LL = [1/seg20LL[0]]
lam20HL = [1/seg20HL[0]] 
lam20LH = [1/seg20LH[0]]
lam20HH = [1/seg20HH[0]]
lam21LL = [1/seg21LL[0]]
lam21HL = [1/seg21HL[0]]
lam21LH = [1/seg21LH[0]]
lam21HH = [1/seg21HH[0]]




#Determine the folder name that should be used
foldernum = 10000
while os.path.isdir(foldername + str(foldernum)[1:]):
    foldernum += 1
foldername = foldername + str(foldernum)[1:]    
os.makedirs(foldername)

# Initialize Random Number Generator
seed = 1

# Initiate run tracker -  monteCarloRuns is the numebr of runs per output file
monteCarloRuns = 100
    
for w in range( math.ceil(monteCarlo/100)):
    if w+1 == math.ceil(monteCarlo/100):
        monteCarloRuns = monteCarlo - (w*100)

    # Initiate variables for the output .csv file
    t = [[]]
    i = 0
    x = [0]
    j = 0
    resid = [0]
    squares = [0]
    SSR = 0
    curseg = 0
    curtemp = "L"
    curhum = "L"
    xresults = [[]]
    residresults = [[]]
    SSRresults = []
    TotSSR = [0]
    
    for k in range(monteCarloRuns):

        # Initialize variables for a new simulated creep test run
        random.seed(seed)
        seed = seed + 1
        x = [0]
        resid = [0]
        squares = [0]
        SSR = 0
        TSSR = 0

        for j in range(len(time)):

            # Generate a random number [0,1)
            p = random.random()

            # Set temp state
            if temperature[j] < tempThresh:
                curtemp = "L"
            else:
                curtemp = "H"

             # Set humidity state
            if humidity[j] < humidThresh:
                curhum = "L"
            else:
                curhum = "H"       

            #update probabilites
            if j > 0:
                s01LL = [1-math.exp(-lam01LL[0]*(time[j]-time[j-1]))]
                s01HL = [1-math.exp(-lam01HL[0]*(time[j]-time[j-1]))] 
                s01LH = [1-math.exp(-lam01LH[0]*(time[j]-time[j-1]))]
                s01HH = [1-math.exp(-lam01HH[0]*(time[j]-time[j-1]))]
                s02LL = [1-math.exp(-lam02LL[0]*(time[j]-time[j-1]))]
                s02HL = [1-math.exp(-lam02HL[0]*(time[j]-time[j-1]))]
                s02LH = [1-math.exp(-lam02LH[0]*(time[j]-time[j-1]))]
                s02HH = [1-math.exp(-lam02HH[0]*(time[j]-time[j-1]))]

                s10LL = [1-math.exp(-lam10LL[0]*(time[j]-time[j-1]))]
                s10HL = [1-math.exp(-lam10HL[0]*(time[j]-time[j-1]))]
                s10LH = [1-math.exp(-lam10LH[0]*(time[j]-time[j-1]))]
                s10HH = [1-math.exp(-lam10HH[0]*(time[j]-time[j-1]))]
                s12LL = [1-math.exp(-lam12LL[0]*(time[j]-time[j-1]))]
                s12HL = [1-math.exp(-lam12HL[0]*(time[j]-time[j-1]))]
                s12LH = [1-math.exp(-lam12LH[0]*(time[j]-time[j-1]))]
                s12HH = [1-math.exp(-lam12HH[0]*(time[j]-time[j-1]))]

                s20LL = [1-math.exp(-lam20LL[0]*(time[j]-time[j-1]))]
                s20HL = [1-math.exp(-lam20HL[0]*(time[j]-time[j-1]))]
                s20LH = [1-math.exp(-lam20LH[0]*(time[j]-time[j-1]))]
                s20HH = [1-math.exp(-lam20HH[0]*(time[j]-time[j-1]))]
                s21LL = [1-math.exp(-lam21LL[0]*(time[j]-time[j-1]))]
                s21HL = [1-math.exp(-lam21HL[0]*(time[j]-time[j-1]))]
                s21LH = [1-math.exp(-lam21LH[0]*(time[j]-time[j-1]))]
                s21HH = [1-math.exp(-lam21HH[0]*(time[j]-time[j-1]))]
            else:
                s01LL = [1-math.exp(-lam01LL[0]*tinit)]
                s01HL = [1-math.exp(-lam01HL[0]*tinit)] 
                s01LH = [1-math.exp(-lam01LH[0]*tinit)]
                s01HH = [1-math.exp(-lam01HH[0]*tinit)]
                s02LL = [1-math.exp(-lam02LL[0]*tinit)]
                s02HL = [1-math.exp(-lam02HL[0]*tinit)]
                s02LH = [1-math.exp(-lam02LH[0]*tinit)]
                s02HH = [1-math.exp(-lam02HH[0]*tinit)]
                
                s10LL = [1-math.exp(-lam10LL[0]*tinit)]
                s10HL = [1-math.exp(-lam10HL[0]*tinit)]
                s10LH = [1-math.exp(-lam10LH[0]*tinit)]
                s10HH = [1-math.exp(-lam10HH[0]*tinit)]
                s12LL = [1-math.exp(-lam12LL[0]*tinit)]
                s12HL = [1-math.exp(-lam12HL[0]*tinit)]
                s12LH = [1-math.exp(-lam12LH[0]*tinit)]
                s12HH = [1-math.exp(-lam12HH[0]*tinit)]

                s20LL = [1-math.exp(-lam20LL[0]*tinit)]
                s20HL = [1-math.exp(-lam20HL[0]*tinit)]
                s20LH = [1-math.exp(-lam20LH[0]*tinit)]
                s20HH = [1-math.exp(-lam20HH[0]*tinit)]
                s21LL = [1-math.exp(-lam21LL[0]*tinit)]
                s21HL = [1-math.exp(-lam21HL[0]*tinit)]
                s21LH = [1-math.exp(-lam21LH[0]*tinit)]
                s21HH = [1-math.exp(-lam21HH[0]*tinit)]
        

            Pno0LL = [(1-s01LL[0])*(1-s02LL[0])]
            Pno0HL = [(1-s01HL[0])*(1-s02HL[0])]
            Pno0LH = [(1-s01LH[0])*(1-s02LH[0])]
            Pno0HH = [(1-s01HH[0])*(1-s02HH[0])]

            Pno1LL = [(1-s10LL[0])*(1-s12LL[0])]
            Pno1HL = [(1-s10HL[0])*(1-s12HL[0])]
            Pno1LH = [(1-s10LH[0])*(1-s12LH[0])]
            Pno1HH = [(1-s10HH[0])*(1-s12HH[0])]

            Pno2LL = [(1-s20LL[0])*(1-s21LL[0])]
            Pno2HL = [(1-s20HL[0])*(1-s21HL[0])]
            Pno2LH = [(1-s20LH[0])*(1-s21LH[0])]
            Pno2HH = [(1-s20HH[0])*(1-s21HH[0])]

            P01LL = [(1-Pno0LL[0])*s01LL[0]/(s01LL[0] + s02LL[0])]
            P01HL = [(1-Pno0HL[0])*s01HL[0]/(s01HL[0] + s02HL[0])]
            P01LH = [(1-Pno0LH[0])*s01LH[0]/(s01LH[0] + s02LH[0])]
            P01HH = [(1-Pno0HH[0])*s01HH[0]/(s01HH[0] + s02HH[0])]
            P02LL = [(1-Pno0LL[0])*s02LL[0]/(s01LL[0] + s02LL[0])]
            P02HL = [(1-Pno0HL[0])*s02HL[0]/(s01HL[0] + s02HL[0])]
            P02LH = [(1-Pno0LH[0])*s02LH[0]/(s01LH[0] + s02LH[0])]
            P02HH = [(1-Pno0HH[0])*s02HH[0]/(s01HH[0] + s02HH[0])]

            P10LL = [(1-Pno1LL[0])*s10LL[0]/(s10LL[0] + s12LL[0])]
            P10HL = [(1-Pno1HL[0])*s10HL[0]/(s10HL[0] + s12HL[0])]
            P10LH = [(1-Pno1LH[0])*s10LH[0]/(s10LH[0] + s12LH[0])]
            P10HH = [(1-Pno1HH[0])*s10HH[0]/(s10HH[0] + s12HH[0])]
            P12LL = [(1-Pno1LL[0])*s12LL[0]/(s10LL[0] + s12LL[0])]
            P12HL = [(1-Pno1HL[0])*s12HL[0]/(s10HL[0] + s12HL[0])]
            P12LH = [(1-Pno1LH[0])*s12LH[0]/(s10LH[0] + s12LH[0])]
            P12HH = [(1-Pno1HH[0])*s12HH[0]/(s10HH[0] + s12HH[0])]

            P20LL = [(1-Pno2LL[0])*s20LL[0]/(s20LL[0] + s21LL[0])]
            P20HL = [(1-Pno2HL[0])*s20HL[0]/(s10HL[0] + s21HL[0])]
            P20LH = [(1-Pno2LH[0])*s20LH[0]/(s20LH[0] + s21LH[0])]
            P20HH = [(1-Pno2HH[0])*s20HH[0]/(s20HH[0] + s21HH[0])]
            P21LL = [(1-Pno2LL[0])*s21LL[0]/(s20LL[0] + s21LL[0])]
            P21HL = [(1-Pno2HL[0])*s21HL[0]/(s20HL[0] + s21HL[0])]
            P21LH = [(1-Pno2LH[0])*s21LH[0]/(s20LH[0] + s21LH[0])]
            P21HH = [(1-Pno2HH[0])*s21HH[0]/(s20HH[0] + s21HH[0])]

            # Determine the state of the system and then see if the random number causes a breakpoint to a new segment type
            if curseg == 0 and curtemp == "L" and curhum == "L":
                if p < P01LL[i]:
                    curseg = 1
                elif p < P01LL[i] + P02LL[i]:
                    curseg = 2
            elif curseg == 0 and curtemp == "H" and curhum == "L":
                if p < P01HL[i]:
                    curseg = 1
                elif p < P01HL[i] + P02HL[i]:
                    curseg = 2   
            elif curseg == 0 and curtemp == "L" and curhum == "H":
                if p < P01LH[i]:
                    curseg = 1
                elif p < P01LH[i] + P02LH[i]:
                    curseg = 2
            elif curseg == 0 and curtemp == "H" and curhum == "H":
                if p < P01HH[i]:
                    curseg = 1
                elif p < P01HH[i] + P02HH[i]:
                    curseg = 2
            elif curseg == 1 and curtemp == "L" and curhum == "L":
                if p < P10LL[i]:
                    curseg = 0
                elif p < P10LL[i] + P12LL[i]:
                    curseg = 2           
            elif curseg == 1 and curtemp == "L" and curhum == "H":
                if p < P10LH[i]:
                    curseg = 0
                elif p < P10LH[i] + P12LH[i]:
                    curseg = 2   
            elif curseg == 1 and curtemp == "H" and curhum == "L":
                if p < P10HL[i]:
                    curseg = 0
                elif p < P10HL[i] + P12HL[i]:
                    curseg = 2   
            elif curseg == 1 and curtemp == "H" and curhum == "H":
                if p < P10HH[i]:
                    curseg = 0
                elif p < P10HH[i] + P12HH[i]:
                    curseg = 2               
            elif curseg == 2 and curtemp == "L" and curhum == "L":
                if p < P20LL[i]:
                    curseg = 0
                elif p < P20LL[i] + P21LL[i]:
                    curseg = 1               
            elif curseg == 2 and curtemp == "L" and curhum == "H":
                if p < P20LH[i]:
                    curseg = 0
                elif p < P20LH[i] + P21LH[i]:
                    curseg = 1 
            elif curseg == 2 and curtemp == "H" and curhum == "L":
                if p < P20HL[i]:
                    curseg = 0
                elif p < P20HL[i] + P21HL[i]:
                    curseg = 1 
            elif curseg == 2 and curtemp == "H" and curhum == "H":
                if p < P20HH[i]:
                    curseg = 0
                elif p < P20HH[i] + P21HH[i]:
                    curseg = 1 

            #update the travel by multiplying the slope of the current segment type by the time interval
            if curseg == 0:
                if j > 0:
                    x.append( x[j-1] +  (time[j]-time[j-1]) * slope0)
            elif curseg == 1:
                if j > 0:
                    x.append( x[j-1] + (time[j]-time[j-1]) * slope1)
            else:
                if j > 0:
                    x.append( x[j-1] + (time[j]-time[j-1]) * slope2)

            #Calculae residual
            if j > 0:
                resid.append( travel[j]-x[j])

            #Calculate residual squared
            if j > 0:
                squares.append(resid[j]**2)

            #Calculate sum of squares
            SSR = SSR+squares[j]




        if k > 0:
            xresults.append(x)
            residresults.append(resid)
            SSRresults.append(SSR)
        else:
            xresults[0]=x
            residresults[0]=resid
            SSRresults.append(SSR)      


    #Calculate total sum of squares for the MonteCarlo Simulaiton
    for q in SSRresults:
        TSSR = TSSR + q

    TotSSR[0]=TSSR

        
    t[0]=time

    #t.append(time)


    #Create lists with the input values
    g = 0
    paramNames = ['monteCarlo', 'tempThresh', 'humidThresh','slope0', 'slope1', 'slope2','seg01LL','seg01HL', 'seg01LH','seg01HH','seg02LL','seg02HL','seg02LH','seg02HH','seg10LL','seg10HL', 'seg10LH','seg10HH',
                 'seg12LL','seg12HL','seg12LH','seg12HH','seg20LL','seg20HL', 'seg20LH','seg20HH','seg21LL','seg21HL','seg21LH','seg21HH']
    paramValues = [monteCarlo,tempThresh, humidThresh, slope0, slope1, slope2,seg01LL[g],seg01HL[g], seg01LH[g],seg01HH[g],seg02LL[g],seg02HL[g],seg02LH[g],seg02HH[g],seg10LL[g],seg10HL[g],seg10LH[g],seg10HH[g],
                 seg12LL[g],seg12HL[g],seg12LH[g],seg12HH[g],seg20LL[g],seg20HL[g], seg20LH[g],seg20HH[g],seg21LL[g],seg21HL[g],seg21LH[g],seg21HH[g]]


    # Save data in row format    
    with open(foldername + '/temp'+str(w)+'.csv', mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(t[0])
        csvwriter.writerow(travel)
        for m in range(len(xresults)):
            csvwriter.writerow(xresults[m])
        csvwriter.writerow(temperature)
        csvwriter.writerow(humidity)
        for min in range(len(residresults)):
            csvwriter.writerow(residresults[m])
        csvwriter.writerow(SSRresults)
        csvwriter.writerow(TotSSR)
        csvwriter.writerow(paramNames)
        csvwriter.writerow(paramValues)
            
    # Save data in column format
    pandas.read_csv(foldername + '/temp'+str(w)+'.csv', header=None).T.to_csv(foldername + '/results' + str(w) +'.csv', header=False, index=False) 

