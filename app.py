from flask import Flask, render_template, request, send_file, after_this_request
import fitz  # PyMuPDF
import json
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_pdf', methods=['POST'])
def save_pdf():
    try:
        app.logger.info("Received save_pdf request")

        # Decode the received annotation data
        annotation_data = request.get_json()
        pdf_path = "Pdf_Annotation/static/Estimate.pdf"  # Replace with your PDF path

        try:
            doc = fitz.open(pdf_path)
            app.logger.info("Opened PDF document")
        except Exception as e:
            app.logger.error(f"Error opening PDF: {e}")
            return f"Error opening PDF: {e}", 500

        # Apply annotations to the PDF document
        for page_num, annotations in annotation_data.items():
            page = doc.load_page(page_num - 1)  # page_num is 1-based, PyMuPDF is 0-based
            for annotation in annotations:
                if annotation['type'] == 'highlight':
                    rect = fitz.Rect(annotation['position'])
                    highlight = page.add_highlight_annot(rect)
                    highlight.set_colors(stroke=annotation['color'])
                elif annotation['type'] == 'circle':
                    rect = fitz.Rect(annotation['position'])
                    circle = page.add_shape(rect)
                    circle.set_stroke_color(annotation['color'])
                elif annotation['type'] == 'underline':
                    rect = fitz.Rect(annotation['position'])
                    underline = page.add_underline_annot(rect)
                    underline.set_colors(stroke=annotation['color'])
                elif annotation['type'] == 'line':
                    rect = fitz.Rect(annotation['position'])
                    line = page.add_line_annot(rect)
                    line.set_colors(stroke=annotation['color'])

        # Save the annotated PDF to a temporary file
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp_path = tmp.name
                doc.write(tmp)  # Use doc.write(tmp) instead of doc.save(tmp.name)
                app.logger.info(f"Saved annotated PDF to temporary file: {tmp_path}")
        except Exception as e:
            app.logger.error(f"Error saving annotated PDF: {e}")
            return f"Error saving annotated PDF: {e}", 500

        # Send the annotated PDF file to the user for download
        @after_this_request
        def remove_file(response):
            try:
                os.remove(tmp_path)
                app.logger.info(f"Removed temporary file: {tmp_path}")
            except Exception as error:
                app.logger.error(f"Error removing temporary file: {error}")
            return response

        return send_file(tmp_path, as_attachment=True, download_name="annotated.pdf", mimetype="application/pdf")

    except Exception as e:
        app.logger.error(f"Error in save_pdf: {e}")
        return "Error saving PDF", 500

if __name__ == '__main__':
    app.run(debug=True)
