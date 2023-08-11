import numpy as np
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

start_time = time.process_time()
history = []

dataset1 = pd.read_csv("TSP_Instance2.csv")
dataset = dataset1.to_numpy()
dummy_data = dataset

gbest_distance = 100000000
k = 2
iteration = 100000

############# defining solution generation function
def generate_solution(position, n, solution):
    node = n
    i = position
    distance = dataset[node]
    if (i + 2) == len(solution):
        solution[i + 1] = solution[0]
    else:
        for j in range(len(distance)):
            value = (np.argsort(distance)[j]) + 1
            if value not in solution:
                solution[i + 1] = value
                break
    return solution

######################## defining calculate distance function
def calculate_distance(input_solution):
    distance = 0
    soution = input_solution
    for i in range(len(input_solution)-1):
        distance = distance + dataset[(soution[i]-1), (soution[i+1]-1)]
    return distance


################################ defining K-opt funtion
def k_opt(i, solution):
    pos  = i
    pos_pick = [pos, pos+1, pos+3, pos+4]
    node_pick = [0, 0, 0, 0]

    for j in range(len(pos_pick)):
        if pos_pick[j] > len(solution)-2:
            pos_pick[j] = pos_pick[j]-len(dataset)

        node_pick[j] = solution[pos_pick[j]]

    for j in range(len(pos_pick)):
        solution[pos_pick[j+1]], solution[pos_pick[j+2]] =  solution[pos_pick[j+2]], solution[pos_pick[j+1]]
        break
    solution[-1] = solution[0]
    return (solution)



# Generating intial random solution
gbest_solution = np.array(range(1, len(dataset)+1))
random.shuffle(gbest_solution)
gbest_solution = np.append(gbest_solution, gbest_solution[0])
gbest_distance = calculate_distance(gbest_solution)
print("Initial Solution", gbest_solution, "with distance", gbest_distance)
cbest_solution = gbest_solution
#calling k opt
for i in range(iteration):
    gbest_solution = np.array(range(1, len(dataset) + 1))
    random.shuffle(gbest_solution)
    gbest_solution = np.append(gbest_solution, gbest_solution[0])
    cbest_solution = gbest_solution
    print("Iteration", i)
    for pos in range(1,len(dataset)+1 ):
        # position = random.choice(np.array(range(1,len(dataset)+1)))
        position = pos
        solution = k_opt(position, cbest_solution)
        cbest_distance = calculate_distance(solution)
        cbest_solution = solution
        if cbest_distance < gbest_distance:
            gbest_distance = cbest_distance
            gbest_solution = solution
            history.append(gbest_distance)

obj = gbest_distance
end_time = time.process_time()
print("Final Solution (2-Opt local search) of given TSP instance = ", gbest_solution)
print("Total distance from 2-Opt local search", obj)
print("Total calculation time:", end_time - start_time,'seconds')
plt.figure(figsize=(10, 8))
plt.plot(history, linewidth = 4)
plt.show()