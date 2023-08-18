import networkx as nx
import random
import matplotlib.pyplot as plt
# import check_deg_seq as cds
import numpy as np

# Set the number of nodes and the m parameter
n = 1000
m = 10

# Create an empty graph
G = nx.Graph()

# Add the initial m nodes to the graph
for i in range(m):
    G.add_node(i)

# Create a list of the nodes that we will use to add edges
node_list = list(range(m))

# Use the Barabasi-Albert algorithm to add edges
for i in range(m, n):
    # Calculate the degree distribution of the nodes in the graph
    degree_dist = [d for n, d in G.degree()]

    # Check if the sum of degree_dist is zero
    if sum(degree_dist) == 0:
        # If the sum is zero, add a random edge to the graph
        u, v = random.sample(range(i), 2)
        G.add_edge(u, v)
        continue

    # Calculate the probability of connecting to each node
    prob = [d / sum(degree_dist) for d in degree_dist]

    # Choose m nodes to connect to
    nodes_to_connect = random.choices(node_list, weights=prob, k=m)

    # Add edges to the graph
    for node in nodes_to_connect:
        G.add_edge(i, node)

    # Add the new node to the node list
    node_list.append(i)

# Check that the graph is connected
if not nx.is_connected(G):
    # If the graph is not connected, keep adding edges until it is
    components = nx.connected_components(G)
    largest_component = max(components, key=len)
    while not nx.is_connected(G):
        node = random.choice(list(largest_component))
        neighbor = random.choice(list(G.nodes()))
        G.add_edge(node, neighbor)

# Remove self-loops
for u, v in list(G.edges()):
    if u == v:
        G.remove_edge(u, v)

# Remove parallel edges
G = nx.Graph(G)

# Print the degree distribution of the graph
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
print("Degree sequence: ", degree_sequence)

# print(cds.check_power_law_degree_sequence(np.array(degree_sequence)))

# Draw the graph
nx.draw(G, with_labels=True)
# plt.show()