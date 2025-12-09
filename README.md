# Gearbox Dataset Preprocessing Tool

A Python tool for preprocessing gearbox vibration data with automatic labeling and flexible processing options.

## Features

- 🌐 **Web Interface**: Modern browser-based analysis with drag-and-drop upload
- 🧠 **AI Damage Classification**: Intelligent HIGH/MEDIUM/LOW damage detection
- 📊 **Visual Analysis**: Interactive charts and damage indicators
- 🔍 **Detailed Reasoning**: Explains WHY damage levels were assigned
- � **Batch Processing**: Analyze multiple files for fleet management
- 🎯 **Actionable Insights**: Clear maintenance recommendations

## Project Structure

```
GierBox/
├── webapp.py                 # 🌐 Main web application (START HERE)
├── main.py                   # 📊 CLI batch processing
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── data/
│   ├── raw/                 # Raw CSV files (h30hz*.csv)
│   └── processed/           # Processed output files
├── src/
│   ├── __init__.py
│   ├── preprocess.py        # Data preprocessing functions
│   └── damage_classifier.py # 🧠 AI damage analysis engine
├── templates/               # Web interface templates
│   ├── index.html          # Homepage
│   ├── upload.html         # File upload
│   ├── results.html        # Analysis results
│   └── batch_results.html  # Multi-file analysis
└── venv/                    # Python virtual environment
```

## Setup

### 1. Clone/Download the Project
```bash
cd "C:/Users/Shri Rishwanth U K/OneDrive/Desktop/GierBox"
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Verify Setup
```powershell
python main.py --help
```

## Usage

### 🌐 Web Application (Recommended)

#### 1. Start the Web Server
```powershell
python webapp.py
```

#### 2. Open Your Browser  
Navigate to: **http://localhost:5000**

#### 3. Analyze Gearbox Data
- **Upload New Files**: Drag-and-drop CSV files with vibration data
- **Analyze Existing**: Process files from your data/processed folder  
- **View Results**: Get damage classification + detailed explanations + charts

### 📊 Command Line (Batch Processing)

#### Create Combined Dataset
```powershell
# Process all raw files into single dataset
python main.py
```

This creates `data/processed/gearbox_dataset.csv` with all files combined.

## Data Processing

### Labeling Rules

The tool automatically assigns labels based on filename patterns:
- **Healthy (0)**: Files containing `h30hz0` in the filename
- **Faulty (1)**: All other files

### Output Format

Processed files include additional columns:
- `label`: 0 (healthy) or 1 (faulty)
- `source_file`: Original filename for traceability

### Example Output
```
         a1        a2        a3        a4  label  source_file
0  4.636710  0.516978  1.234567  2.345678      0   h30hz0.csv
1  1.992800  4.184660  3.456789  4.567890      0   h30hz0.csv
...
```

## Logging

### Log Levels
- **INFO**: General processing information
- **WARNING**: Non-critical issues
- **ERROR**: Processing errors

### Log Outputs
- **Console**: Real-time progress and results
- **File**: `gearbox_processing.log` for persistent logging

### Example Log Output
```
2025-10-23 10:30:15,123 - INFO - Processing single file: data/raw/h30hz0.csv
2025-10-23 10:30:16,456 - INFO - Processed: data/processed/h30hz0_processed.csv (88832 rows, 6 columns)
```

## Advanced Usage

### 🧠 Programmatic Usage

```python
from src.damage_classifier import DamageClassifier
from src import preprocess

# Analyze damage level
classifier = DamageClassifier()
result = classifier.analyze_file('data/raw/h30hz0.csv')

print(f"Damage Level: {result['damage_level']}")
print(f"Reason: {result['reasoning']['overall']}")

# Batch preprocessing  
combined_df = preprocess.load_and_label_data('data/raw')
preprocess.save_processed_data(combined_df, 'output/dataset.csv')
```

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure virtual environment is activated
   ```powershell
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **File Not Found**: Check file paths and ensure raw data exists
   ```powershell
   dir data\raw\*.csv
   ```

3. **Permission Error**: Ensure write permissions to output directory
   ```powershell
   mkdir data\processed
   ```

### Performance Tips

- Use pattern processing for batch operations
- Monitor log file for progress on large datasets
- Consider processing in chunks for very large files

## Development

### Adding New Features

1. **New preprocessing functions**: Add to `src/preprocess.py`
2. **CLI arguments**: Update argument parser in `main.py`
3. **Custom processors**: Create in `scripts/` directory

### Testing

```powershell
# Test single file processing
python main.py --input data/raw/h30hz0.csv --output test_output.csv

# Test pattern processing
python main.py --pattern "data/raw/h30hz0.csv" --output-dir test_processed
```

## Dependencies

- **pandas**: Data manipulation and CSV I/O
- **tqdm**: Progress bars for batch operations
- **argparse**: Command-line argument parsing (built-in)
- **logging**: Structured logging (built-in)

## License

This project is for educational and research purposes.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request with clear description

---

For questions or issues, check the log files or create an issue in the repository.