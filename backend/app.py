from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this line is present

import pandas as pd
import os
from process import set_x  # Import the set_x function from process.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file to the upload folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Read the CSV file using pandas
    try:
        x = pd.read_csv(file_path)
        y = len(x)
        x.to_csv('file.csv')
        set_x(x)

        return jsonify({"length": y})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)