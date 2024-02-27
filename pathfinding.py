#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27.02.2024

<This software implements spike sorting and detection a la Quiroga: http://www.scholarpedia.org/article/Spike_sorting>
It is based on the MCS Tutorial: https://mcspydatatools.readthedocs.io/en/latest/McsPy-Tutorial_DataAnalysis.html

Copyright (C) <2024>  <Freya Ebba Christ>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

@author: Freya Ebba Christ
"""


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial.distance import euclidean

# Create the graph
G = nx.complete_graph(20, create_using=nx.DiGraph())

# Assign random weights to edges
for (u, v) in G.edges():
    G.edges[u, v]['weight'] = np.random.uniform(1, 10)  # Using uniform distribution for clearer edge weights

# Randomly select 5 nodes as waypoints
waypoints = np.random.choice(list(G.nodes()), size=5, replace=False)

# Node positions using spring layout with adjusted parameters for visual clarity
pos = nx.spring_layout(G, k=0.3, iterations=100)

# Calculate Euclidean distances and identify the pair with the largest distance
max_distance = 0
start_node, destination_node = waypoints[0], waypoints[1]  # Default assignment
for i in range(len(waypoints)):
    for j in range(i + 1, len(waypoints)):
        distance = euclidean(pos[waypoints[i]], pos[waypoints[j]])
        if distance > max_distance:
            max_distance = distance
            start_node, destination_node = waypoints[i], waypoints[j]

# Define the order of waypoints including start and end
waypoints_order = [start_node] + [w for w in waypoints if w not in [start_node, destination_node]] + [destination_node]

# Function to find path through waypoints
def find_path_through_waypoints(G, waypoints):
    path = []
    total_cost = 0
    for i in range(len(waypoints) - 1):
        spath = nx.astar_path(G, waypoints[i], waypoints[i + 1], weight='weight')
        path.extend(spath[:-1])  # Avoid duplicating waypoints
        total_cost += sum(G[spath[i]][spath[i + 1]]['weight'] for i in range(len(spath) - 1))
    path.append(waypoints[-1])  # Add the final waypoint
    
    return path, total_cost

# Find path and total cost
path, total_cost = find_path_through_waypoints(G, waypoints_order)

# Drawing the graph with the path
plt.figure(figsize=(12, 10))

# Draw all nodes with default settings
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightgrey', edgecolors='black')

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='grey', width=1, arrows=True)

# Highlight path edges
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2, arrows=True)

# Highlight waypoints and start/end nodes
nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_size=700, node_color='green', edgecolors='black', label='Start Node')
nx.draw_networkx_nodes(G, pos, nodelist=[destination_node], node_size=700, node_color='red', edgecolors='black', label='Destination Node')
nx.draw_networkx_nodes(G, pos, nodelist=[w for w in waypoints if w not in [start_node, destination_node]], node_size=500, node_color='lightblue', edgecolors='black', label='Waypoints')

# Draw node labels
nx.draw_networkx_labels(G, pos, font_weight='bold')

plt.title(f'Complete Directed Graph with Path through Waypoints\nTotal Cost: {total_cost:.2f}')
plt.axis('off')
plt.legend()
plt.show()
