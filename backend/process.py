from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import networkx as nx

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize with some sample data for testing purposes

def node_visualization(dataframe):
    # extract csv metadata    
    edge_list = dataframe
    columns = edge_list.columns.tolist()
    length = len(edge_list)

    # generate node 
    G = nx.from_pandas_edgelist(edge_list[['source', 'target']], source='source', target='target', create_using=nx.DiGraph())
    print("Source Nodes graph generated in the backend successfully")
    
    # descriptive stst using NetworkX library
    density = nx.density(G)
    average_clustering = nx.average_clustering(G)
    nodes_num = G.number_of_nodes()
    edges_num = G.number_of_edges()
    clustering_coefficient = nx.clustering(G)
    transitivity = nx.transitivity(G)
    print("NetworkX descriptive stat run successfully")
    
    # Draw the graph with color-coded nodes
    plt.figure(figsize=(15, 15))
    nx.draw(G, with_labels=False, node_size=10, linewidths=1, font_size=8)
    plt.title('Graph Visualization with Colour-Coded Nodes')
    
    # Save the plot as a PDF file
    graph_plot = plt.gcf()
    graph_plot.savefig('graph_plot.png')  # Saves the plot as a PNG file
    print("Source Nodes graph exported successfully")
    
    return jsonify({"length": length, "columns": columns, "Density": density, "Averageclustering": average_clustering, "NodesNum": nodes_num, "EdgesMum": edges_num, "Transitivity": transitivity})


def attributre_visualization(dataframe):
    # extract csv metadata    
    df = pd.DataFrame(dataframe)
    columns = df.columns.tolist()    
    columns = columns[0].split('\t')

    df_split = df["sexF\tloc\tintern\tdropout\tfails\tfinstress\tLabel\tNode_Set"].str.split('\t', expand=True)
    df_split.columns = columns
    
    #extract attributes details
    attribute_dict = {}
    for i in range(len(columns) -2):
        attribute_dict[columns[i]] = df_split[columns[i]].unique().tolist()

    
    df_split[df_split.columns[0]].value_counts().plot(
    kind='pie', 
    autopct='%1.1f%%', 
    labels=df_split[df_split.columns[0]].value_counts().index
    )

    # Add the title
    plt.title("Distribution of Column Values")

    # Save the figure as a PNG file
    plt.savefig('pie_chart.png')

    # Show the plot (optional)
    plt.show()


    return jsonify(attribute_dict)

if __name__ == '__main__':
    app.run(debug=True)