from flask import Flask, request, jsonify
from flask_cors import CORS

import base64
import io
import pandas as pd
import numpy as np

# functions from own repository  
from dataELT import node_visualization
from dataELT import attributre_visualization
from dataELT import create_edge_histogram
from dataELT import snowball
from alaamintegration import alaam
from alaamintegration import ergm

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Attribute list upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    global attribute_filename
    attribute_filename = file.filename

    try:
        print('Attribute analysis start')
        # Read the file directly into a pandas DataFrame
        stream = io.StringIO(file.stream.read().decode("utf-8"))

        # downstream functions points to this same source
        global attribute_df
        attribute_df = pd.read_csv(stream)

        # extract metadata
        length = len(attribute_df)
        columns = attribute_df.columns.tolist()
        print("Attribut list upload successfully, length of list: ", length)
        print("Name of attributes: ", columns)

        # downstream functions points to this same extracted metadata
        global attribute_visualization_json_data
        attribute_visualization_json_data = attributre_visualization(attribute_df, attribute_filename).get_json()
        print("Attribute analysis completed")

        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Edge list upload route
@app.route('/upload_2', methods=['POST'])
def upload_file_2():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    global edge_filename
    edge_filename = file.filename

    try:
        print('Edge analysis start')
        # Read the file directly into a pandas DataFrame
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        
        # downstream functions points to this same source
        global node_df
        node_df = pd.read_csv(stream, delim_whitespace=True, comment='*')
        
        # extract metadata
        length = len(node_df)
        columns = node_df.columns.tolist()
        print("Node list upload successfully, length of list: ", length)
        print("Name of attributes: ", columns)

        # downstream functions points to this same extracted metadata                
        global node_visualization_json_data
        fig_size = 30
        node_visualization_json_data = node_visualization(node_df, fig_size, edge_filename).get_json()
        print("Edge analysis completed")

        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# route to return descriptive stat and visualisation
@app.route('/get-nodedescriptivestat', methods=['GET'])
def get_nodedescriptivestat():
    print("Edge statistics export to application view")
    return jsonify(node_visualization_json_data)

@app.route('/get-attributevisualisation', methods=['GET'])
def get_attributevisualisation():
    print("Attributes statistics export to application view")
    return jsonify(attribute_visualization_json_data)

# route for selected snowball parameters and output return
@app.route('/get-snowball', methods=['POST'])
def get_snowball():

    print('Snowballing sampling start')
    data = request.json # this is json return from frontend form
    start_node = int(data.get('startNode'))
    num_cycle = int(data.get('numCycle'))
    print('Parameters selected for snowball: Start node: ', start_node, 'No. of cycle: ', num_cycle)
    
    # set global to pass it to ALAAM module
    global snowballed_df
    snowballed_df = snowball(node_df, start_node, num_cycle, edge_filename)

    fig_size = 8
    snowballed_node_visualization_json_data = node_visualization(snowballed_df, fig_size, edge_filename).get_json()
    print("Snowball data export to application view")
    
    return jsonify(snowballed_node_visualization_json_data)

# rotue to get list of attributes of source 
@app.route('/get-startAlaam', methods=['GET'])
def get_startAlaam():
    key_list = list(attribute_visualization_json_data)
    print(key_list)
    return jsonify(key_list)

# route for selected ALAAm parameters and output return 
@app.route('/get-startAlaam', methods=['POST'])
def startAlaam():
    data = request.get_json() # this is json return from frontend form
    selected_attribute = data.get('selectedAttribute')
    max_runs = data.get('maxRuns')
    num_subphases = data.get('numSubphases')
    phase_3_steps = data.get('phase3steps')

    print('Attributes selected for ALAAM analysis: ', selected_attribute, max_runs, num_subphases, phase_3_steps)
    # harded code the returned value for live demostration purpose as ALAAM take +10 mins to run 
    execute_alaam = [{'network_type': 'undirected', 'effect': 'DensityA', 'lambda': 2.0, 'parameter': np.float64(-1.3104), 'stderr': np.float64(0.206), 't_ratio': np.float64(-0.083), 'sacf': 0.048}, {'network_type': 'undirected', 'effect': 'ActivityA', 'lambda': 2.0, 'parameter': np.float64(-0.379), 'stderr': np.float64(0.077), 't_ratio': np.float64(-0.032), 'sacf': -0.09}, {'network_type': 'undirected', 'effect': 'ContagionA', 'lambda': 2.0, 'parameter': np.float64(0.8135), 'stderr': np.float64(0.173), 't_ratio': np.float64(-0.023), 'sacf': -0.046}, {'network_type': 'undirected', 'effect': 'sexF_oOA', 'lambda': 2.0, 'parameter': np.float64(0.2032), 'stderr': np.float64(0.174), 't_ratio': np.float64(-0.071), 'sacf': -0.082}, {'network_type': 'undirected', 'effect': 'loc_oOA', 'lambda': 2.0, 'parameter': np.float64(0.5368), 'stderr': np.float64(0.185), 't_ratio': np.float64(-0.023), 'sacf': 0.012}, {'network_type': 'undirected', 'effect': 'intern_oOA', 'lambda': 2.0, 'parameter': np.float64(-0.1816), 'stderr': np.float64(0.18), 't_ratio': np.float64(0.018), 'sacf': -0.006}, {'network_type': 'undirected', 'effect': 'fails_oOA', 'lambda': 2.0, 'parameter': np.float64(0.7786), 'stderr': np.float64(0.23), 't_ratio': np.float64(-0.082), 'sacf': -0.039}, {'network_type': 'undirected', 'effect': 'finstress_oOA', 'lambda': 2.0, 'parameter': np.float64(0.4734), 'stderr': np.float64(0.094), 't_ratio': np.float64(-0.085), 'sacf': -0.055}]
    # Code to execute ALAAM: result = alaam(node_df, attribute_df, selected_attributes, max_runs, num_subphases, phase_3_steps)
    
    return jsonify(execute_alaam)

# route for ALAAm using snowballed cluster 
@app.route('/get-startSnowballAlaam', methods=['POST'])
def startSnowballAlaam():
    data = request.get_json() # this is json return from frontend form
    print(data)
    selected_attribute = data.get('selectedAttribute')
    max_runs = int(data.get('maxRuns'))
    num_subphases = int(data.get('numSubphases'))
    phase_3_steps = int(data.get('phase3steps'))

    print('Attributes selected for ALAAM analysis: ', selected_attribute, max_runs, num_subphases, phase_3_steps)
    result = alaam(snowballed_df, attribute_df, selected_attribute, max_runs, num_subphases, phase_3_steps)

    return jsonify(result)

# route for selected centrality parameters and output return
@app.route('/get-centrality', methods=['POST'])
def get_centrality():
    
    print('Centrality start')
    data = request.get_json() # this is json return from frontend form
    centrality = data.get('centrality')
    bin_size = int(data.get('binSize'))
    print("Selected centrality: ", centrality, "Bin size: ", bin_size)

    img_io = create_edge_histogram(centrality, node_df, bin_size, edge_filename)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    print("Centrality visualisation export to application view")
    
    return jsonify({'image': img_base64})

# route for ergm
@app.route('/get-ergm', methods=['POST'])
def get_ergm():
    print('ERGM start')
    ergm_result = ergm()
    print("ERGM result export to application view")
    return jsonify(ergm_result)


if __name__ == '__main__':
    app.run(debug=True)