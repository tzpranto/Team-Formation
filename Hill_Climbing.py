import random
from Graph_Generator import load_data
from Utility import create_individual
from Utility import fitness
from Utility import mutate


def hill_climbing(graph,skill_set,iteration=10000,n=6):
    best_individual = create_individual(skill_set, n)

    for i in range(iteration):
        new_individual = mutate(graph,skill_set,best_individual)
        print(fitness(graph,new_individual))
        if fitness(graph,new_individual) < fitness(graph,best_individual):
            best_individual = new_individual

    print(fitness(graph,best_individual))
    print(best_individual)
    return best_individual


if __name__ == "__main__":
    from Graph_Generator import load_data
    random.seed(2)
    directory = "Preprocessed Datasets"
    dataset = "DBLP"
    #social_graph, skill_map = build_graph(dataset)
    social_graph, skill_map = load_data()
    #initialize(skill_map)
    hill_climbing(social_graph,skill_map)