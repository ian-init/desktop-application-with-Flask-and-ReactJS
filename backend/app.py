from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io

import pandas as pd
import numpy as np

from dataELT import node_visualization
from dataELT import attributre_visualization
from dataELT import create_edge_histogram
from dataELT import snowball
from alaamintegration import alaam

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
        global attribute_df
        attribute_df = pd.read_csv(stream)

        # Pass back basic information to frontend
        length = len(attribute_df)
        columns = attribute_df.columns.tolist()
        print("Attribut list upload successfully, length of list: ", length)
        print("Name of attributes: ", columns)

        # Pass DataFrame to cleaning module
        global attribute_visualization_json_data
        attribute_visualization_json_data = attributre_visualization(attribute_df, attribute_filename).get_json()
        print("Attribute analysis completed")

        #Return length and columns name to frontend       
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
        global node_df
        node_df = pd.read_csv(stream, delim_whitespace=True, comment='*')
        
        # Pass back basic information to frontend
        length = len(node_df)
        columns = node_df.columns.tolist()
        print("Node list upload successfully, length of list: ", length)
        print("Name of attributes: ", columns)

        # Pass DataFrame to visualisation module                
        global node_visualization_json_data
        fig_size = 30
        node_visualization_json_data = node_visualization(node_df, fig_size, edge_filename).get_json()
        print("Edge analysis completed")

        #Return length and columns name to frontend
        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-nodedescriptivestat', methods=['GET'])
def get_nodedescriptivestat():
    print("Edge statistics export to application view")
    return jsonify(node_visualization_json_data)

@app.route('/get-attributevisualisation', methods=['GET'])
def get_attributevisualisation():
    print("Attributes statistics export to application view")
    return jsonify(attribute_visualization_json_data)

@app.route('/get-snowball', methods=['POST'])
def get_snowball():

    print('Snowballing sampling start')
    data = request.json # this is json return from frontend form
    start_node = int(data.get('startNode'))
    num_cycle = int(data.get('numCycle'))
    print('Parameters selected for snowball: Start node: ', start_node, 'No. of cycle: ', num_cycle)
    
    global snowballed_df
    snowballed_df = snowball(node_df, start_node, num_cycle, edge_filename)

    fig_size = 8
    snowballed_node_visualization_json_data = node_visualization(snowballed_df, fig_size, edge_filename).get_json()
    print("Snowball data export to application view")
    
    return jsonify(snowballed_node_visualization_json_data)

@app.route('/get-startAlaam', methods=['GET'])
def get_startAlaam():
    key_list = list(attribute_visualization_json_data)
    print(key_list)
    return jsonify(key_list)


@app.route('/get-startAlaam', methods=['POST'])
def startAlaam():
    data = request.get_json()
    
    selected_attribute = data.get('selectedAttribute')
    max_runs = data.get('maxRuns')
    num_subphases = data.get('numSubphases')
    phase_3_steps = data.get('phase3steps')

    print('Attributes selected for ALAAM analysis: ', selected_attribute, max_runs, num_subphases, phase_3_steps)
    # result = alaam(node_df, attribute_df, selected_attributes, max_runs, num_subphases, phase_3_steps)
    result = [{'effect': 'DensityA', 'lambda': 2.0, 'parameter': np.float64(-1.1592), 'stderr': np.float64(0.219), 't_ratio': np.float64(0.028), 'sacf': -0.042}, {'effect': 'ActivityA', 'lambda': 2.0, 'parameter': np.float64(-0.3516), 'stderr': np.float64(0.062), 't_ratio': np.float64(0.039), 'sacf': -0.038}, {'effect': 'ContagionA', 'lambda': 2.0, 'parameter': np.float64(0.6237), 'stderr': np.float64(0.139), 't_ratio': np.float64(0.014), 'sacf': -0.065}, {'effect': 'sexF_oOA', 'lambda': 2.0, 'parameter': np.float64(0.1983), 'stderr': np.float64(0.19), 't_ratio': np.float64(0.075), 'sacf': -0.033}, {'effect': 'loc_oOA', 'lambda': 2.0, 'parameter': np.float64(0.5445), 'stderr': np.float64(0.196), 't_ratio': np.float64(0.002), 'sacf': -0.041}, {'effect': 'intern_oOA', 'lambda': 2.0, 'parameter': np.float64(-0.15), 'stderr': np.float64(0.184), 't_ratio': np.float64(-0.0), 'sacf': 0.013}, {'effect': 'fails_oOA', 'lambda': 2.0, 'parameter': np.float64(0.8324), 'stderr': np.float64(0.253), 't_ratio': np.float64(0.008), 'sacf': 0.054}, {'effect': 'finstress_oOA', 'lambda': 2.0, 'parameter': np.float64(0.494), 'stderr': np.float64(0.095), 't_ratio': np.float64(-0.069), 'sacf': 0.003}]

    return jsonify(result)


@app.route('/get-startSnowballAlaam', methods=['POST'])
def startSnowballAlaam():
    data = request.get_json()
    print(data)
    selected_attribute = data.get('selectedAttribute')
    max_runs = int(data.get('maxRuns'))
    num_subphases = int(data.get('numSubphases'))
    phase_3_steps = int(data.get('phase3steps'))

    print('Attributes selected for ALAAM analysis: ', selected_attribute, max_runs, num_subphases, phase_3_steps)
    result = alaam(snowballed_df, attribute_df, selected_attribute, max_runs, num_subphases, phase_3_steps)

    return jsonify(result)


@app.route('/get-centrality', methods=['POST'])
def get_centrality():
    
    print('Centrality calaulcation start')
    data = request.get_json()
    centrality = data.get('centrality')
    bin_size = int(data.get('binSize'))
    print("Selected centrality: ", centrality, "Bin size: ", bin_size)

    img_io = create_edge_histogram(centrality, node_df, bin_size, edge_filename)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    print("Centrality visualisation export to application view")
    
    return jsonify({'image': img_base64})


if __name__ == '__main__':
    app.run(debug=True)