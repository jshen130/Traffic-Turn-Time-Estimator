from pandas import DataFrame, read_csv
import math
import pandas as pd

turnFile = 'validturns.csv'
turns = pd.read_csv(turnFile).ix[:, :'t_type']

convertFile = 'osmToOsrmMap.csv'
conversions = pd.read_csv(convertFile)

wayFile = 'wayData.csv'
ways = pd.read_csv(wayFile).ix[:, ['osmid','startnode','endnode']]

outFile = open('turnOsmPair.csv', 'w')
outFile.write("start_osm_way_id,end_osm_way_id,t_type\n");

def convert(osrm):
    entry = conversions.loc[conversions['OSRM_id'] == osrm]
    if not entry.shape[0]:
        return float('NaN')
    else:
        return entry.iloc[0]['OSM_id']


def findWay(start, end):
    entry = ways.loc[(ways['startnode'] == start) & (ways['endnode'] == end),'osmid']
    if not entry.shape[0]:
        return float('NaN')
    else:
        return entry.values[0]

success = 0
failure = 0
counter = 0
for index, row in turns.iterrows():
    counter += 1
    if counter % 1000 == 0:
        print("{:10.2f}".format(counter/1362.0)  + "%")
        print("    Success: " + "{:10.2f}".format(success/(counter + 0.0)))
        print("    Failure: " + "{:10.2f}".format(failure/(counter + 0.0)))
    osrm_nodes = [row['node_u'], row['node_v'], row['node_w']]
    osm_nodes = map(convert, osrm_nodes)
    way1 = findWay(osm_nodes[0], osm_nodes[1])
    way2 = findWay(osm_nodes[1], osm_nodes[2])
    if math.isnan(way1) or math.isnan(way2):
        failure += 1
        continue
    else:
        success += 1
        outFile.write(str(way1) + "," + str(way2) + "," + str(row['t_type']) + "\n");
