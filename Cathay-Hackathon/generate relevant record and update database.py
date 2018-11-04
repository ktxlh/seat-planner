import random
import numpy as np

features = {'Window': [-1, 1], 'Sleep': [-2, 2], 'Networking': [-2, 2], 'WindowShading': [-2, 2]}

def add_random_passenger(passenger):
    dic = {'Preferences': {}, 'Weights': {}}
    for feature in features:
        dic['Name'] = ('Passenger' + str(random.randint(0, 100000)))
        dic['Preferences'][feature] = random.randint(features[feature][0], features[feature][1])
        dic['Weights'][feature] = {1: random.uniform(0, 1), 2: random.uniform(0, 1)}
    passenger.append(dic)

num_of_passengers = 10
passenger = []
real_weights = []
for i in range(num_of_passengers):
    add_random_passenger(passenger)
    dic = {}
    for feature in features:
        dic[feature] = {1: random.uniform(0, 1), 2: random.uniform(0, 1)}
    real_weights.append(dic)

flight_arrangement = {1: 2, 3: 8, 5: 4, 9: 6, 7: 0}

def generate_fake_record(flight_arrangement, passenger, real_weights):
    temp = {}
    for key in flight_arrangement:
        value = flight_arrangement[key]
        temp[value] = key
    for key in temp:
        flight_arrangement[key] = temp[key]
    
    expected_cost = []
    for i in flight_arrangement:
        cost = 0
        j = flight_arrangement[i]
        for feature in features:
            if feature == 'Window':
                cost += real_weights[i][feature][1] * (passenger[i]['Preferences'][feature] + passenger[j]['Preferences'][feature]) ** 2
                cost += real_weights[i][feature][2] * (passenger[i]['Preferences'][feature] + passenger[j]['Preferences'][feature]) ** 4
            else:
                cost += real_weights[i][feature][1] * (passenger[i]['Preferences'][feature] - passenger[j]['Preferences'][feature]) ** 2
                cost += real_weights[i][feature][2] * (passenger[i]['Preferences'][feature] - passenger[j]['Preferences'][feature]) ** 4
        expected_cost.append(cost)
    fake_feedback = []
    maxi = max(expected_cost)
    mini = min(expected_cost)
    for i in range(len(expected_cost)):
        expected_cost[i] = int(round(random.uniform(-2, 2) + 5 * (expected_cost[i] - mini) / (maxi - mini)))
        if expected_cost[i] < 0:
            expected_cost[i] = 0
        if expected_cost[i] > 5:
            expected_cost[i] = 5
        fake_feedback.append(5 - expected_cost[i])
    return fake_feedback



def database_update(flight_arrangement, passenger, real_weights):
    feedback = generate_fake_record(flight_arrangement, passenger, real_weights)
    ret = []
    
    temp = {}
    for key in flight_arrangement:
        value = flight_arrangement[key]
        temp[value] = key
    for key in temp:
        flight_arrangement[key] = temp[key]
    for i in range(len(feedback)):
        j = flight_arrangement[i]
        arr = []
        for feature in features:
            if feature == 'Window':
                arr.append((passenger[i]['Preferences'][feature] + passenger[j]['Preferences'][feature]) ** 2)
                arr.append((passenger[i]['Preferences'][feature] + passenger[j]['Preferences'][feature]) ** 4)
            else:
                arr.append((passenger[i]['Preferences'][feature] - passenger[j]['Preferences'][feature]) ** 2)
                arr.append((passenger[i]['Preferences'][feature] - passenger[j]['Preferences'][feature]) ** 4)
        arr.append(5 - feedback[i])
        ret.append({'Name': passenger[i]['Name'], 'Update': arr})
    return ret

database_update(flight_arrangement, passenger, real_weights)



