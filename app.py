"""
Intelligent Gearbox Fault Detection and Vibration Analysis System
Flask Web Application
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from config import Config
from backend.analyzer import VibrationAnalyzer
from backend.preprocessor import DataPreprocessor
from backend.visualizer import create_visualizations

app = Flask(__name__)
app.config.from_object(Config)

# Ensure required directories exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['MODEL_FOLDER'], 
               app.config['DATA_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Initialize analyzer
analyzer = VibrationAnalyzer()
preprocessor = DataPreprocessor()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload CSV, TXT, XLSX, XLS, or MAT files'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process data
        data = preprocessor.load_data(filepath)
        processed_data = preprocessor.preprocess(data)
        
        # Analyze for faults
        analysis_results = analyzer.analyze(processed_data)
        
        # Generate visualizations
        visualizations = create_visualizations(processed_data, analysis_results)
        
        # Clean up uploaded file (optional)
        # os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': analysis_results,
            'visualizations': visualizations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Gearbox Fault Detection System'})


@app.route('/api/analysis/status/<analysis_id>')
def get_analysis_status(analysis_id):
    """Get status of an analysis job"""
    # Placeholder for future async processing
    return jsonify({'status': 'completed', 'analysis_id': analysis_id})


if __name__ == '__main__':
    # Only enable debug mode if explicitly set in environment
    # For production, use a WSGI server like gunicorn instead
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
