import io
import pickle
import copy


def save_data(graph,skill_set, dataset):
    file = open('Objects/social_graph_'+dataset+'.pkl','wb')
    pickle.dump(graph,file,pickle.HIGHEST_PROTOCOL)
    file.close()
    file = open('Objects/skill_map_'+dataset+'.pkl','wb')
    pickle.dump(skill_set,file,pickle.HIGHEST_PROTOCOL)


def load_data(dataset):
    file = open('Objects/social_graph_'+dataset+'.pkl','rb')
    graph = pickle.load(file)
    file.close()
    file = open('Objects/skill_map_'+dataset+'.pkl','rb')
    skill_set = pickle.load(file)
    return graph,skill_set


def build_graph(dataset, skiprow=0):
    coauthor_filename = directory + "/" + dataset + "_coauthor.csv"
    skill_filename = directory + "/" + dataset + "_skill.csv"

    coauthor_file = io.open(coauthor_filename,'r',errors='ignore')
    skill_file = io.open(skill_filename,'r',errors='ignore')

    lines = coauthor_file.readlines()

    graph = {}
    skill_set ={}

    for line in lines:
        data = line.split(",")
        author = data[0].strip()
        total_publications = int(data[1])
        graph[author] = {}
        graph[author]["total_publications"] = total_publications
        graph[author]["co_authors"] = {}
        graph[author]["skills"] = []

        data = data[2:]
        for i in range(0,len(data),2):
            co_author = data[i].strip()
            percent_publish = float(data[i+1])/total_publications
            graph[author]["co_authors"][co_author] = percent_publish

    lines = skill_file.readlines()

    for line in lines:
        data = line.split(",")
        author = data[0].strip()
        author_node = graph.get(author)
        if author_node:
            author_skills = data[1:]
            for skill in author_skills:
                skill = skill.strip()
                author_node["skills"].append(skill)
                skill_node = skill_set.get(skill)
                if not skill_node:
                    skill_set[skill] = []
                    skill_node = skill_set[skill]
                skill_node.append(author)

    coauthor_file.close()
    skill_file.close()
    skills = skill_set.keys()
    filtered_skill_set = {}

    for skill in skills:
        if len(skill_set[skill]) > 5:
            filtered_skill_set[skill] = skill_set[skill]


    print(len(filtered_skill_set))

    save_data(graph, filtered_skill_set, dataset)

    return graph,skill_set


if __name__ == "__main__":
    directory = "Preprocessed Datasets"
    dataset = "DBLP"
    social_graph, skill_map = build_graph(dataset)
    #social_graph, skill_map = load_data(dataset)
    print(len(social_graph.keys()))
    print(len(skill_map.keys()))