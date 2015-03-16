# import csv module
import csv
# open and read the csv file into memory
file = open('host_ip_conf.csv','rU')
reader = csv.reader(file)
lineCount = 0
lineTarget = 5
for line in reader:
    if lineCount == lineTarget:
        print line[1]
    lineCount += 1