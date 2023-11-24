""" ------------------ Question 2 ------------------ """

import math

def create_data(filename):
    data = {}
    with open(filename) as f:
        line = f.readline()
        counter = 1
        while line:
            line = line.strip()
            line = line.split(' ')
            data[counter] = [line[i] for i in range(0, len(line))]
            line = f.readline()
            counter += 1
            
    for key in data:
        #move \t and everything before it from string of element data[key][0]
        data[key][0] = data[key][0].split('\t')[1]
        #convert string to float
        for i in range(0, len(data[key])):
            data[key][i] = float(data[key][i])

    return data

# distance matrix

def create_distance_matrix(len):
    dist_matrix = []
    for i in range(0, len):
        row = []
        for j in range(0, len):
            row.append(0)
        dist_matrix.append(row)
    return dist_matrix

# fill distance matrix

def fill_distance_matrix(dist_matrix, data):
    counter1 = 0
    for key1 in data:
        counter2 = 0
        for key2 in data:
            if key1 != key2:
                dist_matrix[counter1][counter2] = round(math.sqrt((data[key1][0] - data[key2][0])**2
                                                    + (data[key1][1] - data[key2][1])**2
                                                    + (data[key1][2] - data[key2][2])**2), 2)
            counter2 += 1
        counter1 += 1
                

""" for i in range(0, len(dist_matrix)):
    print(dist_matrix[i]) """


def build_chain(dist_matrix, chain, node, to_visit, direction):
    if len(chain) == 1:
        to_visit.remove(node)
    if len(to_visit) == 0:
        return
    else:
        for i in range(0, len(dist_matrix)):
            if (node == i):
                continue
            if abs(dist_matrix[node][i] - 3.8) <= 0.1 and i in to_visit:
                if (node == 0 and direction == 'left'):
                    direction = ''
                    continue
                chain.append(i+1)
                to_visit.remove(i)
                return build_chain(dist_matrix, chain, i, to_visit, '')
            

def getChain(filename):

    data = create_data(filename)
                

    dist_matrix = create_distance_matrix(len(data))

    fill_distance_matrix(dist_matrix, data)
                

    left_chain = [1]
    right_chain = [1]
                

    build_chain(dist_matrix, right_chain, 0, [i for i in range(0, len(dist_matrix))], 'left')

    build_chain(dist_matrix, left_chain, 0, [i for i in range(0, len(dist_matrix))], 'right')

    #chain = inverted left + right
    left_chain = left_chain[::-1]
    chain = left_chain[0:len(left_chain)-1]+ right_chain

    print("For file " + filename + " the chain is: ")

    for i in range(0, len(chain)):
        print(chain[i])



data = create_data("data_q2.txt")

dist_matrix = create_distance_matrix(len(data))

fill_distance_matrix(dist_matrix, data)

def filter_data(dist_matrix, data):
    # if distance between point a and point b is less than 3.5 and there is not a point that dists 3.8 +- 0.1 from a, remove a
    for i in range(0, len(dist_matrix)):
        for j in range(0, len(dist_matrix)):
            if i != j:
                if dist_matrix[i][j] < 3.5:
                    for k in range(0, len(dist_matrix)):
                        if k != i and k != j:
                            if abs(dist_matrix[i][k] - 3.8) <= 0.1:
                                break
                        if k == len(dist_matrix) - 1:
                            if i+1 in data:
                                data.pop(i+1)
                            i -= 1
                            break

def separate_amino_acids(dist_matrix, threshold=1.5):
    n = len(dist_matrix)
    groups = [[i] for i in range(n)]  # Initialize groups (each atom starts in its own group)

    # Iterate over the distance matrix to group atoms
    for i in range(n):
        for j in range(i + 1, n):
            if dist_matrix[i][j] < threshold:
                # Find the groups that i and j belong to
                group_i_index = next(index for index, group in enumerate(groups) if i in group)
                group_j_index = next(index for index, group in enumerate(groups) if j in group)

                # Merge groups if two atoms are within the threshold distance and are not in the same group already
                if group_i_index != group_j_index:
                    groups[group_i_index].extend(groups[group_j_index])
                    del groups[group_j_index]

    return groups




#print("pre data length: " + str(len(data)))


#filter_data(dist_matrix, data)

#print("post data length: " + str(len(data)))

#new_dist_matrix = create_distance_matrix(len(data))

#fill_distance_matrix(new_dist_matrix, data)

amino_acids = separate_amino_acids(dist_matrix, 3.5)

#calculate the average length of the groups of amino-acids

def get_average_length(amino_acids):
    sum = 0
    for group in amino_acids:
        sum += len(group)
    return sum/len(amino_acids)

i = 0.01
while(get_average_length(amino_acids) > 3):
    amino_acids = separate_amino_acids(dist_matrix, threshold= 3-i)
    i += 0.01

#print(amino_acids)
#for each amino acid group now calculate the distance matrix and select the point that is the closest to all points



#print(alpha_carbons)


#build the chain

            

build_chain(dist_matrix, right_chain, 0, [i for i in range(0, len(dist_matrix))], 'left')

build_chain(dist_matrix, left_chain, 0, [i for i in range(0, len(dist_matrix))], 'right')

#chain = inverted left + right
left_chain = left_chain[::-1]
chain = left_chain[0:len(left_chain)-1]+ right_chain

for i in range(0, len(chain)):
    print(chain[i])
                






