## Read Data
import fileinput

data = []
idx = 0
for line in fileinput.input():
    if fileinput.isfirstline():
        n, k, m = line.split(' ')
        k = int(k)
        n = int(n)
        m = int(m)
    else:
        lon, lat = line.split(' ')
        data.append([float(lon), float(lat), idx])
        idx +=1

def dist(x, y, m):
    
    results =[]
    # if x and y are multiple cluster
    isXlist = isinstance(x[0], list)
    isYlist = isinstance(y[0], list)
    if isXlist:
        if isYlist:    
            dist = []
            [results.append(distance(x_points, y_points)) for x_points in x for y_points in y]
        # if x is multiple clusters
        else:
            [results.append(distance(x_points, y)) for x_points in x]
                
    # if y is multiple
    else:
        if isYlist:
            dist = []
            [results.append(distance(x,y_points)) for y_points in y]
                
        # neither is multiple
        else:
            results.append(distance(x,y))
    if m==0:
        temp = min(results)
    elif m==1:
        temp = max(results)
    else:
        temp = sum(results)/len(results)
    return temp

def distance(x,y):
    dist = []
    [dist.append((x[idx]-y[idx])**2) for idx in range(len(x)-1)]
    return sum(dist)**(1/2)
        
# when k is larger than n
if n < k:
    for cluster in arange(n):
        print(idx)
# when k is 1
elif k ==1:
    for cluster in arange(n):
        print(0)
        
else:
    # Repeat splitting until getting k clusters
    while n>k:
        # distance matrix
        dist_mat = [[float('inf') for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                dist_mat[i][j] = dist(data[i], data[j], m)
        dist_list = [(i,j, dist_element) for i, dist_list in enumerate(dist_mat) for j, dist_element in enumerate(dist_list)]
        i, j, _ = min(dist_list, key=lambda t: t[2])

        # when i is list of list
        if isinstance(data[i][0], list):
            # j is list of list
            if isinstance(data[j][0], list):
                new_data = data[i]+data[j]
            else:
                new_data = data[i]+[data[j]]
        else:
            if isinstance(data[j][0], list):
                new_data = [data[i]]+data[j]
            else:
                new_data = [data[i]]+[data[j]]

        data.pop(i)
        data.pop(j-1)
        data.reverse()
        data.append(new_data)
        data.reverse()
        n = len(data)

    # put cluster results
    results = dict()
    for cluster, data_list in enumerate(data):
        # when cluster is list of list
        if isinstance(data_list[0], list):
            [results.update({data_element[-1]:cluster}) for data_element in data_list]
        else:
            results.update({data_list[-1]:cluster})

    for i in range(idx):
        print(results.get(i))