import sys
import csv

data = sys.stdin.readlines()
csvreader = csv.reader(data, delimiter=',')

data = []
for row in csvreader:
    data.append(row)
print(data)