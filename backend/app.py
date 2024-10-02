from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present

import pandas as pd
import io

# Import the set_x function from process.py
from process import attribute_cleaning
from process import node_cleaning

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
        # Read the file directly into a pandas DataFrame without saving it
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        attribute_df = pd.read_csv(stream)
        print("Attribut list upload successfully")
        attribute_cleaning(attribute_df)
        length = len(attribute_df)
        columns = attribute_df.columns.tolist()
        

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
        # Read the file directly into a pandas DataFrame without saving it
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        node_df = pd.read_csv(stream)
        
        print("Node list upload successfully")
        node_cleaning(node_df)
        global length
        length = len(node_df)
        columns = node_df.columns.tolist()

        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    


@app.route('/get-length', methods=['GET'])
def get_length():
    return jsonify({"length": length})


if __name__ == '__main__':
    app.run(debug=True)