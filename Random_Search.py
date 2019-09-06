import random
from Graph_Generator import load_data
from Utility import create_individual
from Utility import fitness


def random_search(graph,skill_set,iteration=10000,n=6):
    individual = create_individual(skill_set, n)
    best_individual = individual

    for i in range(iteration):
        individual = create_individual(skill_set, n)
        print(fitness(graph,individual))
        if fitness(graph,individual) < fitness(graph,best_individual):
            best_individual = individual
    print(fitness(graph,best_individual))
    print(best_individual)
    return best_individual


if __name__ == "__main__":
    random.seed(2)
    from Graph_Generator import load_data
    directory = "Preprocessed Datasets"
    dataset = "DBLP"
    #social_graph, skill_map = build_graph(dataset)
    social_graph, skill_map = load_data()
    #initialize(skill_map)
    random_search(social_graph,skill_map)