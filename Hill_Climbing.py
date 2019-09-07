import random
from Graph_Generator import load_data
from Utility import create_individual
from Utility import fitness
from Utility import mutate
from Utility import generate_random_tasks
from Utility import seeded_create_individual
from Executor import execute_single_state


def hill_climbing(tasks, graph, skill_set, iteration=1000):
    #best_individual = create_individual(tasks, skill_set)
    best_individual = seeded_create_individual(tasks, graph, skill_set)

    for i in range(iteration):
        new_individual = mutate(graph, skill_set, best_individual)
        #print("Iteration:", (i+1), fitness(graph, new_individual))
        if fitness(graph, new_individual) < fitness(graph, best_individual):
            best_individual = new_individual

    print("Best Individual:")
    print("Tasks: ", best_individual["tasks"])
    print("Team: ", best_individual["team"])
    print("Fitness: ", fitness(graph, best_individual))

    return best_individual


def steepest_ascent_hill_climbing(tasks, graph, skill_set, iteration=1000, extra_arg=100):
    #best_individual = create_individual(tasks, skill_set)
    best_individual = seeded_create_individual(tasks, graph, skill_set)

    for i in range(iteration):
        new_individual = mutate(graph, skill_set, best_individual)
        for j in range(1, extra_arg):
            w_individual = mutate(graph, skill_set, best_individual)
            if fitness(graph, w_individual) < fitness(graph, new_individual):
                new_individual = w_individual

        # print("Iteration:", (i+1), fitness(graph, new_individual))
        if fitness(graph, new_individual) < fitness(graph, best_individual):
            best_individual = new_individual

    print("Best Individual:")
    print("Tasks: ", best_individual["tasks"])
    print("Team: ", best_individual["team"])
    print("Fitness: ", fitness(graph, best_individual))

    return best_individual


def steepest_ascent_hill_climbing_with_replacement(tasks, graph, skill_set, iteration=10000, extra_arg=100):
    #individual = create_individual(tasks, skill_set)
    individual = seeded_create_individual(tasks, graph, skill_set)
    best_individual = individual

    for i in range(iteration):
        new_individual = mutate(graph, skill_set, individual)
        for j in range(1, extra_arg):
            w_individual = mutate(graph, skill_set, individual)
            if fitness(graph, w_individual) < fitness(graph, new_individual):
                new_individual = w_individual

        # print("Iteration:", (i+1), fitness(graph, new_individual))
        if fitness(graph, new_individual) < fitness(graph, best_individual):
            best_individual = new_individual

        individual = new_individual

    print("Best Individual:")
    print("Tasks: ", best_individual["tasks"])
    print("Team: ", best_individual["team"])
    print("Fitness: ", fitness(graph, best_individual))

    return best_individual


if __name__ == "__main__":
    dataset = "Stackoverflow"
    random.seed(5)
    social_graph, skill_map = load_data(dataset)
    execute_single_state(social_graph, skill_map, steepest_ascent_hill_climbing_with_replacement)
