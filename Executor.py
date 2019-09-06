from Utility import generate_random_tasks
from Utility import fitness


def execute_single_state(graph, skill_set, algorithm, sample=100, iteration=1000, task_size=6):
    all_tasks = []
    for i in range(sample):
        tasks = generate_random_tasks(skill_set, task_size)
        all_tasks.append(tasks)

    results = []

    for i in range(sample):
        result = algorithm(all_tasks[i], graph, skill_set, iteration)
        results.append(result)

    total_fitness = 0.0
    total_team_size = 0.0

    for i in range(sample):
        total_fitness += fitness(graph, results[i])
        total_team_size += len(set(results[i]["team"]))

    avg_fitness = total_fitness / sample
    avg_team_size = total_team_size / sample

    print("Avg. Team Size: ", avg_team_size)
    print("Avg. Fitness: ", avg_fitness)

    return avg_team_size, avg_fitness
