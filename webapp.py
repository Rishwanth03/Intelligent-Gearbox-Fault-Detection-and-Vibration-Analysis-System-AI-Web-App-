from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
from src.damage_classifier import DamageClassifier
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'gearbox_damage_analysis_2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize damage classifier
classifier = DamageClassifier()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_visualization(df, analysis_result):
    """Create visualizations for the analysis."""
    
    # Set style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Gearbox Analysis: {analysis_result["filename"]} - {analysis_result["damage_level"]} Damage', 
                 fontsize=16, fontweight='bold')
    
    # Get vibration columns
    vibration_cols = [col for col in df.columns if col.startswith('a')]
    
    if len(vibration_cols) >= 2:
        # Time series plot
        sample_size = min(1000, len(df))
        sample_df = df.head(sample_size)
        
        axes[0, 0].plot(sample_df.index, sample_df[vibration_cols[0]], label=vibration_cols[0], alpha=0.7)
        axes[0, 0].plot(sample_df.index, sample_df[vibration_cols[1]], label=vibration_cols[1], alpha=0.7)
        axes[0, 0].set_title('Vibration Time Series (First 1000 samples)')
        axes[0, 0].set_xlabel('Sample Index')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Distribution plots
        axes[0, 1].hist(df[vibration_cols[0]], bins=50, alpha=0.7, label=vibration_cols[0], density=True)
        axes[0, 1].hist(df[vibration_cols[1]], bins=50, alpha=0.7, label=vibration_cols[1], density=True)
        axes[0, 1].set_title('Amplitude Distribution')
        axes[0, 1].set_xlabel('Amplitude')
        axes[0, 1].set_ylabel('Density')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Feature bar chart
        features = analysis_result.get('features', {})
        if features:
            feature_names = list(features.keys())[:8]  # Top 8 features
            feature_values = [features[name] for name in feature_names]
            
            bars = axes[1, 0].bar(range(len(feature_names)), feature_values, 
                                 color=['red' if analysis_result['damage_level'] == 'HIGH' else 
                                       'orange' if analysis_result['damage_level'] == 'MEDIUM' else 'green'])
            axes[1, 0].set_title('Key Features')
            axes[1, 0].set_xlabel('Features')
            axes[1, 0].set_ylabel('Value')
            axes[1, 0].set_xticks(range(len(feature_names)))
            axes[1, 0].set_xticklabels(feature_names, rotation=45, ha='right')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, feature_values):
                axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(feature_values)*0.01,
                               f'{value:.2f}', ha='center', va='bottom', fontsize=8)
        
        # Damage level indicator
        damage_colors = {'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'}
        damage_scores = {'LOW': 25, 'MEDIUM': 50, 'HIGH': 85}
        
        level = analysis_result['damage_level']
        color = damage_colors[level]
        score = damage_scores.get(level, 50)
        
        # Create a gauge-like chart
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        axes[1, 1] = plt.subplot(2, 2, 4, projection='polar')
        axes[1, 1].plot(theta, r, 'k-', linewidth=2)
        axes[1, 1].fill_between(theta, 0, r, alpha=0.3, color=color)
        axes[1, 1].set_ylim(0, 1)
        axes[1, 1].set_title(f'Damage Level: {level}', pad=20)
        axes[1, 1].set_yticks([])
        axes[1, 1].set_xticks([0, np.pi/2, np.pi])
        axes[1, 1].set_xticklabels(['LOW', 'MEDIUM', 'HIGH'])
        
        # Add arrow pointing to current level
        angle_map = {'LOW': 0.2, 'MEDIUM': np.pi/2, 'HIGH': 2.8}
        arrow_angle = angle_map.get(level, np.pi/2)
        axes[1, 1].annotate('', xy=(arrow_angle, 0.8), xytext=(np.pi/2, 0.3),
                           arrowprops=dict(arrowstyle='->', lw=3, color='black'))
    
    plt.tight_layout()
    
    # Convert to base64 string
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_string = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close(fig)
    
    return img_string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Analyze the file
            try:
                analysis_result = classifier.analyze_file(filepath)
                
                # If analysis successful, create visualizations
                if 'error' not in analysis_result:
                    df = pd.read_csv(filepath)
                    visualization = create_visualization(df, analysis_result)
                    analysis_result['visualization'] = visualization
                
                return render_template('results.html', 
                                     result=analysis_result,
                                     filename=filename)
                
            except Exception as e:
                logger.error(f"Analysis error: {str(e)}")
                flash(f'Error analyzing file: {str(e)}')
                return redirect(url_for('upload_file'))
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/analyze_existing')
def analyze_existing():
    """Analyze existing processed files."""
    
    processed_dir = 'data/processed'
    if not os.path.exists(processed_dir):
        flash('No processed files found. Please run the preprocessing first.')
        return redirect(url_for('index'))
    
    csv_files = [f for f in os.listdir(processed_dir) 
                if f.endswith('.csv') and 'processed' in f]
    
    if not csv_files:
        flash('No processed CSV files found.')
        return redirect(url_for('index'))
    
    results = []
    for filename in csv_files[:5]:  # Limit to first 5 files
        filepath = os.path.join(processed_dir, filename)
        try:
            analysis = classifier.analyze_file(filepath)
            if 'error' not in analysis:
                results.append(analysis)
        except Exception as e:
            logger.error(f"Error analyzing {filename}: {str(e)}")
    
    return render_template('batch_results.html', results=results)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for file analysis."""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. CSV required.'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = classifier.analyze_file(filepath)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)