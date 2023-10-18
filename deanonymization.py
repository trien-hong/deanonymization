import networkx as nx
import math
import statistics

file1 = "seed_G1.edgelist"
file2 = "seed_G2.edgelist"
file3 = "seed_node_pairs.txt"

G1 = nx.read_edgelist(file1, create_using=nx.Graph(), nodetype=int)
G2 = nx.read_edgelist(file2, create_using=nx.Graph(), nodetype=int)

print(G1)
print(G2)

array_G1 = list(nx.nodes(G1))
array_G2 = list(nx.nodes(G2))

print(array_G1)
print(array_G2)

seed_pair_G1 = []
seed_pair_G2 = []

with open(file3, "r") as text_file:
    for line in text_file:
        line = line.strip()
        number1, number2 = line.split(" ")
        seed_pair_G1.append(int(number1))
        seed_pair_G2.append(int(number2))

non_matched_G1 = [x for x in array_G1 if (x not in seed_pair_G1)]
non_matched_G1.sort()
non_matched_G2 = [x for x in array_G2 if (x not in seed_pair_G2)]
threshold = 2.66

for x in non_matched_G1:
    score_list = []
    degree_of_V = len(list(nx.neighbors(G1, x)))
    for y in non_matched_G2:
        count_1 = 0
        count_2 = 0
        matched_index_1 = []
        matched_index_2 = []
        degree_of_U = len(list(nx.neighbors(G2, y)))
        neighbors_1 = list(nx.neighbors(G1, x))
        neighbors_2 = list(nx.neighbors(G2, y))
        for nodeV in neighbors_1:
            count_1 = 0
            for a in seed_pair_G1:
                if nodeV == a:
                    matched_index_1.append(count_1)
                    break
                count_1 = count_1 + 1
        for nodeU in neighbors_2:
            count_1 = 0
            for b in seed_pair_G2:
                if nodeU == b:
                    matched_index_2.append(count_1)
                    break
                count_1 = count_1 + 1
        for node1 in matched_index_1:
            for node2 in matched_index_2:
                if node1 == node2:
                    count_2 = count_2 + 1
        scores = (count_2) / (math.sqrt(degree_of_V) * math.sqrt(degree_of_U))
        score_list.append(scores)
    standard_deviation = statistics.pstdev(score_list)
    if standard_deviation != 0.0:
        temp_max = max(score_list)
        test = zip(score_list, non_matched_G2)
        test = list(test)
        for z in test:
            temp_pos = z[0]
            if temp_max == temp_pos:
                node_pos = z[1]
                break
        max1 = max(score_list)
        score_list.remove(max1)
        max2 = max(score_list)
        eccentricity = (max1 - max2) / (standard_deviation)
        if eccentricity > threshold:
            seed_pair_G1.append(x)
            seed_pair_G2.append(node_pos)
            non_matched_G2.remove(node_pos)

seed_matching_pairs = list(zip(seed_pair_G1, seed_pair_G2))

print("Seed Matching Pairs:", seed_matching_pairs)

with open(r"outputfile.txt", "w") as txt_file:
    for line in seed_matching_pairs:
        txt_file.write(" ".join([str(n) for n in line]) + "\n")