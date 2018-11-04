import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

num_of_passengers = 200

passengers = []
real_weights = {}
datasets = []
passengers_dict = {}

features = {'Window': [-1, 1], 'Sleep': [-2, 2], 'Networking': [-2, 2], 'WindowShading': [-2, 2]}

def pass_to_num(st):
    res = ''
    for c in st:
        if c.isdigit():
            res = res + c
    return int(res)

def add_random_passenger(passenger, i):
    dic = {'Preferences': {}, 'Weights': {}}
    for feature in features:
        dic['Name'] = ('Passenger' + str(i))
        dic['Preferences'][feature] = random.randint(features[feature][0], features[feature][1])
        dic['Weights'][feature] = {1: random.uniform(0, 1), 2: random.uniform(0, 1)}
    passenger.append(dic)
    
for i in range(num_of_passengers):
    add_random_passenger(passengers, i)
    dic = {}
    for feature in features:
        dic[feature] = {1: random.uniform(0, 1), 2: random.uniform(0, 0.1)}
    real_weights[('Passenger' + str(i))] = dic
    datasets.append([])

for i in range(num_of_passengers):
    passengers_dict[passengers[i]['Name']] = {'Preferences': passengers[i]['Preferences'],
                                               'Weights': passengers[i]['Weights']}

def generate_relevant_record(flight_arrangement, passenger, real_weights):
    # temp = {}
    # for key in flight_arrangement:
    #     value = flight_arrangement[key]
    #     temp[value] = key
    # for key in temp:
    #     flight_arrangement[key] = temp[key]
    
    expected_cost = []
    for i in flight_arrangement:
        cost = 0
        j = flight_arrangement[i]
        for feature in features:
            if feature == 'Window':
                cost += real_weights[i][feature][1] * (passengers_dict[i]['Preferences'][feature] + passengers_dict[j]['Preferences'][feature]) ** 2
                cost += real_weights[i][feature][2] * (passengers_dict[i]['Preferences'][feature] + passengers_dict[j]['Preferences'][feature]) ** 4
            else:
                cost += real_weights[i][feature][1] * (passengers_dict[i]['Preferences'][feature] - passengers_dict[j]['Preferences'][feature]) ** 2
                cost += real_weights[i][feature][2] * (passengers_dict[i]['Preferences'][feature] - passengers_dict[j]['Preferences'][feature]) ** 4
        expected_cost.append(cost)
    fake_feedback = []
    maxi = max(expected_cost)
    mini = min(expected_cost)
    for i in range(len(expected_cost)):
        expected_cost[i] = int(round(random.uniform(-3, 3) + 5 * (expected_cost[i] - mini) / (maxi - mini)))
        if expected_cost[i] < 0:
            expected_cost[i] = 0
        if expected_cost[i] > 5:
            expected_cost[i] = 5
        fake_feedback.append(5 - expected_cost[i])
    return fake_feedback



def database_update(flight_arrangement, passenger, real_weights):
    feedback = generate_relevant_record(flight_arrangement, passenger, real_weights)
    ret = []
    
    # temp = {}
    # for key in flight_arrangement:
    #     value = flight_arrangement[key]
    #     temp[value] = key
    # for key in temp:
    #     flight_arrangement[key] = temp[key]
    
    for ind in range(len(feedback)):
        i = passenger[ind]['Name']
        j = flight_arrangement[i]
        arr = []
        for feature in features:
            if feature == 'Window':
                arr.append((passengers_dict[i]['Preferences'][feature] + passengers_dict[j]['Preferences'][feature]) ** 2)
                arr.append((passengers_dict[i]['Preferences'][feature] + passengers_dict[j]['Preferences'][feature]) ** 4)
            else:
                arr.append((passengers_dict[i]['Preferences'][feature] - passengers_dict[j]['Preferences'][feature]) ** 2)
                arr.append((passengers_dict[i]['Preferences'][feature] - passengers_dict[j]['Preferences'][feature]) ** 4)
        arr.append(5 - feedback[ind])
        ret.append({'Name': i, 'Update': arr})
    return ret

def get_cost(i, j):
    cost = 0
    for feature in features:
        if feature == 'Window':
            cost += i['Weights'][feature][1] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 2
            cost += j['Weights'][feature][1] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 2
            cost += i['Weights'][feature][2] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 4
            cost += j['Weights'][feature][2] * (i['Preferences'][feature] + j['Preferences'][feature]) ** 4
        else:
            cost += i['Weights'][feature][1] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 2
            cost += j['Weights'][feature][1] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 2
            cost += i['Weights'][feature][2] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 4
            cost += j['Weights'][feature][2] * (i['Preferences'][feature] - j['Preferences'][feature]) ** 4
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
    if len(passenger) == 20: 
        pos = nx.circular_layout(G)
        colors = range(G.number_of_edges())
        nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors,
        width=4, edge_cmap=plt.cm.Blues, with_labels=False)
        plt.show()
    return max_matching


num_of_flights = 100
people_on_flight = 50
array = []
for i in range(num_of_passengers):
    array.append(i)

for ite in range(num_of_flights):
    if ite % 10 == 0:
        print('ite = ', ite)
    random.shuffle(array)
    this_passenger = []
    for i in range(people_on_flight):
        this_passenger.append(passengers[array[i]])
    max_matching = get_best_matching(this_passenger)
    flight_arrangement = {}
    for i in max_matching:
        flight_arrangement[this_passenger[i]['Name']] = this_passenger[max_matching[i]]['Name']
    upd_list = database_update(flight_arrangement, this_passenger, real_weights)
    for i in range(len(upd_list)):
        datasets[pass_to_num(upd_list[i]['Name'])].append(upd_list[i]['Update'])
        

from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression

def linear_regression(dataset):
    dataset = np.array(dataset)
    X_train = dataset[:, :8]
    y_train = dataset[:, 8]
    # regressor = Lasso(alpha=0.0001,precompute=True,max_iter=1000,
    #        positive=True, random_state=9999, selection='random')
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    weights = []
    for i in range(8):
        weights.append(max(0, regressor.coef_[i]))
    return weights

# For first 50 people
this_passenger = []
for i in range(20):
    this_passenger.append(passengers[i])
mm = get_best_matching(this_passenger)
Cost_before_training = 0
for i in mm:
    if i < mm[i]:
        Cost_before_training += get_cost(passengers[i], passengers[mm[i]])



learned_weights = {}
for i in range(num_of_passengers):
    weights = linear_regression(datasets[i])
    dic = {'Window': {1: weights[0], 2: weights[1]},
           'Sleep': {1: weights[2], 2: weights[3]},
           'Networking': {1: weights[4], 2: weights[5]},
           'WindowShading': {1: weights[6], 2: weights[7]},}
    learned_weights[('Passenger' + str(i))] = dic

for i in range(20):
    passengers[i]['Weights'] = learned_weights[passengers[i]['Name']]
mm = get_best_matching(this_passenger)
Cost_after_training = 0
for i in mm:
    if i < mm[i]:
        Cost_after_training += get_cost(passengers[i], passengers[mm[i]])
        
print('total cost before training = ', Cost_before_training)
print('total cost after training = ', Cost_after_training)

    

