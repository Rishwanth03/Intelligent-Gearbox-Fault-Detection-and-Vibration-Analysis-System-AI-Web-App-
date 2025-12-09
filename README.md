# 🔧 Intelligent Gearbox Fault Detection and Vibration Analysis System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An advanced AI-powered web application for analyzing gearbox vibration data to detect faults and determine damage levels using automated data processing and machine learning techniques. The system provides an intuitive web interface for uploading data and viewing comprehensive visual results for quick condition monitoring.

## 🌟 Features

- **Multi-Format Data Support**: Upload vibration data in CSV, TXT, Excel (XLSX/XLS), or MATLAB (.mat) formats
- **Real-time Analysis**: Instant processing and fault detection
- **Comprehensive Diagnostics**: 
  - Time-domain feature extraction (RMS, Peak, Crest Factor, Kurtosis, etc.)
  - Frequency-domain analysis (FFT, Peak Frequency, Spectral Power)
  - Spectrogram visualization
- **Fault Type Detection**:
  - Bearing faults
  - Rotor unbalance
  - Shaft misalignment
  - Gear mesh faults
- **Damage Level Classification**: Categorizes condition from Healthy to Critical
- **Actionable Recommendations**: Provides maintenance suggestions based on analysis
- **Beautiful Visualizations**: Interactive charts and plots for easy interpretation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rishwanth03/Intelligent-Gearbox-Fault-Detection-and-Vibration-Analysis-System-AI-Web-App-.git
   cd Intelligent-Gearbox-Fault-Detection-and-Vibration-Analysis-System-AI-Web-App-
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Starting the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```
   
   **For development with debug mode:**
   ```bash
   # Linux/macOS
   export FLASK_DEBUG=true
   python app.py
   
   # Windows
   set FLASK_DEBUG=true
   python app.py
   ```
   
   **Note:** Debug mode should never be enabled in production as it poses security risks.

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

### Using the Application

1. **Upload Data**: Click "Choose File" or drag and drop your vibration data file
2. **Analyze**: Click "Analyze Vibration Data" button
3. **Review Results**: View the comprehensive analysis including:
   - Fault score and damage level
   - Detected fault types
   - Time and frequency domain visualizations
   - Maintenance recommendations

### Generating Sample Data

To test the application with sample data:

```bash
python generate_sample_data.py
```

This will create sample vibration signals in the `data/samples/` directory:
- `healthy_signal.csv` - Normal operation
- `bearing_fault_signal.csv` - Bearing defect
- `unbalance_fault_signal.csv` - Rotor unbalance
- `misalignment_fault_signal.csv` - Shaft misalignment
- `gear_fault_signal.csv` - Gear mesh fault

## 📁 Project Structure

```
.
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── generate_sample_data.py     # Sample data generator
├── backend/                    # Backend modules
│   ├── __init__.py
│   ├── analyzer.py            # Fault detection and analysis
│   ├── preprocessor.py        # Data preprocessing and feature extraction
│   └── visualizer.py          # Visualization generation
├── templates/                  # HTML templates
│   └── index.html             # Main web interface
├── uploads/                    # Uploaded files (temporary)
├── data/                       # Data directory
│   └── samples/               # Sample data files
└── models/                     # ML models (for future use)
```

## 🔬 Technical Details

### Signal Processing Pipeline

1. **Data Loading**: Supports multiple file formats
2. **Preprocessing**:
   - DC component removal
   - Bandpass filtering (10-5000 Hz)
3. **Feature Extraction**:
   - Time-domain: RMS, Peak, Crest Factor, Kurtosis, Skewness
   - Frequency-domain: FFT, Peak Frequency, Spectral Power
4. **Fault Detection**:
   - Statistical analysis
   - Pattern recognition
   - Threshold-based classification
5. **Visualization**:
   - Time-domain plot
   - Frequency spectrum
   - Spectrogram
   - Feature comparison

### Damage Levels

- **Healthy** (0-20%): Normal operation
- **Slight** (20-40%): Minor abnormalities, increase monitoring
- **Moderate** (40-60%): Moderate wear, schedule inspection
- **Severe** (60-80%): Severe damage, immediate inspection required
- **Critical** (80-100%): Shutdown recommended

## 🛠️ API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and analyze vibration data
- `GET /health` - Health check endpoint
- `GET /api/analysis/status/<id>` - Get analysis status (for future async processing)

## 📊 Data Format Requirements

Your vibration data file should:
- Contain vibration measurements in a single column or as the first numeric column
- Be sampled at a consistent rate (default: 12 kHz, configurable)
- Represent acceleration values (m/s² or g)

Example CSV format:
```csv
vibration
0.123
0.145
0.132
...
```

## 🔒 Security Considerations

- Maximum file size: 16MB (configurable in `config.py`)
- Allowed file extensions are validated
- Uploaded files are stored temporarily and can be automatically cleaned
- Consider implementing authentication for production use

## 🚧 Future Enhancements

- [ ] Machine learning model integration (CNN, LSTM)
- [ ] Real-time monitoring dashboard
- [ ] Historical trend analysis
- [ ] Multi-sensor data fusion
- [ ] Automated report generation
- [ ] Email/SMS alerts
- [ ] User authentication and role management
- [ ] Database integration for storing analysis history

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shri Rishwanth Udayakumaravadivel**

## 🙏 Acknowledgments

- Signal processing techniques based on vibration analysis literature
- Flask framework for web application
- NumPy, SciPy, and Matplotlib for data processing and visualization
- TensorFlow for future ML integration

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub or contact the author.

---

**Note**: This is an academic/research project. For industrial applications, additional validation and testing are recommended.
