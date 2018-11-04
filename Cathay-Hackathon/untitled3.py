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
    for i in max_matching:
        ret[passenger[i]['Name']] = passenger[max_matching[i]]['Name']
    return ret

