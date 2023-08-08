import os

import networkx as nx

import utils.graph_to_image_converter


# Function to read node data from file
def read_node_data(file_path, size=1024):
    nodes_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            node, data = line.strip().replace(" ", "").split('=')
            x, y = data.strip('()').split(',')
            x_val = int(eval(x) * size)
            y_val = int(eval(y) * size)
            nodes_data[node] = (x_val, y_val, f'{node}\n({x},{y})\n({x_val},{y_val})')
    return nodes_data


# Function to read adjacency list from file
def read_adjacency_list(file_path, nodes_data):
    adjacency_list = []
    with open(file_path, 'r') as file:
        for line in file:
            node1, node2 = line.strip().split()
            node1_data = (nodes_data[node1][0], nodes_data[node1][1])
            node2_data = (nodes_data[node2][0], nodes_data[node2][1])
            adjacency_list.append((node1_data, node2_data))
    return adjacency_list


os.makedirs('output', exist_ok=True)
os.makedirs('output/pics', exist_ok=True)
os.makedirs('output/graphs', exist_ok=True)

size = 1024
target_files = []
for root, directories, files in os.walk("./digits"):
    for f in files:
        if f.endswith(".adjlist"):
            target_files.append(f.split(".")[0])

for i in target_files:
    # Read node data from file
    node_data_file = f'./digits/{i}.data'
    nodes_data = read_node_data(node_data_file, size)

    # Read adjacency list from file
    adjacency_list_file = f'./digits/{i}.adjlist'
    adjacency_list = read_adjacency_list(adjacency_list_file, nodes_data)

    texts = {}
    for node, data in nodes_data.items():
        texts[(data[0], data[1])] = data[2]

    # Create an empty graph
    G = nx.Graph()
    # Add edges from the adjacency list
    G.add_edges_from(adjacency_list)
    utils.graph_to_image_converter.convert_graph_to_cv2_image(G, size, size, f'./output/pics/{i}.png',
                                                              color=(0, 0, 255),
                                                              size=5, texts=texts)
    nx.write_adjlist(G, f'./output/graphs/{i}.adjlist', delimiter="|")
