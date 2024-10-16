from flask import Flask, request, jsonify


# Enable cross-origin AJAX
from flask_cors import CORS
import base64
import io

import pandas as pd

from process import node_visualization
from process import attributre_visualization
from process import create_edge_histogram
from process import snowball

from app2 import alaam

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Attribute list upload API
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

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
        attribute_visualization_json_data = attributre_visualization(attribute_df).get_json()
        print("Attribute analysis completed")

        #Return length and columns name to frontend       
        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Node list upload API
@app.route('/upload_2', methods=['POST'])
def upload_file_2():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

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
        fig_size = 20
        node_visualization_json_data = node_visualization(node_df, fig_size).get_json()
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
    
    snowballed_df = snowball(node_df, start_node, num_cycle)
    fig_size = 5
    snowballed_node_visualization_json_data = node_visualization(snowballed_df, fig_size).get_json()
    print("Snowball data export to application view")
    
    return jsonify(snowballed_node_visualization_json_data)

@app.route('/get-startAlaam', methods=['GET'])
def get_startAlaam():
    key_list = list(attribute_visualization_json_data)
    return jsonify(key_list)

@app.route('/get-alaamVariables', methods=['POST'])
def alaamVariables():
    data = request.json
    selected_attributes = str(data.get('selectedAttributes', []))
    print(selected_attributes)

    print('Attributes selected for ALAAM analysis: ', selected_attributes)
    result = alaam(node_df, attribute_df, selected_attributes)

    return jsonify(result)


@app.route('/get-centrality', methods=['POST'])
def get_centrality():
    
    print('Centrality calaulcation start')
    data = request.get_json()
    centrality = data.get('centrality')
    bin_size = int(data.get('binSize'))
    print("Selected centrality: ", centrality, "Bin size: ", bin_size)

    img_io = create_edge_histogram(centrality, node_df, bin_size)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    print("Centrality visualisation export to application view")
    
    return jsonify({'image': img_base64})


if __name__ == '__main__':
    app.run(debug=True)