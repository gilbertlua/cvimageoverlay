import os
import sys
from flask import Blueprint, request, jsonify, send_file

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Lib.twibbon_generator import TwibbonGenerator

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/generate_twibbon', methods=['POST'])
def generate_twibbon():
    try:
        if 'base_image' not in request.files or 'overlay_image' not in request.files:
            return jsonify({"error": "Both base_image and overlay_image are required"}), 400

        base_image = request.files['base_image']
        overlay_image = request.files['overlay_image']
        
        empty_area = request.json.get('empty_area')
        if not empty_area:
            return jsonify({"error": "empty_area JSON data is required"}), 400

        base_path = os.path.join("static", base_image.filename)
        overlay_path = os.path.join("static", overlay_image.filename)

        base_image.save(base_path)
        overlay_image.save(overlay_path)

        generator = TwibbonGenerator(base_path, overlay_path)
        output_path = generator.generate_twibbon(empty_area, output_dir="output")

        return send_file(output_path, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500
