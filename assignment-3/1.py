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
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            if i != j:
                dist_matrix[i][j] = round(math.sqrt((data[i+1][0] - data[j+1][0])**2
                                                    + (data[i+1][1] - data[j+1][1])**2
                                                    + (data[i+1][2] - data[j+1][2])**2), 2)

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

""" FOR FILE test_q1.txt """
            
getChain("test_q1.txt")

""" FOR FILE test_q2.txt """

getChain("data_q1.txt")







