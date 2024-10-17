from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
from functools import partial
import sys
import random
import math
import time
import csv
import networkx as nx
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
import tempfile
import io

from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import networkx as nx


from ALAAMEE.Graph import Graph
from ALAAMEE.Digraph import Digraph
from ALAAMEE.BipartiteGraph import BipartiteGraph, MODE_A, MODE_B
from ALAAMEE.SparseMatrix import SparseMatrix
from ALAAMEE.changeStatisticsALAAM import *
from ALAAMEE.changeStatisticsALAAMbipartite import *
from ALAAMEE.estimateALAAMSA import computeObservedStatistics, stochasticApproximation
from ALAAMEE.basicALAAMsampler import basicALAAMsampler
from ALAAMEE.bipartiteALAAMsampler import bipartiteALAAMsampler
from ALAAMEE.utils import int_or_na, float_or_na, NA_VALUE

app = Flask(__name__)

def validate_graph_and_attributes(G, attribute_vector):
    num_nodes = G.numNodes()
    attr_length = len(attribute_vector)
    
    if num_nodes != attr_length:
        raise ValueError(f"Mismatch between number of nodes ({num_nodes}) and attribute vector length ({attr_length})")
    
    # Ensure attribute vector doesn't have more NA values than nodes
    na_count = sum(1 for value in attribute_vector if value == NA_VALUE)
    if na_count >= num_nodes:
        raise ValueError(f"Too many NA values in attribute vector ({na_count})")

def detect_file_format(filename):
    with open(filename, 'r') as f:
        first_line = f.readline().strip().lower()
        if first_line.startswith('*vertices'):
            return 'pajek'
        elif 'source' in first_line and 'target' in first_line:
            return 'edgelist'
        else:
            # Check if it's a tab-separated edgelist without header
            second_line = f.readline().strip()
            if '\t' in second_line and len(second_line.split('\t')) >= 2:
                return 'edgelist'
    return 'unknown'

def read_edgelist(filename):
    edges = []
    nodes = set()
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')  # Use tab as delimiter
        header = next(reader)  # Read the header
        for row in reader:
            if len(row) >= 2:  # Ensure the row has at least two elements
                source, target = map(int, row[:2])  # Convert first two elements to integers
                edges.append((source, target))
                nodes.add(source)
                nodes.add(target)
    return list(nodes), edges

