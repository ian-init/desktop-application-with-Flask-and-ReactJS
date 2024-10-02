from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present

import pandas as pd
import io

# Import the set_x function from process.py
from process import set_x  


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# First file upload route (no saving to disk)
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
        df = pd.read_csv(stream)
        set_x(df)
        
        # Process the CSV
        length = len(df)
        columns = df.columns.tolist()
        
        print("Attribut list upload successfully")

        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Second file upload route (no saving to disk)
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
        df = pd.read_csv(stream)
        
        # Process the CSV
        length = len(df)
        columns = df.columns.tolist()
        
        
        print("Node list upload successfully")

        return jsonify({"length": length, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)