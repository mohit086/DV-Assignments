import io
import pandas as pd
import networkx as nx
import xml.etree.ElementTree as ET

input_file = 'chinese_buddhism.gexf'
# Note - Added a line <attribute id="n@nationality" title="nationality" type="string"/> to the node attributes of the .gexf file.
# Added it below this line - <attribute id="n@gender" title="gender" type="integer"/> (Line 11)

# Load the GEXF file and parse it
tree = ET.parse(input_file)
root = tree.getroot()
namespace = {"gexf": "http://www.gexf.net/1.2draft"}

# Change all directed edges to undirected
for edge in root.findall(".//gexf:edge", namespaces=namespace):
    if edge.get("type") == "directed":
        edge.set("type", "undirected")

modified_gexf_string = ET.tostring(root, encoding='utf-8', xml_declaration=True)
modified_gexf_file = io.BytesIO(modified_gexf_string)
graph = nx.read_gexf(modified_gexf_file)
print(f'Initially, {len(graph.nodes)} nodes, {len(graph.edges())} edges')

# Remove all 0-degree nodes
nodes_to_remove = [node for node, degree in dict(graph.degree()).items() if degree == 0]
graph.remove_nodes_from(nodes_to_remove)

# Check for and remove duplicate edges
seen_edges = set()
duplicate_edges = []
for u, v in graph.edges():
    edge = (u, v)
    if edge in seen_edges:
        duplicate_edges.append((u, v))
    else:
        seen_edges.add(edge)

for u, v in duplicate_edges:
    graph.remove_edge(u, v)

# Remove specific nodes
for node in ["A013544", "A004261", "G000111"]:
    if node in graph:
        graph.remove_node(node)

# Impute birth years based on neighbors
for i in range(5):
    for node, data in graph.nodes(data=True):
        birth_year = data.get('birthY', 0)
        neighbors = list(graph.neighbors(node))
        if birth_year == 0:
            valid_birth_years = [graph.nodes[neighbor].get('birthY', 0) for neighbor in neighbors if graph.nodes[neighbor].get('birthY', 0) != 0]
            if valid_birth_years:
                average_birth_year = int(sum(valid_birth_years) / len(valid_birth_years))
                graph.nodes[node]['birthY'] = average_birth_year

# Remove nodes with birthY still as 0
nodes_to_remove = [node for node, data in graph.nodes(data=True) if data.get('birthY', 0) == 0]
graph.remove_nodes_from(nodes_to_remove)

# Clear 'deathY' attributes from all nodes
for node in graph.nodes:
    if 'deathY' in graph.nodes[node]:
        del graph.nodes[node]['deathY']

# Clear all edge attributes
for edge in graph.edges:
    graph.edges[edge].clear()  # This will remove all edge attributes

# Relabel nodes and edges to be serial starting from 1
new_id_mapping = {old_id: str(new_id) for new_id, old_id in enumerate(graph.nodes, start=1)}
nx.relabel_nodes(graph, new_id_mapping, copy=False)

# Keep only the largest connected component
largest_component = max(nx.connected_components(graph), key=len)
graph = graph.subgraph(largest_component).copy()

# Filter by top 15 nationalities
nationality_counts = pd.Series([data.get('nationality') for _, data in graph.nodes(data=True)]).value_counts()
top_nationalities = nationality_counts.nlargest(15).index.tolist()

# Remove nodes not in the top nationalities
nodes_to_remove = [node for node, data in graph.nodes(data=True) if data.get('nationality') not in top_nationalities]
graph.remove_nodes_from(nodes_to_remove)

# Save the final graph to a GEXF file
if graph.is_multigraph():
    simple_graph = nx.Graph()
    simple_graph.add_nodes_from(graph.nodes(data=True))
    simple_graph.add_edges_from((u, v, data) for u, v, data in graph.edges(data=True))
else:
    simple_graph = graph

largest_component = max(nx.connected_components(simple_graph), key=len)
graph = simple_graph.subgraph(largest_component).copy()

# Convert to DataFrames
nodes_df = pd.DataFrame(graph.nodes(data=True))
nodes_df.columns = ['id', 'attributes']  # Rename columns for clarity
nodes_df = pd.concat([nodes_df.drop('attributes', axis=1), nodes_df['attributes'].apply(pd.Series)], axis=1)
edges_df = pd.DataFrame(graph.edges(data=True))
edges_df.columns = ['source', 'target', 'attributes']  # Rename columns for clarity
edges_df = pd.concat([edges_df.drop('attributes', axis=1), edges_df['attributes'].apply(pd.Series)], axis=1)

# Save the final graph to CSV
nodes_df.to_csv("nodes.csv", index=False)
edges_df.to_csv("edges.csv", index=False)

# Print statistics
print(f"After preprocessing, {len(nodes_df)} nodes, {len(edges_df)} edges")

# Define subgraph birth year ranges
ranges = [(0, 800), (801, 1400), (1401, 2000)]
for i, (start_year, end_year) in enumerate(ranges, start=1):
    subgraph_nodes = [node for node, data in graph.nodes(data=True)
        if start_year <= data.get('birthY', 0) <= end_year]
    subgraph = graph.subgraph(subgraph_nodes).copy()
    edges_to_remove = [(u, v) for u, v in subgraph.edges
        if not (start_year <= graph.nodes[u].get('birthY', 0) <= end_year and 
        start_year <= graph.nodes[v].get('birthY', 0) <= end_year)]
    subgraph.remove_edges_from(edges_to_remove)
    
    if nx.is_connected(subgraph):
        largest_component = subgraph
    else:
        largest_component = max(nx.connected_components(subgraph), key=len)
        largest_component = subgraph.subgraph(largest_component).copy()
    
    nodes_df = pd.DataFrame(largest_component.nodes(data=True))
    nodes_df.columns = ['id', 'attributes']
    nodes_df = pd.concat([nodes_df.drop('attributes', axis=1),
                          nodes_df['attributes'].apply(pd.Series)], axis=1)
    
    edges_df = pd.DataFrame(largest_component.edges(data=True))
    edges_df.columns = ['source', 'target', 'attributes']
    edges_df = pd.concat([edges_df.drop('attributes', axis=1),
                          edges_df['attributes'].apply(pd.Series)], axis=1)
    
    nodes_df.to_csv(f"nodes{i}.csv", index=False)
    edges_df.to_csv(f"edges{i}.csv", index=False)
    
    print(f"Subgraph {i}: {len(nodes_df)} nodes, {len(edges_df)} edges")