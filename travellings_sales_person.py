import random


POPULATION_SIZE = 100
MUTATION_RATE = 0.01
ELITE_SIZE = 2
GENERATIONS = 100

path_length = 0

def fitness_function(path):
    path = list(path)
    sum = 0
    for i in range(path_length):
        if(i != path_length-1):
            sum += graph[str(path[i])][str(path[i+1])]
        else:
            sum += graph[str(path[i])][str(path[0])]

    return sum


def create_initial_population(num_nodes):
    pop = []
    for i in range(POPULATION_SIZE):
        path = []
        while len(path) != 4:
            x = random.randint(1, num_nodes)
            if x not in path:
                path.append(x)
        pop.append(path)

    return pop

def evaluate_population(list_pop):
    fitness_scores = []
    for path in list_pop:
        fitness_scores.append(fitness_function(path))
    return fitness_scores

def select_parents(list_pop):
    parents = []
    while(len(parents) != 2):
        x = random.randint(1, POPULATION_SIZE)
        if(x not in parents):
            parents.append(list_pop[x-1])
    return parents

def cycle_crossover(parents):
    child1 = parents[0]
    child2 = parents[1]

    index = random.randint(1, len(parents[0])) - 1
    preserve_index = index
    n_index = -1

    while preserve_index != n_index:
        temp = child1[index]

        try:
            n_index = child2.index(temp)
        except:
            child1[index] = child2[index]
            child2[index] = temp
            break

        child1[index] = child2[index]
        child2[index] = temp

        index = n_index
    
    return child1, child2


def mutate(list_pop):
    rand_index = random.randint(0, len(list_pop)-1)

    mutated_path = list_pop[rand_index]

    index_node1, index_node2 = -1, -1

    while(index_node1 == index_node2):
        index_node1 = random.randint(1, path_length-1)
        index_node2 = random.randint(1, path_length-1)

    if random.random() < MUTATION_RATE:
        temp = mutated_path[index_node1]
        mutated_path[index_node1] = mutated_path[index_node2]
        mutated_path[index_node2] = temp

    return(mutated_path)



graph = {'1': {'4':20, '2':10, '3':15}, '2': {'1':10, '4':25, '3':35}, 
         '3': {'1':15, '2':35, '4':30}, '4':{'1':20, '2':25, '3':30}}


path_length = len(graph)

population = create_initial_population(path_length)


for i in range(GENERATIONS):
    fitness_scores = evaluate_population(population)

    best_answer_set = min(population, key=lambda answer_set: fitness_function(x for x in answer_set))
    best_x = [x for x in best_answer_set]
    best_fitness = fitness_function(best_x)
    print("Generation {}: Best solution found: nodes = {}, travel cost = {}".format(i+1, best_x, best_fitness))

    elite_population = []
    
    elite_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])[:ELITE_SIZE]

    for index in elite_indices:
        elite_population.append(population[index])

    
    next_population = elite_population.copy()
    while len(next_population) < POPULATION_SIZE:
        parents = select_parents(population)

        child1, child2 = cycle_crossover(parents)

        next_population.append(child1)
        if len(next_population) < POPULATION_SIZE:
            next_population.append(child2)
        
    mutate(next_population)

    # Replace the current population with the next generation
    population = next_population
