from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from collections import defaultdict

app = Flask(__name__)

# Path to the static folder where PDF files are stored
PDF_PATH = r'C:\Users\DELL\Downloads\PyMuPdF Project\static\Estimate.pdf'

# Store annotations in-memory (this can be saved in a database or a file for persistence)
annotations = defaultdict(list)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/Estimate.pdf')
def serve_pdf():
    return send_from_directory(os.path.dirname(PDF_PATH), os.path.basename(PDF_PATH))

@app.route('/api/save_annotations', methods=['POST'])
def save_annotations():
    data = request.json  # Contains annotations for each page
    annotations.update(data)  # Save the annotations (could be stored in a file/database in the future)

    return jsonify({"status": "success", "message": "Annotations saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
