import random


def solve_airplane_landing(airplanes, num_ants, num_iterations, alpha, beta, rho, q0):
    num_airplanes = len(airplanes)
    pheromone = [[1] * num_airplanes for _ in range(num_airplanes)]
    separation_time = calculate_separation_time(airplanes)
    best_solution = []
    best_cost = float('inf')

    for iteration in range(num_iterations):
        solutions = []
        costs = []

        for ant in range(num_ants):
            solution = construct_solution(airplanes, pheromone, separation_time, alpha, beta, q0)
            cost = calculate_cost(solution, airplanes)
            solutions.append(solution)
            costs.append(cost)

            if cost < best_cost:
                best_solution = solution
                best_cost = cost

        pheromone = update_pheromone(pheromone, solutions, costs, rho)

    return best_solution, best_cost


def construct_solution(airplanes, pheromone, separation_time, alpha, beta, q0):
    num_airplanes = len(airplanes)
    solution = []
    unvisited = list(range(num_airplanes))

    start_airplane = random.choice(unvisited)
    solution.append(start_airplane)
    unvisited.remove(start_airplane)

    while unvisited:
        current_airplane = solution[-1]
        probabilities = calculate_probabilities(current_airplane, unvisited, pheromone, separation_time, alpha, beta, q0)
        next_airplane = choose_next_airplane(probabilities, unvisited)
        solution.append(next_airplane)
        unvisited.remove(next_airplane)

    return solution


def calculate_probabilities(current_airplane, unvisited, pheromone, separation_time, alpha, beta, q0):
    pheromone_sum = 0.0
    probabilities = []

    for airplane in unvisited:
        st = separation_time[current_airplane][airplane]
        visibility = 1 / (st + 1e-6)
        pheromone_value = pheromone[current_airplane][airplane] ** alpha
        heuristic = visibility ** beta
        probabilities.append(pheromone_value * heuristic)
        pheromone_sum += pheromone_value * heuristic

    probabilities = [p / pheromone_sum for p in probabilities]
    return probabilities


def choose_next_airplane(probabilities, unvisited):
    if random.random() < q0:
        max_probability = max(probabilities)
        max_index = probabilities.index(max_probability)
        next_airplane = unvisited[max_index]
    else:
        next_airplane = random.choices(unvisited, probabilities)[0]

    return next_airplane


def calculate_cost(solution, airplanes):
    total_cost = 0.0

    for i in range(len(solution)):
        current_airplane = solution[i]
        current_time = sum([airplanes[solution[j]]['S'][i] for j in range(i)])
        appearance_time = airplanes[current_airplane]['A']
        earliest_time = airplanes[current_airplane]['E']
        target_time = airplanes[current_airplane]['T']
        latest_time = airplanes[current_airplane]['L']
        penalty_before = airplanes[current_airplane]['G']
        penalty_after = airplanes[current_airplane]['H']

        if current_time < appearance_time:
            total_cost += (appearance_time - current_time) * penalty_before
        elif current_time > appearance_time:
            total_cost += (current_time - appearance_time) * penalty_after

        if current_time < earliest_time:
            total_cost += (earliest_time - current_time) * penalty_before
        elif current_time > latest_time:
            total_cost += (current_time - latest_time) * penalty_after

        current_time += airplanes[current_airplane]['S'][i]

    return total_cost


def update_pheromone(pheromone, solutions, costs, rho):
    num_airplanes = len(pheromone)
    updated_pheromone = [[0] * num_airplanes for _ in range(num_airplanes)]

    for solution, cost in zip(solutions, costs):
        for i in range(len(solution) - 1):
            current_airplane = solution[i]
            next_airplane = solution[i + 1]
            updated_pheromone[current_airplane][next_airplane] += 1 / cost

    for i in range(num_airplanes):
        for j in range(num_airplanes):
            pheromone[i][j] = (1 - rho) * pheromone[i][j] + rho * updated_pheromone[i][j]

    return pheromone


def calculate_separation_time(airplanes):
    num_airplanes = len(airplanes)
    separation_time = [[0] * num_airplanes for _ in range(num_airplanes)]

    for i in range(num_airplanes):
        for j in range(num_airplanes):
            if i != j:
                separation_time[i][j] = airplanes[i]['S'][j]

    return separation_time


# Example usage
if __name__ == '__main__':
    airplanes = [
        {'A': 0, 'E': 10, 'T': 20, 'L': 30, 'G': 2, 'H': 1, 'S': [5, 10, 15, 20]},
        {'A': 5, 'E': 15, 'T': 25, 'L': 35, 'G': 2, 'H': 1, 'S': [5, 10, 15, 20]},
        {'A': 10, 'E': 20, 'T': 30, 'L': 40, 'G': 2, 'H': 1, 'S': [5, 10, 15, 20]},
        {'A': 15, 'E': 25, 'T': 35, 'L': 45, 'G': 2, 'H': 1, 'S': [5, 10, 15, 20]},
    ]

    num_ants = 10
    num_iterations = 100
    alpha = 1
    beta = 2
    rho = 0.1
    q0 = 0.9

    best_solution, best_cost = solve_airplane_landing(airplanes, num_ants, num_iterations, alpha, beta, rho, q0)

    print('Best solution:', best_solution)
    print('Best cost:', best_cost)
