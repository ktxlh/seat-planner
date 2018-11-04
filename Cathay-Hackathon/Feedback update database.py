# Flight Arrangement + feedback ==> update personal database

import random

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
for i in range(num_of_passengers):
    add_random_passenger(passenger)

flight_arrangement = {1: 2, 3: 8, 5: 4, 9: 6, 7: 0}
feedback = [random.randint(0, 5) for i in range(num_of_passengers)]

Update_prototype = {'Name': 'Passenger', 'Update': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

def database_update(flight_arrangement, feedback, passenger):
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

# upd = database_update(flight_arrangement, feedback, passenger)
#　upd