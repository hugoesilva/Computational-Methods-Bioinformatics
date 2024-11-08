import math

pseudo_valence_angle_bottom = 60
distance_threshold = 0.12

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

def build_chain(dist_matrix, chain, node, to_visit, direction):
    if len(chain) == 1 and direction != "right":
        to_visit.remove(node)

    for point in to_visit:
        if (point != node):
            if abs(dist_matrix[node-1][point-1] - 3.8) <= distance_threshold and point in to_visit:
                if (len(chain) == 1 and direction == "left"):
                    direction = ''
                    continue
                chain.append(point)
                to_visit.remove(point)
                return build_chain(dist_matrix, chain, point, to_visit, '')
            
            
def first_filter_alpha_carbon_data(dist_matrix, data):
    # keep only points that dist 3.8 +- distance_threshold from at least 1 other point
    potential_alpha_C = {}
    for key1 in data:
        for key2 in data:
            if key1 != key2:
                if abs(dist_matrix[key1-1][key2-1] - 3.8) <= distance_threshold:
                    if key1 in potential_alpha_C:
                        potential_alpha_C[key1].append(key2)
                    else:
                        potential_alpha_C[key1] = [key2]
    return potential_alpha_C

def calculate_angle_3_points(atom1, atom2, atom3, data):
    vector_1_2 = [data[atom2][0] - data[atom1][0], data[atom2][1] - data[atom1][1], data[atom2][2] - data[atom1][2]]
    vector_1_3 = [data[atom3][0] - data[atom1][0], data[atom3][1] - data[atom1][1], data[atom3][2] - data[atom1][2]]

    norm_vector_1_2 = math.sqrt(vector_1_2[0]**2 + vector_1_2[1]**2 + vector_1_2[2]**2)
    norm_vector_1_3 = math.sqrt(vector_1_3[0]**2 + vector_1_3[1]**2 + vector_1_3[2]**2)

    angle = math.degrees(math.acos((vector_1_2[0]*vector_1_3[0] + vector_1_2[1]*vector_1_3[1] + vector_1_2[2]*vector_1_3[2])/(norm_vector_1_2*norm_vector_1_3)))

    return [angle, atom2, atom3]


def remove_atoms_just_connected_to_each_other(potential_alpha_C):
    keys_to_remove = []
    for key in potential_alpha_C:
        if len(potential_alpha_C[key]) == 1:
            connection = potential_alpha_C[key][0]
            if len(potential_alpha_C[connection]) == 1:
                # remove key from dict
                keys_to_remove.append(key)
                keys_to_remove.append(connection)

    for key in keys_to_remove:
        if key in potential_alpha_C:
            del potential_alpha_C[key]


def create_angle_dict(potential_alpha_C, data):
    angles = {}
    for key in potential_alpha_C:
        angles[key] = []
        for i in range(0, len(potential_alpha_C[key])):
            for j in range(i, len(potential_alpha_C[key])):
                if i != j:
                    points_angle = calculate_angle_3_points(key, potential_alpha_C[key][i], potential_alpha_C[key][j], data)
                    angles[key].append(points_angle)
    return angles



def first_filter_angles(angles):
    """ 
    removes angle combinations that have an angle that is not in the range of degrees
    """
    for key in angles:
        combinations_to_remove = []
        for combination in angles[key]:
            if (combination[0] < pseudo_valence_angle_bottom):
                combinations_to_remove.append(combination)
        for combination in combinations_to_remove:
            angles[key].remove(combination)


def remove_empty_angles(angles):
    angles_to_remove = []

    for key in angles:
        if angles[key] == []:
            angles_to_remove.append(key)
            continue

    for key in angles_to_remove:
        if key in angles:
            del angles[key]


def second_filter_angles(angles):
    """ 
        removes angle combinations that have a point that is not in the angles dict
        if an angle has no combinations, remove it from the dict
    """
    pre_angles = []

    while pre_angles != angles:

        angles_to_remove = []

        for key in angles:
            combinations_to_remove = []
            for combination in angles[key]:
                if combination[1] not in angles or combination[2] not in angles:
                    combinations_to_remove.append(combination)
            for combination in combinations_to_remove:
                angles[key].remove(combination)
            if angles[key] == []:
                angles_to_remove.append(key)

        pre_angles = angles.copy()

        for key in angles_to_remove:
            if key in angles:
                del angles[key]

