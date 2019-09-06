import random
import copy


def generate_random_tasks(skill_set, n=6):
    skills = skill_set.keys()
    tasks = random.sample(skills,k=n)
    return tasks


def create_individual(tasks,skill_set, n=6):
    team = []
    for task in tasks:
        person = random.choice(skill_set[task])
        team.append(person)
    return {"tasks": tasks, "team": team}


def initialize(skill_set,pop_size=100,n=6):
    population = []
    tasks = generate_random_tasks(skill_set, n)
    for i in range(pop_size):
        individual = create_individual(tasks,skill_set,n)
        population.append(individual)
    return population


def copy_individual(individual):
    return copy.deepcopy(individual)


def fitness(graph,individual):
    team = individual["team"]
    score = 0.0

    for author1 in team:
        for author2 in team:
            weight = 0
            if author1 == author2:
                weight = 1.0
            elif graph[author1]["co_authors"].get(author2):
                weight = graph[author1]["co_authors"].get(author2)
            score = score + (1.0 - weight)

    return score/2.0


def mutate(graph,skill_set,individual):
    new_individual = copy_individual(individual)
    to_delete = random.choice(individual["team"])
    new_individual["team"].remove(to_delete)

    tasks = new_individual["tasks"]

    for task in tasks:
        set1 = set(skill_set[task])
        set2 = set(new_individual["team"])
        if not bool(set1.intersection(set2)):
            all_co_authors = set()
            for author in new_individual["team"]:
                co_authors = set(graph[author]["co_authors"].keys())
                all_co_authors = all_co_authors.union(co_authors)

            candidates = set1.intersection(all_co_authors)
            if bool(candidates):
                new_individual["team"].append(random.choice(list(candidates)))
            else:
                new_individual["team"].append(random.choice(list(set1)))

    return new_individual


if __name__ == "__main__":
    from Graph_Generator import load_data
    directory = "Preprocessed Datasets"
    dataset = "DBLP"
    #social_graph, skill_map = build_graph(dataset)
    social_graph, skill_map = load_data()
    #initialize(skill_map)
    tasks = generate_random_tasks(skill_map)
    individual = create_individual(tasks,skill_map)
    mutate(social_graph,skill_map,individual)