import sys
import csv
from geopy.distance import vincenty


# inputLine = open(sys.stdin)
# ofile = open("final.csv", "w")
# writer = csv.writer(ofile, delimiter=',')

inputFile = sys.stdin
outputFile = sys.stdout
prevLine = ""

for line in inputFile:
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
            timeSpent = int(lineArray[0]) - int(prevLineArray[0])

            # # Get speed in unit of mile per hour
            # if time != 0:
            #     speed = 3600 * distance / time
            # else:
            #     speed = 0
            # result = [lineArray[4], speed, lineArray[3], lineArray[5]]
            # writer.writerow(result)
            # outputfile.write("{0},{1},{3},{2}".format(lineArray[4], speed, lineArray[3].strip(), lineArray[5]))

            # Output: osm_id / time spent / distance / road type / street name
            outputFile.write('%s|%s,%s,%s,%s|%s,%s,%s|%s\n' % (prevLine.split(",")[4], osm_id, timeSpent, distance, prevLineArray[5].strip(), lineArray[5].strip(), "12", prevLineArray[3].strip(), lineArray[3].strip()))
            

    prevLine = line

outputFile.flush()
