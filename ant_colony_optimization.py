import random

def ant_colony_optimization(graph, num_ants, num_iterations, alpha, beta, evaporation_rate, initial_pheromone):
    """
    Solves the traveling salesman problem using ant colony optimization.
    :param graph: adjacency matrix of the graph
    :param num_ants: number of ants to use
    :param num_iterations: number of iterations to run
    :param alpha: parameter controlling the importance of pheromone levels
    :param beta: parameter controlling the importance of distance
    :param evaporation_rate: rate at which pheromone evaporates
    :param initial_pheromone: initial pheromone level on each edge
    :return: shortest path found by the algorithm and its length
    """
    num_cities = len(graph)
    
    # initialize pheromone levels on all edges
    # May initial pheromone yung each edge
    # Gagawa ng matrix for the pheromone instead of distance
    pheromone = [[initial_pheromone] * num_cities for _ in range(num_cities)]
    print(pheromone)
    
    # initialize the best path found so far and its length
    best_path = None
    best_path_length = float('inf')
    
    # run the algorithm for the specified number of iterations
    for iteration in range(num_iterations):
        
        # initialize the paths taken by each ant and their distances
        paths = [[] for _ in range(num_ants)]
        path_distances = [0] * num_ants

        # have each ant build a path through the graph
        for ant in range(num_ants):
            current_city = random.randint(0, num_cities-1)
            paths[ant].append(current_city)
            # move to the next city until all cities have been visited
            while len(paths[ant]) < num_cities:
                # choose the next city based on pheromone levels and distance
                next_city = choose_next_city(graph, pheromone, paths[ant], current_city, alpha, beta)
                paths[ant].append(next_city)
                path_distances[ant] += graph[current_city][next_city]
                current_city = next_city
            # add the distance between the last and first cities to complete the path
            path_distances[ant] += graph[current_city][paths[ant][0]]
            # update the best path found so far if this ant's path is shorter
            if path_distances[ant] < best_path_length:
                best_path = paths[ant]
                best_path_length = path_distances[ant]
        # update pheromone levels based on the paths taken by the ants
        update_pheromone(pheromone, paths, path_distances, evaporation_rate)
    return best_path, best_path_length

def choose_next_city(graph, pheromone, path, current_city, alpha, beta):
    """
    Chooses the next city for an ant to visit based on the pheromone levels and distance to each neighboring city.
    :param graph: adjacency matrix of the graph
    :param pheromone: pheromone matrix
    :param path: list of cities visited so far
    :param current_city: index of the current city
    :param alpha: parameter controlling the importance of pheromone levels
    :param beta: parameter controlling the importance of distance
    :return: index of the next city to visit
    """
    # calculate the distances to each neighboring city and the pheromone levels on the edges connecting them
    # Ilagay sa list yung mga distances based sa current city yung lahat ng cities na di pa napupuntahan
    distances = [graph[current_city][neighbor] for neighbor in range(len(graph)) if neighbor not in path]
    # Ilagay sa list yung mga pheromone level ng mga edges na di pa napupuntahan
    pheromone_levels = [pheromone[current_city][neighbor] for neighbor in range(len(graph)) if neighbor not in path]
    
    # calculate the probability of moving to each neighboring city
    # TODO: Alamin kung bakit ito yung naging formula
    # Gawa ng list ng probabilities based sa mga di pa nadadaanang cities
    probabilities = [((pheromone_levels[i] ** alpha) * ((1.0 / distances[i]) ** beta)) for i in range(len(distances))]
    total_probability = sum(probabilities)
    
    # choose the next city randomly based on the probabilities
    # Gawa ng list ng probabilities this time true probability na sya since dinivide sa sum ng lahat
    probabilities = [probability / total_probability for probability in probabilities]
    # Yung random.choices(x, y) yung first param x is for the choices. yung next param y ay para doon sa probability na mapili sya
    next_city = random.choices([neighbor for neighbor in range(len(graph)) if neighbor not in path], probabilities)[0]
    return next_city


def update_pheromone(pheromone, paths, path_distances, evaporation_rate):
    """
    Updates the pheromone levels on the edges based on the paths taken by the ants.
    :param pheromone: pheromone matrix
    :param paths: list of paths taken by each ant
    :param path_distances: list of distances for each ant's path
    :param evaporation_rate: rate at which pheromone evaporates
    """
    num_cities = len(pheromone)
    # evaporate pheromone on all edges
    for i in range(num_cities):
        for j in range(num_cities):
            # Decrease the pheromone level of each edges by the evaporation rate.
            pheromone[i][j] *= (1 - evaporation_rate)
    
    # update pheromone levels on edges used by the ants
    # TODO: Mas intindihin pa to.
    for ant in range(len(paths)):
        for i in range(len(paths[ant])):
            j = (i + 1) % num_cities
            # Dagdagan ng 1/distance yung pheromone level kapag nadaanan sya ng ant
            pheromone[paths[ant][i]][paths[ant][j]] += (1.0 / path_distances[ant])

graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# TODO: Verify the formula for the ACO especially the alpha and beta

best_path, best_path_length = ant_colony_optimization(graph, num_ants=10, num_iterations=100, alpha=1, beta=5, evaporation_rate=0.5, initial_pheromone=1)
print('Shortest path:', best_path)
print('Path length:', best_path_length)