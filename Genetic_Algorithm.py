import random
from Graph_Generator import load_data
from Utility import create_individual
from Utility import fitness
from Utility import mutate
from Utility import crossover
from Utility import tournament_selection
from Utility import initialize
from Utility import generate_random_tasks
from Executor import execute_single_state
from Utility import seeded_initialize
import numpy


def plain_ga(tasks, graph, skill_set, iteration=1000, pop_size=100):
    P = initialize(tasks, skill_set, pop_size)
    #P = seeded_initialize(tasks,graph,skill_set,pop_size)
    best_individual = None

    for i in range(iteration):
        for p in P:
            if best_individual is None or fitness(graph,p) < fitness(graph, best_individual):
                best_individual = p

        Q = []
        for j in range(pop_size//2):
            individual1 = tournament_selection(graph,P, tournament_size=7)
            individual2 = tournament_selection(graph,P, tournament_size=7)
            child1, child2 = crossover(skill_set, individual1, individual2)
            child1 = mutate(graph,skill_set,child1)
            child2 = mutate(graph,skill_set,child2)
            Q.append(child1)
            Q.append(child2)

        P = Q

    '''
    print("Best Individual:")
    print("Tasks: ", best_individual["tasks"])
    print("Team: ", best_individual["team"])
    print("Fitness: ", fitness(graph, best_individual))
    '''

    return best_individual


def elitist_ga(tasks, graph, skill_set, iteration=1000, pop_size=100, elites_size=20):
    P = initialize(tasks, skill_set, pop_size)
    #P = seeded_initialize(tasks,graph,skill_set,pop_size)
    best_individual = None

    for i in range(iteration):
        all_fitness = []
        for p in P:
            fp = fitness(graph,p)
            all_fitness.append(fp)
            if best_individual is None or fp < fitness(graph, best_individual) :
                best_individual = p

        elites = numpy.array(all_fitness)
        elites_index = numpy.argsort(elites)
        elites_index = elites_index[:elites_size]
        Q = []

        for j in range(elites_size):
            Q.append(P[elites_index[j]])

        for j in range((pop_size-elites_size)//2):
            individual1 = tournament_selection(graph,P, tournament_size=7)
            individual2 = tournament_selection(graph,P, tournament_size=7)
            child1, child2 = crossover(skill_set, individual1, individual2)
            child1 = mutate(graph,skill_set,child1)
            child2 = mutate(graph,skill_set,child2)
            Q.append(child1)
            Q.append(child2)

        P = Q

    '''
    print("Best Individual:")
    print("Tasks: ", best_individual["tasks"])
    print("Team: ", best_individual["team"])
    print("Fitness: ", fitness(graph, best_individual))
    '''

    return best_individual


if __name__ == "__main__":
    dataset = "DBLP"
    random.seed(5)
    social_graph, skill_map = load_data(dataset)
    print()
    print("Running Plain GA...")
    print()
    execute_single_state(social_graph, skill_map, plain_ga)
    print()
    print("Running Eitist GA...")
    print()
    execute_single_state(social_graph, skill_map, elitist_ga)