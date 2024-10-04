from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present
import io

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import networkx as nx

from process import node_cleaning

# Import the set_x function from process.py

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

    try:
        # Read the file directly into a pandas DataFrame
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        attribute_df = pd.read_csv(stream)
        
        # Pass back basic information to frontend
        length = len(attribute_df)
        columns = attribute_df.columns.tolist()
        print("Attribut list upload successfully, length of list: ", length) # print on Flask terminal

        # Pass DataFrame to cleaning module
       
        
        #Return length and columns name to frontend
        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Node list upload route
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
        node_df = pd.read_csv(stream, delim_whitespace=True, comment='*')
        
        global length
        # Pass back basic information to frontend
        length = len(node_df)
        columns = node_df.columns.tolist()
        print("Hode list upload successfully, length of list: ", length)


        # Pass DataFrame to cleaning module
        node_cleaning(node_df)
        
        global json_data
        viewUploadStat = node_cleaning(node_df)
        json_data = viewUploadStat.get_json()
        print(json_data)
        

        #Return length and columns name to frontend
        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get-result', methods=['GET'])
def get_result():
    
    return jsonify(json_data)


if __name__ == '__main__':
    app.run(debug=True)