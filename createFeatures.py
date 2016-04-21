from pandas import DataFrame, read_csv
import math
import re
import datetime
import pandas as pd

# use regex to extract date patterns in filename
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
date_r = r'(0[1-9]|[12]\d|3[01])(' + '|'.join(months) + ')'
year_r = r'(201[0-5])'
def extractDate(filename):
    datematch = re.search(date_r, filename)
    yearmatch = re.search(year_r, filename)
    if datematch and yearmatch:
        return {'month': datematch.group(2),
                'day': datematch.group(1),
                'year':yearmatch.group(1)}

def parseDay(date):
    month, day, year = date['month'], date['day'], date['year']
    weekday = datetime.datetime.strptime(day+month+year, '%d%b%Y').weekday()
    if month == "Jul" and day == "04": #holiday
        return 2
    elif weekday <= 4: # mon = 0, fri = 4
        return 1
    else: # sat, sun = 5, 6
        return 2
    
# lookup table
roads = {'unclassified':0, 'primary':1, 'secondary':2, 'tertiary':3,
         'trunk':4, 'motorway':5, 'primary_link':6, 'secondary_link':7,
         'tertiary_link':8, 'trunk_link':9, 'motorway_link':10,
         'residential':11, 'service':12}

# time interval calculation
intervals = [[7, 10], [16, 19], [10, 16], [19, 23], [23, 7]]
intervals = map(lambda interval: map(lambda hour:hour*60*60, interval), intervals)
modular = 24 * 60 * 60
def parseTimeInterval(time):
    time = time%modular
    for i in range(len(intervals)):
        start, end = intervals[i] # use wraparound intervals
        if (time-start)%modular <= (end-start)%modular:
            return i
    
# temporarily hardcode filename for now
dataFile = 'SOTU2014_DOE2_MPS28Jan_1946t_lat_long.csv'
data = pd.read_csv(dataFile)

# get the required mapping files
turnFile = 'turnOsmPair.csv'
turns = pd.read_csv(turnFile)
def findTurn(start, end):
    turn = turns.loc[(turns['start_osm_way_id'] == start) &
                     (turns['end_osm_way_id'] == end),'t_type']
    if turn.shape[0]:
        return turn.values[0]

outFile = open('out.csv', 'w')
outFile.write("road_type, timestamp, day_type, duration, turn_type\n")
# see if we want to add geographic features (start, end)
#outFile.write("road_type, timestamp, day_type, duration, turn_type, osm_start, osm_end\n")

# iterate through each entry in data file
for index, row in data.iterrows():
    # if we're at the last entry
    if index == data.shape[0] - 1:
        break
    nextrow = data.ix[index+1]
    road_type = roads[row['osm_highway']]
    timestamp = parseTimeInterval(row['timestamp'])
    day_type = parseDay(extractDate(dataFile))
    duration = row['duration']
    startOsm = row['osm_osm_id']
    endOsm = nextrow['osm_osm_id']
    turn_type = findTurn(startOsm, endOsm)
