from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Initialize with some sample data for testing purposes

def attribute_cleaning(dataframe):
    global attribute_raw
    attribute_raw = dataframe
    length_1 = len(attribute_raw)
    print(f"Attribute Length: {length_1}")  # Debugging print statement
    return length_1

def node_cleaning(dataframe):
    global node_raw
    node_raw = dataframe
    length_2 = len(node_raw)
    print(f"Node Length: {length_2}")  # Debugging print statement
    return length_2

@app.route('/get_lengths', methods=['GET'])
def get_lengths():
    print("test")
    length_1 = attribute_cleaning(attribute_raw)
    length_2 = node_cleaning(node_raw)
    print(f"Returning lengths: Length 1 = {length_1}, Length 2 = {length_2}")  # Debugging print statement
    return jsonify({'length_1': length_1, 'length_2': length_2})


if __name__ == '__main__':
    app.run(debug=True)