def createChain(angles, direction, visited, left_chain, right_chain, chains):

    last_left_atom = left_chain[len(left_chain)-1]
    last_right_atom = right_chain[len(right_chain)-1]

    if (len(angles) == len(visited)):
        chains.append(left_chain[::-1] + right_chain[1:])
        return
    
    # when direction is left we want to build the right chain and vice versa
    if direction == "left":
        for combination in angles[last_left_atom]:

            second_to_last_atom = left_chain[len(left_chain)-2]
            need_break = False


            if second_to_last_atom not in combination:
                continue

            first_element_comb = combination[1]
            second_element_comb = combination[2]
            new_element = 0

            if first_element_comb == second_to_last_atom:
                new_element = second_element_comb
            else:
                new_element = first_element_comb

            for i in range(1, 3):
                if combination[i] in visited and second_to_last_atom != combination[i]:
                    need_break = True
            if need_break:
                continue

            left_chain.append(new_element)
            visited.append(new_element)
            createChain(angles, "right", visited, left_chain, right_chain, chains)
            createChain(angles, "left", visited, left_chain, right_chain, chains)
            left_chain = left_chain[0:len(left_chain)-1]
            visited = visited[0:len(visited)-1]
    else:
        for combination in angles[last_right_atom]:
                
                second_to_last_atom = right_chain[len(right_chain)-2]
                need_break = False
    
    
                if second_to_last_atom not in combination:
                    continue
    
                first_element_comb = combination[1]
                second_element_comb = combination[2]
                new_element = 0
    
                if first_element_comb == second_to_last_atom:
                    new_element = second_element_comb
                else:
                    new_element = first_element_comb
    
                for i in range(1, 3):
                    if combination[i] in visited and second_to_last_atom != combination[i]:
                        need_break = True
                if need_break:
                    continue
    
                right_chain.append(new_element)
                visited.append(new_element)
                createChain(angles, "left", visited, left_chain, right_chain, chains)
                createChain(angles, "right", visited, left_chain, right_chain, chains)
                right_chain = right_chain[0:len(right_chain)-1]
                visited = visited[0:len(visited)-1]
            

    chains.append(left_chain[::-1] + right_chain[1:])


""" def createChain(angles, chain, chains, visited):

    last_atom = chain[len(chain)-1]

    found_combination = False

    for combination in angles[last_atom]:
        if combination[1] not in visited and combination[2] not in visited:
            found_combination = True
            break

    if not found_combination:
        chains.append(chain)
        return

    
    if (len(angles) == len(visited)):
        chains.append(chain)
        return
    
    for combination in angles[last_atom]:
        need_break = False
        for i in range(1, 3):
            if combination[i] in visited:
                need_break = True
        if need_break:
            continue
        chain.append(combination[1])
        chain.append(combination[2])
        visited.append(combination[1])
        visited.append(combination[2])
        createChain(angles, chain, chains, visited)
        chain = chain[0:len(chain)-2]
        visited = visited[0:len(visited)-2] """
    
    
    
    




def getChain(filename):

    data = create_data(filename)
    dist_matrix = create_distance_matrix(len(data))
    fill_distance_matrix(dist_matrix, data)

    potential_alpha_C = first_filter_alpha_carbon_data(dist_matrix, data)

    # remove atoms that only have connections to each other.
    remove_atoms_just_connected_to_each_other(potential_alpha_C)

    angles = create_angle_dict(potential_alpha_C, data)


    # remove combinations that are not in the range of degrees
    first_filter_angles(angles)
    remove_empty_angles(angles)

    second_filter_angles(angles)

    # mash all the angles in a list
    all_alpha_carbons = [key for key in angles]
    # make every element in the list unique
    all_alpha_carbons = list(dict.fromkeys(all_alpha_carbons))
    
    chains = []

    max_len_chains = []
    max_len_chain = []
    max_len = 0

    for atom in angles:

        for combination in angles[atom]:
            left_chain = [atom, combination[1]]
            right_chain = [atom, combination[2]]
            visited = [atom, combination[1], combination[2]]
            createChain(angles, "left", visited.copy(), left_chain.copy(), right_chain.copy(), chains)
            createChain(angles, "right", visited.copy(), left_chain.copy(), right_chain.copy(), chains)

        for chain in chains:
            if len(chain) > max_len:
                max_len = len(chain)
                max_len_chain = chain.copy()
                max_len_chains = []
            elif len(chain) == max_len:
                max_len_chains.append(chain)
        break;

    print(len(list(set(max_len_chain))))

    # delete repeated chains
    chains_to_remove = []
    for i in range(0, len(max_len_chains) - 1):
        if max_len_chains[i] in max_len_chains[i+1:]:
            chains_to_remove.append(max_len_chains[i])

    for chain in chains_to_remove:
        max_len_chains.remove(chain)

    for chain in max_len_chains:
        print(chain)


getChain('data_q2.txt')

#160, 117, 83, 69, 63, 39, 19, 4, 3, 16, 27, 54, 72, 70
#70, 72, 54, 27, 16, 3, 4, 19, 39, 63, 69, 83, 117, 160, 228, 257, 220, 230, 244, 291, 280, 241, 177, 203, 237, 256, 266, 301, 294, 243, 217, 189, 205, 223, 273, 262, 215, 242, 207, 129, 158, 169, 142, 86]