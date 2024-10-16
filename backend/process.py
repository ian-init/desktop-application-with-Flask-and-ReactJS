from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present
import base64
import io
from PIL import Image

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import networkx as nx

from datetime import date
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize with some sample data for testing purposes

now = datetime.now()
current_time = now.strftime("%H-%M-%S")
today = date.today()

def node_visualization(dataframe, fig_size):

    print('Visualising edges...')
    # extract csv metadata    
    edge_list = dataframe
    columns = edge_list.columns.tolist()
    length = len(edge_list)

    # descriptive stst using NetworkX library
    G = nx.from_pandas_edgelist(edge_list[['source', 'target']], source='source', target='target', create_using=nx.DiGraph())
    density = nx.density(G)
    average_clustering = nx.average_clustering(G)
    nodes_num = G.number_of_nodes()
    edges_num = G.number_of_edges()
    transitivity = nx.transitivity(G)    
    print("NetworkX descriptive statistics completed")

    # Edge graph
    plt.figure(figsize=(fig_size, fig_size))
    nx.draw(G, with_labels=False, node_size=10, linewidths=1, font_size=8)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    '''
    edge_visualization_plot = plt.gcf()
    edge_visualization_plot.savefig('edge_visualization.png')
    '''
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    response_data = {
    "length": length,
    "columns": columns,
    "Density": density,
    "Averageclustering": average_clustering,
    "NodesNum": nodes_num,
    "EdgesNum": edges_num,
    "Transitivity": transitivity,
    "image": img_base64,
    }

    print("Edge visualisation completed")
    return jsonify(response_data)


def attributre_visualization(dataframe):

    print('Visualising attributes...')
    # extract csv metadata    
    df = pd.DataFrame(dataframe)
    length = len(df)
    columns = df.columns.tolist()
    columns_to_string = ' '.join(columns)
    columns = columns[0].split('\t')      
    df_split = df[columns_to_string].str.split('\t', expand=True)
    df_split.columns = columns

    # Visualise data using stacked bar 
    stack_bar_data = df_split
    stack_bar_data = stack_bar_data.drop(['Label'], axis=1)
 
    unique_value = []
    for i in range(len(columns) -2):
        unique_value += stack_bar_data[columns[i]].unique().tolist()
    unique_value = set(unique_value)

    # Calculate occurance of categories
    percentage_counts = stack_bar_data.apply(lambda x: x.value_counts(normalize=True)).fillna(0) * 100
    percentage_counts = percentage_counts.T
    percentage_counts.plot(kind='bar', stacked=True)
    plt.xlabel('Columns')
    plt.ylabel('Percentage')
    plt.title('Attributes observation')
    plt.legend(title='Value', labels=unique_value)
    '''
    pstacked_bar_plot = plt.gcf()
    pstacked_bar_plot.savefig('pstacked_bar_plot.png')
    '''
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')


    # extract attributes values and show in table
    attribute_dict = {}
    for i in range(len(columns) -2):
        attribute_dict[columns[i]] = df_split[columns[i]].unique().tolist()

    response_data = {
    "length": length,
    "columns": columns,
    "attributeDict": attribute_dict,
    "image": img_base64,
    }

    print("Attribute visualisation completed")
    return jsonify(response_data)


def create_edge_histogram(selectedCentrality, node_df, bin_size):

    print('Visualising centrality...')
    select_centrality = selectedCentrality
    edge_list = node_df
    columns = edge_list.columns.tolist()   
    G = nx.from_pandas_edgelist(edge_list[['source', 'target']], source='source', target='target', create_using=nx.DiGraph())

    if select_centrality == "Betweenness":
        vis = nx.betweenness_centrality(G)
    elif select_centrality == "Closeness":
        vis = nx.closeness_centrality(G)
    elif select_centrality == "Eigenvector":
        vis = nx.eigenvector_centrality(G)
    elif select_centrality == "ClusteringCoefficient":
        vis = nx.clustering(G)

    # Generate centrality histgrom
    vis_value = list(vis.values())
    plt.hist(vis_value, bins=bin_size)
    plt.title(select_centrality)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    print("Histogram generated")
    return img

def snowball(dataframe, start_node, num_cycle):

    print('Clustering start...')
    sampled_edges = []
    current_nodes = {start_node}

    for i in range(num_cycle):
        print("Snowball cycle ", i+1, " running")
        new_nodes = set()  # Initialize a new set to store nodes in this cycle

        for node in current_nodes: 
            # Find the rows in the DataFrame where the current node is the source
            neighbors = dataframe[dataframe['source'] == node]['target'].tolist()
            
            if neighbors:
                for neighbor in neighbors:
                    sampled_edges.append((node, neighbor))
                new_nodes.update(neighbors)  # Add new neighbors to the set of new nodes        
        current_nodes = new_nodes

    sampled_df = pd.DataFrame(sampled_edges, columns=["source", "target"]).drop_duplicates()

    # export snowball sample to user
    sampled_df.to_csv(f"./export/snowball sample,cycle_{num_cycle},start node_{start_node},time_{today}-{current_time}.csv")
    
    print('Snowball cluster generated')
    return sampled_df

    
if __name__ == '__main__':
    app.run(debug=True)


