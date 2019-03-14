
# coding: utf-8



## Read Data
import fileinput

data = []
idx = 0
for line in fileinput.input():
    if fileinput.isfirstline():
        n, k, m = line.split(' ')
    else:
        lon, lat = line.split(' ')
        data.append([float(lon), float(lat), idx])
        idx +=1

# In[8]:


def dist(x, y, m):
    
    results =[]
    # if x and y are multiple cluster
    if isinstance(x[0], list):
        if isinstance(y[0], list):    
            dist = []
            for x_points in x:
                for y_points in y:
                    result = distance(x_points, y_points)
                    results.append(result)
        # if x is multiple clusters
        else:
            for x_points in x:
                results.append(distance(x_points, y))
    # if y is multiple
    else:
        if isinstance(y[0], list):
            dist = []
            for y_points in y:
                results.append(distance(x,y_points))
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


# In[9]:


def distance(x,y):
    dist = []
    for idx in range(len(x)-1):
        dist.append((x[idx]-y[idx])**2)
    return sum(dist)**(1/2)


# In[282]:


data = [[51.5217, 30.114], [27.9698, 27.0568], [10.6233, 52.4207], [122.1483, 6.9586], [146.4236, -41.3457]]


# In[19]:


data = [[51.5217, 30.114, 0], [27.9698, 27.0568, 1], [10.6233, 52.4207, 2], [122.1483, 6.9586, 3], [146.4236, -41.3457, 4]]


# In[20]:


# Repeat splitting until getting k clusters
k=2
n=len(data)
while n!=k:
    # distance matrix
    dist_mat = [[float('inf') for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            # print(str(i)+', '+str(j))
            dist_mat[i][j] = dist(data[i], data[j], m)
    dist_list = [(i,j, dist_element) for i, dist_list in enumerate(dist_mat) for j,dist_element in enumerate(dist_list)]
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


# In[22]:


# put cluster results
results = dict()
for cluster, data_list in enumerate(data):
    # when cluster is list of list
    if isinstance(data_list[0], list):
        for data_element in data_list:
            results.update({data_element[-1]:cluster})
    else:
        results.update({data_list[-1]:cluster})


# In[39]:


for idx in range(len(results.items())):
    print(results.get(idx))

