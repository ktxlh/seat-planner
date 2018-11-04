features = {'Window': [-1, 1], 'Sleep': [-2, 2], 'Networking': [-2, 2], 'WindowShading': [-2, 2]}
passenger_prototype = {'Name': 'Person', 'Preferences': {'Window': 1, 'Sleep': -1, 'Networking': 2, 'WindowShading': 2},
                       'Weights': {'Window': {1: 1, 2: 0}, 'Sleep': {1: 1, 2: 0},
                                   'Networking': {1: 1, 2: 0}, 'WindowShading': {1: 1, 2: 0}}}

def add_random_passenger(passenger):
    dic = {'Preferences': {}, 'Weights': {}}
    for feature in features:
        dic['Name'] = ('Passenger' + str(random.randint(0, 100000)))
        dic['Preferences'][feature] = random.randint(features[feature][0], features[feature][1])
        dic['Weights'][feature] = {1: random.uniform(0, 1), 2: random.uniform(0, 1)}
    passenger.append(dic)
