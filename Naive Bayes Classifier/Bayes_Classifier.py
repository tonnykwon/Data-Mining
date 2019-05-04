## read data
import sys
import csv
from collections import Counter

data = sys.stdin.readlines()
csvreader = csv.reader(data, delimiter=',')

data = []
for row in csvreader:
    data.append(row)
    
# train test split
class_type = list(zip(*data))[-1]
train_idx = [idx for idx, label in enumerate(class_type) if label!='-1' ][1:]
test_idx = [idx for idx, label in enumerate(class_type) if label=='-1' ]
train_data = [list(map(int,column[1:])) for idx, column in enumerate(data) if idx in train_idx]
test_data = [list(map(int,column[1:])) for idx, column in enumerate(data) if idx in test_idx]

# calculate py
train_class_type = list(zip(*train_data))[-1]
# counts for each class. Setting default 0
counts = {}
for label in range(1,8):
    counts[label] = 0
counts.update(Counter(train_class_type))
n = sum(counts.values())
py = [(key, (item+0.1)/(n+item*0.1)) for key, item in counts.items()]


# calculate set of features and number of features
feature_set = []
for feature_idx, column in enumerate(list(zip(*train_data))):
    # leg features
    if feature_idx == 12:
        feature_set.append(((0,2,4,5,6,8), 6))
    # class
    elif feature_idx == 16:
        feature_set.append((tuple(range(1,8)), 7))
    else:
        feature_set.append(((0,1), 2)) 

# seperate data by class
seperated = {}
for label in list(range(1,8)):
    seperated[label] = []
for column in train_data:
    seperated[column[-1]].append(column)
    
# counts each feature for each class
# for each items' feature, count each feature attributes
feature_counts = {}
for key, items in seperated.items():
    if not items:
        for idx, features in enumerate(feature_set):
            feature_counts[(key, idx)] = Counter({feature:0 for feature in features[0]})
    for idx, item in enumerate(list(zip(*items))):
        # get counts for zero counts
        if (key,idx) not in feature_counts:
            feature_counts[(key,idx)] = Counter({key:0 for key in feature_set[idx][0]})
        feature_counts[(key, idx)].update(list(item))


# calculate pxy based on counts of each attribute and feature number
pxy = {}
for key, item in feature_counts.items():
    num_class = len(list(item.elements()))
    # feature: feature attributes, num: feature attributes counts
    for feature, num in item.items():
        # class, feature, attribute 
        pxy[(key[0], key[1], feature)] = (num+0.1)/(num_class+0.1*feature_set[key[1]][1])
        
# predict test sets by calculating pxy * py
test_pxy = []
for test_set in test_data:
    test_set_pxy=[]
    for feature_idx, feature in enumerate(test_set[:-1]):
        test_set_pxy.append([pxy.get((label, feature_idx, feature)) for label, prob in py])
    test_pxy.append(test_set_pxy)
    

# multiply all elements in pxy
pxy_list = []
for test_set_pxy in test_pxy:
    pxy_set_list = []
    for elements in list(zip(*test_set_pxy)):
        result = 1
        for element in elements:
            result *= element
        pxy_set_list.append(result)
    pxy_list.append(pxy_set_list)

# calculate pxy and py
results = [[pxy_set_list[label-1]*prob for label, prob in py] for pxy_set_list in pxy_list]

# predict test label
for result in results:
    print(result.index(max(result))+1)