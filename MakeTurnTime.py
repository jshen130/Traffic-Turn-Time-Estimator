import sys
import csv
from geopy.distance import vincenty


# inputLine = open(sys.stdin)
# ofile = open("final.csv", "w")
# writer = csv.writer(ofile, delimiter=',')

inputFile = sys.stdin
outputFile = sys.stdout



prevLine = ""
straightTimeSpent = 0


# lookup table
roads = {'unclassified':2, 'primary':1, 'secondary':1, 'tertiary':1,
         'trunk':0, 'motorway':0, 'primary_link':1, 'secondary_link':1,
         'tertiary_link':1, 'trunk_link':0, 'motorway_link':0,
         'residential':2, 'service':2}


def classifyTime(time):

    # change TimeZone
    if time - 5 * 3600 < 0:
        time += ((24-5) * 3600)
    else:
        time -= 5 * 3600
    time %= 24 * 3600

    if 7 * 3600 <= time < 10 * 3600:
        return 1
    elif 16 * 3600 <= time < 19 * 3600:
        return 0
    elif 10 * 3600 <= time < 16 * 3600:
        return 2
    elif 19 * 3600 <= time < 23 * 3600:
        return 3
    else:
        return 4


def findTurnType(osm1, osm2):
    ifile  = open('dataset/turnOsmPair.csv', "rb")
    turnReader = csv.reader(ifile)
    rownum = 0
    for row in turnReader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            if (row[0] == osm1 and row[1] == osm2) or (row[1] == osm1 and row[0] == osm2):
                turntype = int(row[2])
                if turntype == 5:
                    return 0
                elif turntype in [6, 7, 8]:
                    return 1
                elif turntype in [2, 3, 4]:
                    return 2
                elif turntype in [0, 1]:
                    return 3
        rownum += 1
    return 3


def findNumLane(osm):
    ifile2  = open('dataset/wayData.csv', "rb")
    laneReader = csv.reader(ifile2)
    rownum = 0
    for row in laneReader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            if row[0] == osm:
                return int(row[5])
        rownum += 1
    return 0

count = 0

for line in inputFile:

    count = count + 1
    if (count % 1000 == 0):
        sys.stderr.write("processing line %s\n"%(count))

    lineArray = line.split(",")

    if len(lineArray) == 1:
        continue

    if prevLine != "":
        osm_id = lineArray[4]
        if osm_id != prevLine.split(",")[4]:
            prevLineArray = prevLine.split(",")
            coordinate1 = (lineArray[1], lineArray[2])
            coordinate2 = (prevLineArray[1], prevLineArray[2])
            # print str(coordinate1) + "   " + str(coordinate2)

            # Get distance b/w start and end point
            distance = vincenty(coordinate1, coordinate2).miles

            # Get time difference b/w start and end point
            timeSpent = int(lineArray[0]) - int(prevLineArray[0]) + straightTimeSpent

            # Get time class
            timeClass = classifyTime(int(prevLineArray[0]))

            # Get day class (1: weekday, 2: weekend, holiday)
            dayClass = 2

            # Output: osm_id1 / osm_id2 / time spent / r_type1 / r_type2 / laneNum1 / laneNum2 / timeClass / dayClass / turnType
            if 0 < int(timeSpent) < 400:
                outputFile.write('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n' %
                                 (int(prevLine.split(",")[4]), int(osm_id), timeSpent, roads[prevLineArray[5].strip()],
                                  roads[lineArray[5].strip()], findNumLane(prevLine.split(",")[4]), findNumLane(osm_id), timeClass, dayClass, findTurnType(prevLine.split(",")[4], osm_id)))
        # Save time spent on one osm_id
        else:
            prevLineArray = prevLine.split(",")

            straightTimeSpent = int(lineArray[0]) - int(prevLineArray[0])


    prevLine = line

outputFile.flush()

