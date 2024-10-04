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

def node_cleaning(dataframe):

    
    edge_list = dataframe
    columns = edge_list.columns.tolist()
    length = len(edge_list)

    G = nx.from_pandas_edgelist(edge_list[['source', 'target']], source='source', target='target', create_using=nx.DiGraph())
    density = nx.density(G)
    
    
    # Draw the graph with color-coded nodes
    plt.figure(figsize=(15, 15))
    nx.draw(G, with_labels=False, node_size=10, linewidths=1, font_size=8)
    plt.title('Graph Visualization with Colour-Coded Nodes')
    
    # Save the plot as a PDF file
    graph_plot = plt.gcf()
    graph_plot.savefig('graph_plot.png')  # Saves the plot as a PNG file

    return jsonify({"length": length, "columns": columns, "Density": density})


if __name__ == '__main__':
    app.run(debug=True)