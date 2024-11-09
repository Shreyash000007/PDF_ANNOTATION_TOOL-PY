from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from collections import defaultdict
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

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

    # Save the annotations to the PDF (this needs implementation)
    annotated_pdf_path = apply_annotations(PDF_PATH, annotations)

    return jsonify({"status": "success", "message": "Annotations saved successfully!"})

@app.route('/api/download_pdf', methods=['GET', 'POST'])
def download_pdf():
    if request.method == 'POST':
        file_name = request.form.get('file_name')
        if file_name:
            file_path = os.path.join(r'C:\Users\DELL\Downloads\PyMuPdF Project\static', file_name)
            if os.path.exists(file_path):
                return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path), as_attachment=True)
            else:
                return jsonify({"status": "error", "message": "File not found."})
        else:
            return jsonify({"status": "error", "message": "File name not provided."})
    else:
        # Path to the saved annotated PDF
        annotated_pdf_path = r'C:\Users\DELL\Downloads\PyMuPdF Project\static\annotated_estimate.pdf'
        if os.path.exists(annotated_pdf_path):
            return send_from_directory(os.path.dirname(annotated_pdf_path), os.path.basename(annotated_pdf_path), as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "Annotated PDF not found."})

def apply_annotations(pdf_path, annotations):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Create a new in-memory file for the annotated PDF
    output_pdf_path = r'C:\Users\DELL\Downloads\PyMuPdF Project\static\annotated_estimate.pdf'
    
    # Iterate through all pages of the original PDF
    for page_num, page in enumerate(reader.pages):
        # Apply annotations for the current page
        if page_num + 1 in annotations:  # Annotations are 1-based index
            for annotation in annotations[page_num + 1]:
                x = annotation['position']['x']
                y = annotation['position']['y']
                width = annotation['position']['width']
                height = annotation['position']['height']
                color = annotation['color']
                annotation_type = annotation['type']
                
                if annotation_type == 'highlight':
                    # Apply highlight annotation using PyPDF2
                    annot = page.Annot(rect=[x, y, x + width, y + height], flags=4, contents='Highlight')
                    annot.set_color(color)
                    page.add_annotation(annot)
                elif annotation_type == 'circle':
                    # Apply circle annotation using PyPDF2
                    annot = page.Annot(rect=[x, y, x + width, y + height], flags=4, contents='Circle')
                    annot.set_color(color)
                    page.add_annotation(annot)
                elif annotation_type == 'underline':
                    # Apply underline annotation using PyPDF2
                    annot = page.Annot(rect=[x, y, x + width, y + height], flags=4, contents='Underline')
                    annot.set_color(color)
                    page.add_annotation(annot)
                elif annotation_type == 'line':
                    # Apply line annotation using PyPDF2
                    annot = page.Annot(rect=[x, y, x + width, y + height], flags=4, contents='Line')
                    annot.set_color(color)
                    page.add_annotation(annot)
        
        writer.add_page(page)
    
    # Save the final annotated PDF to a file
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)
    
    return output_pdf_path


if __name__ == '__main__':
    app.run(debug=True)
