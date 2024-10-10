from flask import Flask, request, jsonify
# Enable cross-origin AJAX
from flask_cors import CORS
import io

import pandas as pd

from process import node_visualization
from process import attributre_visualization

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
        print("Attribute successfully extracted: ", attribute_visualization_json_data)

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
        node_visualization_json_data = node_visualization(node_df).get_json()
        print("Node successfully extracted: ", node_visualization_json_data)


        #Return length and columns name to frontend
        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# return to frontend
@app.route('/get-nodedescriptivestat', methods=['GET'])
def get_nodedescriptivestat():
    return jsonify(node_visualization_json_data)

@app.route('/get-attributevisualisation', methods=['GET'])
def get_attributevisualisation():
    return jsonify(attribute_visualization_json_data)

@app.route('/get-startAlaam', methods=['GET'])
def get_startAlaam():
    key_list = list(attribute_visualization_json_data)
    return jsonify(key_list)

@app.route('/get-alaamVariables', methods=['POST'])
def alaamVariables():
    data = request.json
    selected_keys = data.get('selectedKeys', [])
    print('Attributes selected for ALAAM analysis: ', selected_keys)
    return jsonify({"message": "Data received", "selected_keys": selected_keys})

if __name__ == '__main__':
    app.run(debug=True)