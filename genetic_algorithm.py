import math
import random

# DE JONG'S Function 1
# ------------------------------------------------------

# def fitness_function(x_values):
#     x = list(x_values)
#     return sum(x**2 for x in x_values)
#     # return 100*((x[0]**2)-(x[1]))**2 + (1-x[0])**2

# FIND_MAX = False
# NUM_VARIABLES = 3
# MIN_RANGE = -5.12
# MAX_RANGE = 5.12

# ------------------------------------------------------


# DE JONG'S Function 2
# ------------------------------------------------------

# def fitness_function(x_values):
#     x = list(x_values)
#     # return sum(x**2 for x in x_values)
#     return 100*((x[0]**2)-(x[1]))**2 + (1-x[0])**2

# FIND_MAX = False
# NUM_VARIABLES = 2
# MIN_RANGE = -2.048
# MAX_RANGE = 2.048

# ------------------------------------------------------


# DE JONG'S Function 3
# ------------------------------------------------------

# def fitness_function(x_values):
#     x = list(x_values)
#     # return sum(x**2 for x in x_values)
#     # return 100*((x[0]**2)-(x[1]))**2 + (1-x[0])**2
#     return sum(math.floor(x) for x in x_values)

# FIND_MAX = False
# NUM_VARIABLES = 5
# MIN_RANGE = -5.12
# MAX_RANGE = 5.12

# ------------------------------------------------------


# DE JONG'S Function 4
# ------------------------------------------------------

# def fitness_function(x_values):
#     x = list(x_values)
#     fitness_value = 0
    
#     for i in range(1, len(x)+1):
#         fitness_value += i*x[i-1] + random.gauss(0, math.sqrt(1))
        
#     return fitness_value

# FIND_MAX = True
# NUM_VARIABLES = 50
# MIN_RANGE = -1.28
# MAX_RANGE = 1.28

# ------------------------------------------------------


# DE JONG'S Function 5
# ------------------------------------------------------

def fitness_function(x_values):
    x = list(x_values)
    
    a = [[-32, -16, 0, 16, 32, -32, -16, 0, 16, 32],
         [-32, -32, -32, -32, -32, -16, -16, -16, 32, 32, 32]]
    
    fitness_value = 0
    
    for j in range(1, 26):
        fitness_value += 1/[j+((x[0]-a[1][j])**6)+((x[1]-a[1][j])**6)]
        
    return (0.002 + fitness_value)

FIND_MAX = False
NUM_VARIABLES = 2
MIN_RANGE = -65.536
MAX_RANGE = 65.536

# ------------------------------------------------------

POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 64
MUTATION_RATE = 0.1
ELITE_SIZE = 2
GENERATIONS = 300




def create_initial_population():
    population = []
    for i in range(POPULATION_SIZE):
        answer_set = []
        for j in range(NUM_VARIABLES):
            chromosome = ""
            for k in range(CHROMOSOME_LENGTH):
                chromosome += str(random.randint(0, 1))
            answer_set.append(chromosome)
        population.append(answer_set)
        
    # print("initial population: " + str(population))
    return population

def decode_chromosome(chromosome):
    decoded_number = int(chromosome, 2)
    # print("decoded_number: " + str(decoded_number))
    number_of_data_sets = 2**CHROMOSOME_LENGTH
    ratio = (MAX_RANGE-MIN_RANGE)/number_of_data_sets
    # print("ratio " + str(ratio))


    adjusted_number = MIN_RANGE + (ratio*decoded_number)
    # print("adjusted_number " + str(adjusted_number))

    return adjusted_number

def evaluate_population(population):
    fitness_scores = []
    for set_answer in population:
        arr_answers = []
        for chromosome in set_answer:
            x = decode_chromosome(chromosome)
            arr_answers.append(x)
        fitness_scores.append(fitness_function(arr_answers))
    return fitness_scores

def select_parents(population, fitness_scores):
    parents = []
    total_fitness = sum(fitness_scores)
    for i in range(2):
        pick = random.uniform(0, total_fitness)
        current = 0
        for j in range(POPULATION_SIZE):
            current += fitness_scores[j]
            if current > pick:
                parents.append(population[j])
                break
    # print("parents: " + str(parents))
    return parents

# TODO: Ayusin to boi ha!
def crossover(parents):
    child1 = []
    child2 = []
    crossover_point = random.randint(0, CHROMOSOME_LENGTH - 1)
    
    for i in range(0, NUM_VARIABLES):
        child1.append((parents[0][i])[:crossover_point] + (parents[1][i])[crossover_point:])
        child2.append((parents[1][i])[:crossover_point] + (parents[0][i])[crossover_point:])

    # print("child1: " + str(child1) + " ---- child2: " + str(child2))
    return child1, child2


def mutate(answer_set):
    mutated_answers = []
    for chromosome in answer_set:
        mutated_chromosome = ""
        for bit in chromosome:
            if random.random() < MUTATION_RATE:
                mutated_chromosome += '0' if bit == '1' else '1'
            else:
                mutated_chromosome += bit
        mutated_answers.append(mutated_chromosome)
    # print(mutated_answers)
    return mutated_answers

# Create the initial population
population = create_initial_population()

# Run the genetic algorithm for a fixed number of generations
for i in range(GENERATIONS):
    # Evaluate the fitness of the population
    fitness_scores = evaluate_population(population)

    print("---------------------------------------------")
    # Print the best solution found so far
    if FIND_MAX:
        best_answer_set = max(population, key=lambda answer_set: fitness_function(decode_chromosome(x) for x in answer_set))
    else:
        best_answer_set = min(population, key=lambda answer_set: fitness_function(decode_chromosome(x) for x in answer_set))
    best_x = [decode_chromosome(x) for x in best_answer_set]
    best_fitness = fitness_function(best_x)
    print("Generation {}: Best solution found: x = {}, f(x) = {}".format(i+1, best_x, best_fitness))

    # Select the elite chromosomes
    elite_population = []
    if FIND_MAX:
        elite_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k], reverse=True)[:ELITE_SIZE]
    else:
        elite_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])[:ELITE_SIZE]
    for index in elite_indices:
        elite_population.append(population[index])

    # Generate the next generation of chromosomes
    next_population = elite_population.copy()
    while len(next_population) < POPULATION_SIZE:
        parents = select_parents(population, fitness_scores)
        while len(parents) < 2:
            parents = select_parents(population, fitness_scores)
        child1, child2 = crossover(parents)
        child1 = mutate(child1)
        child2 = mutate(child2)
        next_population.append(child1)
        if len(next_population) < POPULATION_SIZE:
            next_population.append(child2)

    # Replace the current population with the next generation
    population = next_population


