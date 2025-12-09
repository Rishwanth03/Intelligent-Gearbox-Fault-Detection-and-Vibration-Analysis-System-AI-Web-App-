# Project Overview

## Intelligent Gearbox Fault Detection and Vibration Analysis System

A complete, production-ready web application for analyzing gearbox vibration data and detecting mechanical faults using signal processing and AI techniques.

## 📦 What's Included

### Core Application Files

1. **app.py** - Main Flask web application
   - REST API endpoints
   - File upload handling
   - Request routing
   - Error handling

2. **config.py** - Configuration management
   - Application settings
   - File upload limits
   - Analysis parameters
   - Damage level thresholds

### Backend Modules

Located in `backend/` directory:

1. **preprocessor.py** - Data preprocessing
   - Multi-format file loading (CSV, Excel, MATLAB, TXT)
   - Signal filtering and conditioning
   - Feature extraction (time and frequency domain)
   - Statistical calculations

2. **analyzer.py** - Fault detection and analysis
   - Fault score calculation
   - Damage level classification
   - Fault type identification
   - Recommendation generation

3. **visualizer.py** - Data visualization
   - Time-domain plots
   - Frequency spectrum (FFT)
   - Spectrograms
   - Feature comparison charts

### Frontend

1. **templates/index.html** - Web interface
   - Responsive design
   - Drag-and-drop file upload
   - Real-time analysis feedback
   - Interactive result displays
   - Beautiful visualizations

### Utilities

1. **generate_sample_data.py** - Sample data generator
   - Creates healthy signal samples
   - Generates various fault types
   - Configurable signal parameters

2. **test_system.py** - Test suite
   - Backend module tests
   - Integration tests
   - Validation checks

### Setup & Deployment

1. **setup.sh** / **setup.bat** - Automated setup scripts
   - Environment setup
   - Dependency installation
   - Sample data generation
   - Initial testing

2. **requirements.txt** - Python dependencies
   - Flask (web framework)
   - NumPy (numerical computing)
   - Pandas (data manipulation)
   - SciPy (signal processing)
   - Matplotlib (visualization)
   - scikit-learn (machine learning)

### Documentation

1. **README.md** - Main documentation
   - Project overview
   - Installation instructions
   - Usage guide
   - Feature descriptions

2. **API.md** - API documentation
   - Endpoint descriptions
   - Request/response formats
   - Example usage
   - Error handling

3. **DEPLOYMENT.md** - Deployment guide
   - Production setup
   - Docker configuration
   - Cloud deployment options
   - Security considerations

4. **CONTRIBUTING.md** - Contribution guidelines
   - Development setup
   - Code style
   - Testing requirements
   - Pull request process

### Configuration Files

1. **.gitignore** - Git ignore rules
   - Python artifacts
   - Virtual environments
   - Upload directories
   - Data files

2. **LICENSE** - MIT License

## 🎯 Key Features

### Signal Processing
- DC component removal
- Bandpass filtering (10-5000 Hz)
- FFT analysis
- Spectrogram generation
- Time-domain statistics

### Feature Extraction
- RMS (Root Mean Square)
- Peak amplitude
- Crest factor
- Kurtosis
- Skewness
- Peak frequency
- Spectral power
- Band power distribution

### Fault Detection
- Bearing defects
- Rotor unbalance
- Shaft misalignment
- Gear mesh problems
- General abnormalities

### Damage Assessment
- 5-level classification
  - Healthy (0-20%)
  - Slight (20-40%)
  - Moderate (40-60%)
  - Severe (60-80%)
  - Critical (80-100%)

### Recommendations
- Severity-based maintenance advice
- Fault-specific inspection guidance
- Operational recommendations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Web Browser (Client)              │
│  - File upload interface                    │
│  - Result visualization                     │
│  - Interactive charts                       │
└────────────────┬────────────────────────────┘
                 │ HTTP/AJAX
                 ▼
