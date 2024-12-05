from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
API_KEY = 'your-secure-api-key'  # Replace with a secure key or load from environment

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verify_api_key(request):
    key = request.headers.get('x-api-key')
    if key and key == API_KEY:
        return True
    return False

@app.route('/process', methods=['POST'])
def process_video_endpoint():
    if not verify_api_key(request):
        return jsonify({'error': 'Unauthorized'}), 401

    if 'video' not in request.files:
        return jsonify({'error': 'No video part in the request'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex
        input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
        output_filename = f"enhanced_{unique_id}_{filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Save the uploaded video
        file.save(input_path)
        
        # Call Blender as a subprocess
        blender_command = [
            'blender', 
            '-b',  # Background mode
            '-P', 'enhance_screen_recording.py',  # Blender script
            '--',  # Separator for Blender args and script args
            '--input', input_path,
            '--output', output_path
        ]
        
        try:
            # Run Blender process
            result = subprocess.run(
                blender_command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                timeout=900  # 15 minutes timeout
            )
            
            if result.returncode != 0:
                return jsonify({'error': 'Video processing failed', 'details': result.stderr.decode()}), 500
            
            # Send the processed video
            return send_file(output_path, mimetype='video/mp4', as_attachment=True, attachment_filename=output_filename)
        
        except subprocess.TimeoutExpired:
            return jsonify({'error': 'Video processing timed out'}), 500
        
        except Exception as e:
            return jsonify({'error': 'An error occurred during processing', 'details': str(e)}), 500
        
        finally:
            # Clean up uploaded and output files after sending response
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Video Enhancer API'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)