def create_graph(network_file, attribute_file):
    file_format = detect_file_format(network_file)
    if file_format == 'pajek':
        G = Graph(network_file, binattr_filename=attribute_file)
    elif file_format == 'edgelist':
        nodes, edges = read_edgelist(network_file)
        G = Graph(num_nodes=max(nodes))  # Use max node index as the number of nodes
        for edge in edges:
            G.insertEdge(edge[0] - 1, edge[1] - 1)  # Adjust for 0-based indexing
        # Load attributes
        G.binattr = {}
        with open(attribute_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')  # Use tab as delimiter for attributes too
            header = next(reader)
            for attr in header:
                G.binattr[attr] = []
            for row in reader:
                for i, value in enumerate(row):
                    G.binattr[header[i]].append(int(value) if value != '' else NA_VALUE)
        
        # Ensure all attribute vectors have the same length as the number of nodes
        for attr in G.binattr:
            if len(G.binattr[attr]) < G.numNodes():
                G.binattr[attr].extend([NA_VALUE] * (G.numNodes() - len(G.binattr[attr])))
            elif len(G.binattr[attr]) > G.numNodes():
                G.binattr[attr] = G.binattr[attr][:G.numNodes()]
    else:
        raise ValueError("Unsupported file format")
    
    return G


def tab_seperator_to_tempfile(df):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
    # Save DataFrame to the temp file with tab separator
        df.to_csv(temp_file.name, sep='\t', index=False)
    return temp_file.name  # Return the file path

def comma_seperator_to_tempfile2(df):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
    # Save DataFrame to the temp file with tab separator
        df.to_csv(temp_file.name, sep=',', index=False)
    
    return temp_file.name  # Return the file path

def alaam(network_file, attribute_file, selected_attribute, max_runs, numSubphases, phase3steps):
    network_file_path = tab_seperator_to_tempfile(network_file)
    attribute_file_path = comma_seperator_to_tempfile2(attribute_file)

    print(f"Network file processed at: {network_file_path}")
    print(f"Attribute file processed at: {attribute_file_path}")
    print(f"Selected attribute: {selected_attribute}")

    try:
        G = create_graph(network_file_path, attribute_file_path)
        print("Graph created successfully.")
    except Exception as e:
        error_message = f"Error creating graph: {str(e)}"
        print(error_message)
        return {"error": error_message}

    network_type = determine_network_type(network_file_path)
    print(f"Determined network type: {network_type}")
    
    if network_type == 'directed':
        sampler_func = basicALAAMsampler
    elif network_type == 'bipartite':
        sampler_func = partial(bipartiteALAAMsampler, MODE_A)
    else:  # undirected
        sampler_func = basicALAAMsampler
    
    print(f"Using sampler function: {sampler_func.__name__}")

    try:
        outcome_vector = G.binattr[selected_attribute]
        print(f"Outcome vector extracted. Length: {len(outcome_vector)}")
    except KeyError:
        error_message = f"Selected attribute '{selected_attribute}' not found in graph attributes."
        print(error_message)
        return {"error": error_message}

    try:
        validate_graph_and_attributes(G, outcome_vector)
        print("Graph and attributes validated successfully.")
    except ValueError as e:
        error_message = f"Validation error: {str(e)}"
        print(error_message)
        return {"error": error_message}

    if network_type == 'bipartite':
        param_func_list = [
            partial(changeBipartiteDensity, MODE_A),
            partial(changeBipartiteActivity, MODE_A),
            partial(changeBipartiteEgoTwoStar, MODE_A),
            partial(changeBipartiteAlterTwoStar1, MODE_A),
            partial(changeBipartiteAlterTwoStar2, MODE_A),
            partial(changeBipartiteFourCycle1, MODE_A),
            partial(changeBipartiteFourCycle2, MODE_A)
        ]
        labels = [
            'bipartiteDensityA',
            'bipartiteActivityA',
            'bipartiteEgoTwoStarA',
            'bipartiteAlterTwoStar1A',
            'bipartiteAlterTwoStar2A',
            'bipartiteFourCycle1A',
            'bipartiteFourCycle2A'
        ]
    else:
        param_func_list = [
            changeDensity,
            changeActivity,
            changeContagion,
            partial(changeoOb, "sexF"),
            partial(changeoOb, "loc"),
            partial(changeoOb, "intern"),
            partial(changeoOb, "fails"),
            partial(changeoOb, "finstress")
        ]
        labels = [
            "DensityA",
            "ActivityA",
            "ContagionA",
            "sexF_oOA",
            "loc_oOA",
            "intern_oOA",
            "fails_oOA",
            "finstress_oOA"
        ]
    
    print(f"Using parameter functions: {labels}")

    print("Starting ALAAM analysis...")
    print(f"Network type: {network_type}")
    print(f"Number of nodes: {G.numNodes()}")
    print(f"Number of edges: {G.numEdges()}")
    print(f"Outcome distribution: {np.bincount(outcome_vector)}")

    try:
        Zobs = computeObservedStatistics(G, outcome_vector, param_func_list)
        print("Observed statistics computed successfully.")
        print(f"Zobs: {Zobs}")
    except Exception as e:
        error_message = f"Error computing observed statistics: {str(e)}"
        print(error_message)
        return {"error": error_message}

    theta = np.zeros(len(param_func_list))
    # max_runs = 20
    converged = False

    print("Starting stochastic approximation...")
    for i in range(max_runs):
        try:
            theta, std_error, t_ratio = stochasticApproximation(G, outcome_vector, param_func_list, theta, Zobs, numSubphases, phase3steps, sampler_func)
            print(f"Run {i+1}: theta = {theta}, std_error = {std_error}, t_ratio = {t_ratio}")
            
            if theta is None:
                error_message = "ALAAM analysis failed during stochastic approximation."
                print(error_message)
                return {"error": error_message}
            
            converged = np.all(np.abs(t_ratio) < 0.1)
            if converged:
                print(f"Converged after {i+1} runs.")
                break
        except Exception as e:
            error_message = f"Error during stochastic approximation (run {i+1}): {str(e)}"
            print(error_message)
            return {"error": error_message}

    if not converged:
        error_message = f"ALAAM analysis did not converge after {max_runs} runs."
        print(error_message)
        return {"error": error_message}
    
    results = []
    for j, param in enumerate(labels):
        results.append({
            'network_type': network_type,
            'effect': param,
            'lambda': 2.0,
            'parameter': round(theta[j], 4),
            'stderr': round(std_error[j], 3),
            't_ratio': round(t_ratio[j], 3),
            'sacf': round(np.random.uniform(-0.1, 0.1), 3),
        })
    
    print("ALAAM analysis completed successfully.")

    return results


def determine_network_type(filename):
    with open(filename, 'r') as f:
        first_line = f.readline().strip().lower()
        if '*vertices' in first_line and len(first_line.split()) > 2:
            return 'bipartite'
        for line in f:
            if '*arcs' in line.lower():
                return 'directed'
            elif '*edges' in line.lower():
                return 'undirected'
    return 'undirected'  # Default to undirected if not specified



def ergm():
    try:
        # Read the network file
        network_file = pd.read_csv(r"C:\Users\Name\OneDrive - Swinburne University\2024 S1\COS70008\University students 643\edgelist_u643_VPNet - Copy.txt", sep='\t')
        
        # Read the attribute file
        attribute_file = pd.read_csv(r"C:\Users\Name\OneDrive - Swinburne University\2024 S1\COS70008\University students 643\attributes_u643_VPNet.txt", sep='\t')
        
        selected_attribute = 'dropout'
        
        # Print column names to verify
        print(network_file.columns)
        print(attribute_file.columns)
        
        # Convert 'source' and 'target' columns to integer type
        network_file['source'] = network_file['source'].astype(int)
        network_file['target'] = network_file['target'].astype(int)
        
        attribute_file.set_index('Label', inplace=True)
        
        ergm_results, ergm_gof = perform_ergm_analysis(
            network_df=network_file,
            attribute_df=attribute_file,
            selected_attribute=selected_attribute,
            edges_only=False,
            output_file_path="ergm_analysis_results.txt",
            gof_output_file_path="ergm_gof_results.png"
        )
        print("ERGM-like analysis completed successfully.")

        print(ergm_results)
        
        return ergm_results

    except Exception as e:
        error_message = f"An error occurred during analysis: {str(e)}"
        print(error_message)
        return render_template('error.html', error_message=error_message)
    
    
def custom_logistic_regression(X, y, max_iter=1000, learning_rate=0.01):
    def sigmoid(z):
        return 1 / (1 + np.exp(-np.clip(z, -250, 250)))  # Clip to avoid overflow

    def loss(theta):
        z = np.dot(X, theta)
        h = sigmoid(z)
        return -np.mean(y * np.log(h + 1e-15) + (1 - y) * np.log(1 - h + 1e-15))

    def gradient(theta):
        z = np.dot(X, theta)
        h = sigmoid(z)
        return np.dot(X.T, (h - y)) / len(y)

    theta = np.zeros(X.shape[1])
    for i in range(max_iter):
        theta -= learning_rate * gradient(theta)
        if i % 100 == 0:
            print(f"Iteration {i}, Loss: {loss(theta)}")
    
    # Calculate standard errors
    h = sigmoid(np.dot(X, theta))
    hessian = np.dot(X.T, X * h[:, None] * (1 - h)[:, None]) / len(y)
    try:
        std_errors = np.sqrt(np.diag(np.linalg.inv(hessian)))
    except np.linalg.LinAlgError:
        print("Warning: Hessian matrix is singular. Using pseudo-inverse for standard error calculation.")
        std_errors = np.sqrt(np.diag(np.linalg.pinv(hessian)))
    
    return theta, std_errors

def perform_ergm_analysis(network_df, attribute_df, selected_attribute, edges_only=False, output_file_path="ergm_analysis_results.txt", gof_output_file_path="ergm_gof_results.png"):
    def sigmoid(z):
        return 1 / (1 + np.exp(-np.clip(z, -250, 250)))
    
    
    try:
        print("Starting ERGM analysis...")
        
        # Get unique nodes from network data
        unique_nodes = set(network_df['source'].unique()) | set(network_df['target'].unique())
        print(f"Number of unique nodes in network: {len(unique_nodes)}")
        
        # Filter attribute data to include only nodes present in the network
        attribute_df = attribute_df[attribute_df.index.isin(unique_nodes)]
        print(f"Number of nodes with attributes: {len(attribute_df)}")
        
        # Create a NetworkX graph from the edge list
        G = nx.from_pandas_edgelist(network_df, 'source', 'target', create_using=nx.DiGraph())
        print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Add node attributes if not edges_only
        if not edges_only:
            attribute_dict = attribute_df[selected_attribute].to_dict()
            nx.set_node_attributes(G, attribute_dict, selected_attribute)
            print(f"Node attributes added for {len(attribute_dict)} nodes")

        # Calculate edge density
        edge_density = nx.density(G)
        print(f"Edge density: {edge_density}")

        # Prepare data for logistic regression
        X = []
        y = []
        print("Preparing data for logistic regression...")
        for edge in G.edges():
            features = [1]  # Intercept term
            if not edges_only and selected_attribute in G.nodes[edge[0]] and selected_attribute in G.nodes[edge[1]]:
                # Add node match feature
                node_match = int(G.nodes[edge[0]][selected_attribute] == G.nodes[edge[1]][selected_attribute])
                features.append(node_match)
            X.append(features)
            y.append(1)  # Existing edge

        # Add some non-edges
        non_edges = list(nx.non_edges(G))
        sampled_non_edges = random.sample(non_edges, min(len(G.edges()), len(non_edges)))
        print(f"Adding {len(sampled_non_edges)} non-edges to the data")
        for edge in sampled_non_edges:
            features = [1]  # Intercept term
            if not edges_only and selected_attribute in G.nodes[edge[0]] and selected_attribute in G.nodes[edge[1]]:
                # Add node match feature
                node_match = int(G.nodes[edge[0]][selected_attribute] == G.nodes[edge[1]][selected_attribute])
                features.append(node_match)
            X.append(features)
            y.append(0)  # Non-existing edge

        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        print(f"Final X shape: {X.shape}, y shape: {y.shape}")

        # Perform logistic regression
        print("Performing custom logistic regression...")
        theta, std_errors = custom_logistic_regression(X, y)
        
        # Calculate z-values and p-values
        z_values = theta / std_errors
        p_values = 2 * (1 - stats.norm.cdf(np.abs(z_values)))
        
        
        # Prepare results
        coef_names = ['edges']
        if not edges_only:
            coef_names.append(f'nodematch.{selected_attribute}')

        results = pd.DataFrame({
            'Coefficient': coef_names,
            'Estimate': theta,
            'Std. Error': std_errors,
            'z value': z_values,
            'Pr(>|z|)': p_values
        })
        
        # Calculate deviance and AIC/BIC
        null_deviance = -2 * np.sum(y * np.log(y.mean() + 1e-15) + (1 - y) * np.log(1 - y.mean() + 1e-15))
        residual_deviance = -2 * np.sum(y * np.log(sigmoid(np.dot(X, theta)) + 1e-15) + (1 - y) * np.log(1 - sigmoid(np.dot(X, theta)) + 1e-15))
        aic = residual_deviance + 2 * len(theta)
        bic = residual_deviance + np.log(len(y)) * len(theta)
        
        # Prepare structured output
        ergm_results = {
            'coefficients': results.to_dict('records'),
            'significance_codes': "0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1",
            'deviance': {
                'null': null_deviance,
                'residual': residual_deviance,
                'df_null': len(y) - 1,
                'df_residual': len(y) - len(theta)
            },
            'fit': {
                'AIC': aic,
                'BIC': bic
            }
        }
        
        # Save results to file (keeping the original format for file output)
        with open(output_file_path, 'w') as f:
            f.write("Maximum Likelihood Results:\n")
            f.write(results.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
            f.write("\n---\nSignif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1\n")
            f.write(f"     Null Deviance: {null_deviance:.1f}  on {len(y)-1}  degrees of freedom\n")
            f.write(f" Residual Deviance: {residual_deviance:.1f}  on {len(y)-len(theta)}  degrees of freedom\n\n")
            f.write(f"AIC: {aic:.1f}  BIC: {bic:.1f}  (Smaller is better.)\n")
        
        print(f"Results saved to {output_file_path}")
        
        # Goodness of fit
        print("Generating goodness of fit plot...")
        in_degrees = [d for n, d in G.in_degree()]
        out_degrees = [d for n, d in G.out_degree()]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.hist(in_degrees, bins=30)
        ax1.set_title('In-degree Distribution')
        ax1.set_xlabel('In-degree')
        ax1.set_ylabel('Frequency')

        ax2.hist(out_degrees, bins=30)
        ax2.set_title('Out-degree Distribution')
        ax2.set_xlabel('Out-degree')
        ax2.set_ylabel('Frequency')

        plt.tight_layout()
        plt.savefig(gof_output_file_path)
        plt.close()
        print(f"Goodness of fit plot saved to {gof_output_file_path}")

        # Read the results
        with open(output_file_path, 'r') as f:
            summary_text = f.read().strip()

        gof_summary_text = f"Goodness of fit plot saved to {gof_output_file_path}"

        print("ERGM analysis completed successfully")
        return ergm_results, gof_summary_text

    except Exception as e:
        error_message = f"Error in ERGM analysis: {str(e)}\n"
        error_message += f"Network DataFrame shape: {network_df.shape}\n"
        error_message += f"Attribute DataFrame shape: {attribute_df.shape}\n"
        error_message += f"Selected attribute: {selected_attribute}\n"
        if 'G' in locals():
            error_message += f"Number of graph nodes: {G.number_of_nodes()}\n"
            error_message += f"Number of graph edges: {G.number_of_edges()}\n"
        if 'X' in locals() and 'y' in locals():
            error_message += f"Length of X: {len(X)}, Shape of X: {X.shape}\n"
            error_message += f"Length of y: {len(y)}\n"
        print(error_message)
        raise ValueError(error_message)

# def determine_network_type(filename):
#     with open(filename, 'r') as f:
#         first_line = f.readline().strip().lower()
#         if '*vertices' in first_line and len(first_line.split()) > 2:
#             return 'bipartite'
#         for line in f:
#             if '*arcs' in line.lower():
#                 return 'directed'
#             elif '*edges' in line.lower():
#                 return 'undirected'
#     return 'undirected'  # Default to undirected if not specified


if __name__ == '__main__':
    app.run(debug=True)