┌─────────────────────────────────────────────┐
│         Flask Web Server                    │
│  - Request handling                         │
│  - File validation                          │
│  - Response formatting                      │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         Backend Processing                  │
│  ┌─────────────────────────────────────┐   │
│  │ Preprocessor                        │   │
│  │  - Load data                        │   │
│  │  - Filter signal                    │   │
│  │  - Extract features                 │   │
│  └──────────┬──────────────────────────┘   │
│             │                               │
│             ▼                               │
│  ┌─────────────────────────────────────┐   │
│  │ Analyzer                            │   │
│  │  - Calculate fault score            │   │
│  │  - Classify damage level            │   │
│  │  - Detect fault types               │   │
│  │  - Generate recommendations         │   │
│  └──────────┬──────────────────────────┘   │
│             │                               │
│             ▼                               │
│  ┌─────────────────────────────────────┐   │
│  │ Visualizer                          │   │
│  │  - Create time plots                │   │
│  │  - Generate FFT plots               │   │
│  │  - Build spectrograms               │   │
│  │  - Render feature charts            │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 📊 Data Flow

1. **Upload**: User uploads vibration data file
2. **Validation**: Server validates file type and size
3. **Loading**: Data loaded from file (CSV/Excel/MATLAB/TXT)
4. **Preprocessing**: Signal filtered and features extracted
5. **Analysis**: Faults detected and severity assessed
6. **Visualization**: Charts and plots generated
7. **Response**: Results sent back to browser
8. **Display**: User views analysis results and visualizations

## 🔧 Technology Stack

- **Backend**: Python 3.8+, Flask
- **Signal Processing**: NumPy, SciPy
- **Data Handling**: Pandas
- **Visualization**: Matplotlib
- **ML Ready**: scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 🚀 Quick Start

```bash
# Clone repository
git clone [repository-url]
cd Intelligent-Gearbox-Fault-Detection-and-Vibration-Analysis-System-AI-Web-App-

# Run setup (Linux/macOS)
./setup.sh

# Or run setup (Windows)
setup.bat

# Manual start
python app.py
```

## 📁 Directory Structure

```
.
├── app.py                    # Main application
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── backend/                  # Backend modules
│   ├── __init__.py
│   ├── analyzer.py
│   ├── preprocessor.py
│   └── visualizer.py
├── templates/                # HTML templates
│   └── index.html
├── uploads/                  # Temporary uploads
├── data/                     # Data directory
│   └── samples/             # Sample data
├── models/                   # ML models
├── generate_sample_data.py  # Data generator
├── test_system.py           # Test suite
├── setup.sh                 # Linux/macOS setup
├── setup.bat                # Windows setup
├── README.md                # Main documentation
├── API.md                   # API docs
├── DEPLOYMENT.md            # Deployment guide
├── CONTRIBUTING.md          # Contribution guide
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore rules
```

## 🧪 Testing

```bash
# Run test suite
python test_system.py

# Generate sample data
python generate_sample_data.py

# Test with sample files
# Use files in data/samples/ directory
```

## 🎨 UI Features

- Modern gradient design
- Drag-and-drop file upload
- Loading indicators
- Color-coded damage levels
- Responsive layout
- Interactive visualizations
- Real-time feedback
- Error handling

## 🔐 Security Features

- File type validation
- File size limits
- Secure filename handling
- Input sanitization
- Error message filtering

## 📈 Future Enhancements

- [ ] Deep learning models (CNN, LSTM)
- [ ] Real-time monitoring
- [ ] Historical trend analysis
- [ ] Multi-sensor fusion
- [ ] Automated reporting
- [ ] Alert notifications
- [ ] User authentication
- [ ] Database integration
- [ ] API rate limiting
- [ ] WebSocket support

## 📝 Version

Current Version: 1.0.0 (Initial Release)

## 👥 Author

Shri Rishwanth Udayakumaravadivel

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

See CONTRIBUTING.md for contribution guidelines

## 📧 Support

- GitHub Issues: For bug reports and feature requests
- Documentation: See README.md, API.md, DEPLOYMENT.md

## 🌟 Acknowledgments

Built with modern web technologies and signal processing techniques for condition monitoring and predictive maintenance applications.
