import networkx as nx
import random
import numpy as np

features = {'Window': [-1, 1], 'Sleep': [-2, 2], 'Networking': [-2, 2], 'WindowShading': [-2, 2]}

def get_cost(i, j):
    cost = 0
    for feature in features:
        if feature == 'Window':
            cost += i['Weights'][feature]['1'] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 2
            cost += j['Weights'][feature]['1'] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 2
            cost += i['Weights'][feature]['2'] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 4
            cost += j['Weights'][feature]['2'] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 4
        else:
            cost += i['Weights'][feature]['1'] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 2
            cost += j['Weights'][feature]['1'] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 2
            cost += i['Weights'][feature]['2'] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 4
            cost += j['Weights'][feature]['2'] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 4
    return cost

def get_best_matching(passenger):
    inf = 10000
    G = nx.Graph()
    for i in range(len(passenger)):
        G.add_node(i)
    for i in range(len(passenger)):
        for j in range(i + 1, len(passenger)):
            G.add_edge(i, j, weight = inf - get_cost(passenger[i], passenger[j]))
    max_matching = nx.max_weight_matching(G)
    ret = {}
    for key, value in max_matching:
        ret[passenger[key]['Name']] = passenger[value]['Name']
    return max_matching

def get_seat_plan(passenger):
    max_matching = get_best_matching(passenger)

    partners = []
    for key, value in max_matching:
        partners.append([key, value])
    seating_plan = []
    rows = len(passenger) // 2
    for i in range(rows):
        seating_plan.append([np.nan for j in range(2)])
    
    rowind = 0
    for pair in partners:
        i = pair[0]
        j = pair[1]
        passenger[i]
        if passenger[i]['Preferences']['Window'] == -1:
            seating_plan[rowind][1] = i
            seating_plan[rowind][0] = j
        elif passenger[j]['Preferences']['Window'] == -1:
            seating_plan[rowind][1] = j
            seating_plan[rowind][0] = i
        elif passenger[i]['Preferences']['Window'] == 1:
            seating_plan[rowind][1] = j
            seating_plan[rowind][0] = i
        else:
            seating_plan[rowind][1] = i
            seating_plan[rowind][0] = j
        rowind += 1
    ret = {}
    for i in range(len(seating_plan)):
        ret['Row' + str(i)] = { 'Aisle': passenger[int(seating_plan[i][0])]['Name'], 
                                'Window': passenger[int(seating_plan[i][1])]['Name']}
    return ret
    

