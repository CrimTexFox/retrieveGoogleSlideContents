from flask import request, send_file, jsonify
from app import app
from app.extract import process_presentation
import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    presentation_id = data.get('presentation_id')
    if not presentation_id:
        logging.error("No presentation_id provided")
        return jsonify({"error": "No presentation_id provided"}), 400

    try:
        result_folder, json_file = process_presentation(presentation_id)
        zip_filename = f"{result_folder}.zip"

        # Create a ZIP file
        shutil.make_archive(result_folder, 'zip', result_folder)

        # Ensure the ZIP file exists before sending
        if not os.path.isfile(zip_filename):
            logging.error("Failed to create ZIP file")
            return jsonify({"error": "Failed to create ZIP file"}), 500

        logging.debug(f"Sending file: {zip_filename}")
        return send_file(zip_filename, mimetype='application/zip', as_attachment=True, download_name='slides_data.zip')
    except Exception as e:
        logging.exception("An error occurred")
        return jsonify({"error": str(e)}), 500
