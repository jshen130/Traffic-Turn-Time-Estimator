import csv
import sys




ifile = open("dataset/completeData.csv", "rb")
reader = csv.reader(ifile)
ofile0 = open("Train_XY.csv", "w")
ofile1 = open("Train_X.csv", "w")
ofile2 = open("Train_Y.csv", "w")
ofile3 = open("Test_X.csv", "w")
ofile4 = open("Test_Y.csv", "w")
ofile5 = open("Test_XY.csv", "w")
# writer1 = csvwriter(ofile1, delimiter=',')
# writer2 = csv.writer(ofile2, delimiter=',')




count = 0
for row in reader:
    # Save header row.
    if (count % 10 == 0):
        ofile4.write('%s\n' % row[2])
        ofile3.write('%s,%s,%s,%s,%s,%s,%s\n' % (row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        ofile5.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    else:
        ofile2.write('%s\n' % row[2])
        ofile1.write('%s,%s,%s,%s,%s,%s,%s\n' % (row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        ofile0.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    count += 1




