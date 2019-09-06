import random
from Graph_Generator import load_data
from Utility import create_individual
from Utility import fitness
from Utility import generate_random_tasks
from Executor import execute_single_state


def random_search(tasks, graph, skill_set, iteration=1000):
    individual = create_individual(tasks, skill_set)
    best_individual = individual

    for i in range(iteration):
        individual = create_individual(tasks, skill_set)
        #print("Iteration:", (i+1), fitness(graph, individual))
        if fitness(graph, individual) < fitness(graph, best_individual):
            best_individual = individual

    print("Best Individual:")
    print("Tasks: ", best_individual["tasks"])
    print("Team: ", best_individual["team"])
    print("Fitness: ",fitness(graph, best_individual))

    return best_individual


if __name__ == "__main__":
    random.seed(5)
    social_graph, skill_map = load_data()
    execute_single_state(social_graph,skill_map,random_search)