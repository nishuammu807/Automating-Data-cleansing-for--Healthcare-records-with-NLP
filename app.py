from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from clean_data import clean_healthcare_data  # Import your cleaning function

app = Flask(__name__)
CORS(app)  # Enable CORS for React

UPLOAD_FOLDER = "uploads"
CLEANED_FOLDER = "cleaned"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)  # Save the uploaded file

        # Clean the data
        cleaned_path = os.path.join(CLEANED_FOLDER, "cleaned_" + file.filename)
        clean_healthcare_data(file_path, cleaned_path)  # Clean data

        # Read cleaned data and return as JSON
        df = pd.read_csv(cleaned_path)
        cleaned_data = df.dropna()  # Ensure null values are removed

        return jsonify(cleaned_data.to_dict(orient="records"))  # Send cleaned data to React
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    cleaned_path = os.path.join(CLEANED_FOLDER, filename)
    if os.path.exists(cleaned_path):
        return send_file(cleaned_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
