import numpy as np
from collections import defaultdict
import random

file_name = 'socialNet.sn'
data = np.genfromtxt(file_name, dtype=str)
network = defaultdict(list) #represents as child: [parent1, parent2, ...]
omegas = []
all_edges = []
for row in data:
    network[row[1]].append(row[0])
    if row[0]=='omega':
        omegas.append(row[1])
        continue
    all_edges.append(row)

parent_network = defaultdict(list) #represents as parent: [child1, child2, ...]
for row in data:
    parent_network[row[0]].append([row[1], random.uniform(0,1)])
    if row[0]=='omega':
        break
#for [t,d] in parent_network['mycentraljersey.com']:
#    print(t)
def check_omega_parents(node):
    yesomegas = []
    for i in network[node]:
        if i in omegas:
            yesomegas.append(i)
    return yesomegas

fname = 'Episodes.out'
with open(fname) as f:
    lines = f.readlines()
    #print(lines[1].split()[1])

place_holder = lines[0]
count = 0
all_eps = []
for l in lines:
    if count == 0:
        episode = []
        count = count + 1
        continue
    if l == place_holder:
        all_eps.append(episode)
        episode = []
    else:
        episode.append(l.split()[1])

final_count = 0
print(len(all_edges))
for [curr_v, curr_w] in all_edges:
    print('Progress: ' + str(float(final_count/len(all_edges))*100) + '%')
    final_count += 1
    if curr_v not in omegas:
        continue
    else:
        s_neg = 0
        s_pos = 0
        p_w = []
        count = 0
        for e in all_eps:
            if curr_w not in e:
                s_neg = s_neg + 1
            else:
                s_pos = s_pos + 1
                active_parents = check_omega_parents(curr_w)
                if len(active_parents) == 0:
                    p_w.append(1)
                    continue
                k_vw_list = []
                for p in active_parents:
                    for [child,prob] in parent_network[p]:
                        if child == curr_w:
                            k_vw_list.append(prob)
                    prod_anti_probs = float(1)
                for prob in k_vw_list:
                    prod_anti_probs = prod_anti_probs * (1-prob)
                p_w.append(1 - prod_anti_probs)
        
        #print('Hi ')
        #print(curr_v)
        #print(parent_network[curr_v][1])
        for i in range(len(parent_network[curr_v])):
            if parent_network[curr_v][i][0] == curr_w:
                curr_k_vw = parent_network[curr_v][i][1]
                summation = 0
                for p in p_w:
                    summation += curr_k_vw/p
                new_k_vw = 1/(s_pos+s_neg) * summation
                parent_network[curr_v][i][1] = new_k_vw
