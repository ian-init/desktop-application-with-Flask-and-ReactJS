from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present
import base64
import io

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
    betweenness = nx.betweenness_centrality(G)
    
    
    print("NetworkX descriptive stat run successfully")
    
    # Generate betweenness histgrom
    betweenness_value = list(betweenness.values())
    plt.hist(betweenness_value)
    plt.title('Betweenness')
    betweenness_plot = plt.gcf()
    betweenness_plot.savefig('betweenness_hist.png', dpi=300)
    print("Betweenness histogram exported successfully, next one is Clustering Coefficient")
    plt.clf()
    plt.close()

    # Generate Clustering Coefficient histgrom
    clustering_coefficient_value = list(clustering_coefficient.values())
    plt.hist(clustering_coefficient_value)
    plt.title('Clustering Coefficient')
    clustering_coefficient_value_plot = plt.gcf()
    clustering_coefficient_value_plot.savefig('clustering_coefficient_hist.png')
    print("Clustering Coefficient histogram exported successfully, next one is ... ")
    plt.clf()
    plt.close()

    # Node graph
    plt.figure(figsize=(50, 50))
    nx.draw(G, with_labels=False, node_size=10, linewidths=1, font_size=8)
    plt.title('Edge visualization')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    '''
    edge_visualization_plot = plt.gcf()
    edge_visualization_plot.savefig('edge_visualization.png')
    '''
    print("Nodes visualization created successfully")
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    response_data = {
    "length": length,
    "columns": columns,
    "Density": density,
    "Averageclustering": average_clustering,
    "NodesNum": nodes_num,
    "EdgesMum": edges_num,
    "Transitivity": transitivity,
    "image": img_base64,
    }

    return jsonify(response_data)


def attributre_visualization(dataframe):
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
    print(unique_value)

    # Calculate occurance of categories in percentage
    percentage_counts = stack_bar_data.apply(lambda x: x.value_counts(normalize=True)).fillna(0) * 100
    percentage_counts = percentage_counts.T
    percentage_counts.plot(kind='bar', stacked=True)
    plt.xlabel('Columns')
    plt.ylabel('Percentage')
    plt.title('Distributio of attributes values')
    plt.legend(title='Value', labels=unique_value)
    '''
    pstacked_bar_plot = plt.gcf()
    pstacked_bar_plot.savefig('pstacked_bar_plot.png')
    '''
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    print("Attribute visualization successfully")
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')


    # extract attributes values and show in table
    attribute_dict = {}
    for i in range(len(columns) -2):
        attribute_dict[columns[i]] = df_split[columns[i]].unique().tolist()
    ''' 
    df_split[columns[0]].value_counts().plot(
    kind='pie', 
    autopct='%1.1f%%', 
    labels=df_split[columns[0]].value_counts().index
    )
    plt.title("Distribution of Column Values")
    pie_plot = plt.gcf()
    pie_plot.savefig('pie_chart.png')
    plt.clf()
    plt.close()
    '''

    response_data = {
    "length": length,
    "columns": columns,
    "attributeDict": attribute_dict,
    "image": img_base64,
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)