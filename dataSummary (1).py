import csv
import sys

inputfile  = sys.stdin
reader = csv.reader(inputfile)

ofile  = sys.stdout
writer = csv.writer(ofile, delimiter=',')

rownum = 0
prevRow = ""
osm_id = 0
for row in reader:
    # Save header row.
    if row[0] == "tstamp":
        continue
    else:

        if (osm_id != row[4]):
            writer.writerow(prevRow[0:6])
            writer.writerow(row[0:6])
            osm_id = row[4]

        prevRow = row

        # for col in row:
        #     print '%-8s: %s' % (header[colnum], col)
        #     colnum += 1


    rownum += 1

inputfile.close()
ofile.close()