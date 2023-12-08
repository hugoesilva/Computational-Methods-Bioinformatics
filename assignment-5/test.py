#1 Write a program that reads the trajectory file (traj-2.txt). The columns represent the dimensions. As you will see, you will be working with a two-dimensional system.

file = open("traj-2.txt", "r")
lines = file.readlines()
file.close()

import numpy as np
from scipy.cluster.vq import kmeans2

np.random.seed(0)

num_clusters = 100

x = []
y = []
for line in lines:
    x.append(float(line.split()[0]))
    y.append(float(line.split()[1]))


data = np.array([x, y]).T
centroids, labels = kmeans2(data, num_clusters, minit='points')

#Plot the trajectory itself as well as a 2D histogram.

import matplotlib.pyplot as plt
#plot the points and color them by their cluster
plt.scatter(data[:,0], data[:,1], c=labels)
plt.show()

plt.hist2d(x, y, bins=num_clusters)
plt.show()

#count matrix for the transition probabilities between the clusters

time_lag = 1
#counter = 1

count_matrix = np.zeros((num_clusters, num_clusters))

for i in range(1, len(labels), time_lag):
    current_cluster = labels[i]
    previous_cluster = labels[i-1]
    count_matrix[previous_cluster][current_cluster] += 1
    #counter += 1

#print(counter)
count_matrix

transition_matrix = np.zeros((num_clusters, num_clusters))

for i in range(num_clusters):
    row_sum = sum(count_matrix[i])
    for j in range(num_clusters):
        transition_matrix[i][j] = count_matrix[i][j] / row_sum

transition_matrix
