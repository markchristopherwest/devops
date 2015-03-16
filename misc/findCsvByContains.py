import csv
# open and read the csv file into memory
file = open('host_ip_conf.csv','rU')
reader = csv.reader(file)
lineCount = 0
#Pull in the Bladename
lineContains = "Puhi"
for line in reader:
    if line[0] == lineContains:
        print line[0] +" has the IP addres of " + line[1]
    lineCount += 1