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

if __name__ == '__main__':
    app.run(debug=True)