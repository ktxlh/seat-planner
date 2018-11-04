import networkx as nx
import random
import numpy as np

num_of_passengers = 50
features = {'Window': [-1, 1], 'Sleep': [-2, 2], 'Networking': [-2, 2], 'Window Shading': [-2, 2]}
weights = {'Window': 1, 'Sleep': 1, 'Networking': 1, 'Window Shading': 1}
inf = 10000
# Window: Window = 1, Indifferent = 0, Aisle = -1
# Sleep: Very Much = 2 <-----> Very Less = -2
# Networking: Very Willing = 2 <-----> Very Unwilling = -2
# Window Shading: Open = 2 <-----> Close = -2

'''Do you want so sit with someone with similar / different background and personality?
Similar= 1, Indifferent = 0, Different = -1'''

# Add a random passenger into the list
def add_random_passenger(passenger):
    dic = {}
    for feature in features:
        mini = features[feature][0]
        maxi = features[feature][1]
        dic[feature] = random.randint(mini, maxi)
    passenger.append(dic)

def get_cost(i, j):
    cost = 0
    for feature in features:
        if feature is 'Window':
            cost += weights[feature] * (i[feature] + j[feature]) ** 2
        else:
            cost += weights[feature] * (i[feature] - j[feature]) ** 2
    return cost

#-----------------------------------------------------------------------------#

# Maximal Matching
passenger = []
for i in range(num_of_passengers):
    add_random_passenger(passenger)

G = nx.Graph()

for i in range(num_of_passengers):
    G.add_node(i)

# Reward = inf - Cost
for i in range(num_of_passengers):
    for j in range(i + 1, num_of_passengers):
        G.add_edge(i, j, weight = inf - get_cost(passenger[i], passenger[j]))

max_matching = nx.max_weight_matching(G)

for i in max_matching:
    print(i, max_matching[i], inf - G[i][max_matching[i]]['weight'])
    
#-----------------------------------------------------------------------------#

# Optimal Weight Training
feedback = [random.randint(0, 5) for i in range(num_of_passengers)]

dataset = []

for i in range(num_of_passengers):
    if i < max_matching[i]:
        arr = []
        for feature in features:
            if feature == 'Window':
                arr.append((passenger[i][feature] + passenger[max_matching[i]][feature]) ** 2)
            else:
                arr.append((passenger[i][feature] - passenger[max_matching[i]][feature]) ** 2)
        arr.append(5 - (feedback[i] + feedback[max_matching[i]]) / 2)
        dataset.append(arr)
dataset = np.array(dataset)

X_train = dataset[:, :4]
y_train = dataset[:, 4]

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

ind = 0
for feature in features:
    weights[feature] = regressor.coef_[ind]
    ind += 1

y_pred = []
for i in range(num_of_passengers):
    y_pred.append(get_cost(passenger[i], passenger[max_matching[i]]))

temp = []
for i in range(num_of_passengers):
    temp.append(5-feedback[i])