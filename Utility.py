import random
import copy
from Graph_Generator import load_data


def generate_random_tasks(skill_set, task_size=6):
    skills = skill_set.keys()
    tasks = random.sample(skills, k=task_size)
    return tasks


def create_individual(tasks, skill_set):
    team = []
    for task in tasks:
        person = random.choice(skill_set[task])
        team.append(person)
    return {"tasks": tasks, "team": team}


def initialize(tasks, skill_set, pop_size=100):
    population = []

    for i in range(pop_size):
        individual = create_individual(tasks, skill_set)
        population.append(individual)
    return population


def seeded_create_individual(tasks, graph, skill_set):
    team = []
    for task in tasks:
        set1 = set(skill_set[task])
        set2 = set(team)
        if not bool(set1.intersection(set2)):
            all_co_authors = set()
            for author in team:
                co_authors = set(graph[author]["co_authors"].keys())
                all_co_authors = all_co_authors.union(co_authors)

            candidates = set1.intersection(all_co_authors)
            if bool(candidates):
                team.append(random.choice(list(candidates)))
            else:
                team.append(random.choice(list(set1)))

    return {"tasks": tasks, "team": team}


def seeded_initialize(tasks, graph, skill_set, pop_size=100):
    population = []

    for i in range(pop_size):
        individual = seeded_create_individual(tasks,graph,skill_set)
        population.append(individual)
    return population



def copy_individual(individual):
    return copy.deepcopy(individual)


def fitness(graph, individual):
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

    return score / 2.0


def mutate(graph, skill_set, individual):
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


def tournament_selection(graph, population, tournament_size=2):
    best_individual = random.choice(population)

    for i in range(1, tournament_size):
        individual = random.choice(population)

        if fitness(graph, individual) < fitness(graph, best_individual):
            best_individual = individual

    return copy_individual(best_individual)


def crossover(skill_set, individual1, individual2):
    tasks = individual1["tasks"]
    child_1 = {"tasks": tasks, "team": []}
    child_2 = {"tasks": tasks, "team": []}

    set1 = set(individual1["team"])
    set2 = set(individual2["team"])

    team1 = set()
    team2 = set()

    for task in tasks:
        set3 = set(skill_set[task])
        candidate1 = set()
        candidate2 = set()
        if random.random() < 0.5:
            candidate1 = set3.intersection(set1)
            candidate2 = set3.intersection(set2)

        else:
            candidate1 = set3.intersection(set2)
            candidate2 = set3.intersection(set1)

        team1.add(random.choice(list(candidate1)))
        team2.add(random.choice(list(candidate2)))

    child_1["team"] = list(team1)
    child_2["team"] = list(team2)

    return child_1,child_2


if __name__ == "__main__":
    social_graph, skill_map = load_data()
    tasks = generate_random_tasks(skill_map)
    population = initialize(tasks, skill_map)
    individual1 = tournament_selection(social_graph, population)
    individual2 = tournament_selection(social_graph, population)

    print(individual1["team"])
    print(individual2["team"])

    child1, child2 = crossover(skill_map, individual1, individual2)

    print(child1["team"])
    print(child2["team"])
