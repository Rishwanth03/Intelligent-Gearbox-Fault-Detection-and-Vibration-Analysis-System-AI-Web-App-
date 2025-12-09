# API Documentation

This document describes the API endpoints available in the Gearbox Fault Detection System.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Main Page

**GET /**

Returns the main web interface.

**Response:** HTML page

---

### 2. Health Check

**GET /health**

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Gearbox Fault Detection System"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

---

### 3. Upload and Analyze

**POST /upload**

Upload vibration data file and get analysis results.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body Parameter:**
  - `file` (required): Vibration data file

**Supported File Formats:**
- CSV (.csv)
- Text (.txt)
- Excel (.xlsx, .xls)
- MATLAB (.mat)

**Response:**
```json
{
  "success": true,
  "results": {
    "fault_score": 0.65,
    "damage_level": "moderate",
    "is_faulty": true,
    "fault_types": [
      {
        "type": "bearing_fault",
        "confidence": 0.75,
        "description": "Possible bearing defect detected"
      }
    ],
    "recommendations": [
      "Moderate wear detected. Schedule inspection within 2-4 weeks.",
      "Inspect bearings for wear, contamination, or lubrication issues."
    ],
    "time_features": {
      "mean": 0.002,
      "std": 1.234,
      "rms": 1.235,
      "peak": 5.678,
      "peak_to_peak": 11.234,
      "crest_factor": 4.598,
      "kurtosis": 6.234,
      "skewness": 0.123
    },
    "freq_features": {
      "peak_frequency": 85.5,
      "spectral_power": 12345.67,
      "frequency_bands": {
        "low": 1234.5,
        "mid": 5678.9,
        "high": 2345.6
      }
    }
  },
  "visualizations": {
    "time_domain": "base64_encoded_image",
    "frequency_domain": "base64_encoded_image",
    "spectrogram": "base64_encoded_image",
    "features": "base64_encoded_image"
  }
}
```

**Error Response:**
```json
{
  "error": "Error message description"
}
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request (no file, wrong format, etc.)
- `500 Internal Server Error`: Server error during analysis

---

### 4. Analysis Status

**GET /api/analysis/status/<analysis_id>**

Get the status of an analysis job (placeholder for future async processing).

**Parameters:**
- `analysis_id` (path): ID of the analysis job

**Response:**
```json
{
  "status": "completed",
  "analysis_id": "12345"
}
```

**Status Codes:**
- `200 OK`: Status retrieved successfully

---

## Data Models

### Fault Score
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Description:** Overall fault severity score

### Damage Level
- **Type:** String
- **Values:**
  - `healthy` (0-20%): Normal operation
  - `slight` (20-40%): Minor abnormalities
  - `moderate` (40-60%): Moderate wear
  - `severe` (60-80%): Severe damage
  - `critical` (80-100%): Critical condition

### Fault Types
Detected fault categories:
- `bearing_fault`: Bearing defects
- `unbalance`: Rotor unbalance
- `misalignment`: Shaft misalignment
- `gear_fault`: Gear mesh issues
- `general_abnormality`: General abnormal vibrations

### Time Features
Statistical features from time-domain signal:
- `mean`: Mean value
- `std`: Standard deviation
- `rms`: Root mean square
- `peak`: Peak amplitude
- `peak_to_peak`: Peak-to-peak amplitude
- `crest_factor`: Peak to RMS ratio
- `kurtosis`: Distribution tailedness
- `skewness`: Distribution asymmetry

### Frequency Features
Features from frequency-domain analysis:
- `peak_frequency`: Dominant frequency (Hz)
- `spectral_power`: Total spectral power
- `frequency_bands`: Power in different frequency ranges
  - `low`: 0-500 Hz
  - `mid`: 500-2000 Hz
  - `high`: 2000-5000 Hz

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages in JSON format:

```json
{
  "error": "Description of the error"
}
```

Common error scenarios:
- **No file uploaded:** Returns 400 with message about missing file
- **Invalid file type:** Returns 400 with list of supported formats
- **File too large:** Returns 400 (max size: 16MB by default)
- **Processing error:** Returns 500 with error details

---

## File Upload Limits

- **Maximum file size:** 16 MB (configurable in `config.py`)
- **Allowed extensions:** .csv, .txt, .xlsx, .xls, .mat

---

## Visualization Format

Visualizations are returned as base64-encoded PNG images. To display them in HTML:

```html
<img src="data:image/png;base64,{base64_string}" alt="Visualization">
```

---

## Example Usage

### Python (using requests)

```python
import requests

# Upload and analyze
url = 'http://localhost:5000/upload'
files = {'file': open('vibration_data.csv', 'rb')}
response = requests.post(url, files=files)

if response.status_code == 200:
    results = response.json()
    print(f"Fault Score: {results['results']['fault_score']}")
    print(f"Damage Level: {results['results']['damage_level']}")
else:
    print(f"Error: {response.json()['error']}")
```

### cURL

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@vibration_data.csv"
```

### JavaScript (Fetch API)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Fault Score:', data.results.fault_score);
    console.log('Damage Level:', data.results.damage_level);
  } else {
    console.error('Error:', data.error);
  }
})
.catch(error => console.error('Error:', error));
```

---

## Configuration

Configuration can be modified in `config.py`:

```python
class Config:
    SECRET_KEY = 'your-secret-key'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx', 'xls', 'mat'}
    SAMPLING_RATE = 12000  # Hz
    FAULT_THRESHOLD = 0.5
```

---

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing rate limiting using Flask-Limiter or similar middleware.

---

## Authentication

The current version does not include authentication. For production use, consider adding:
- API keys
- JWT tokens
- OAuth integration
- Role-based access control

---

## Future Enhancements

Planned API improvements:
- Async processing with job queues
- Batch processing endpoint
- Historical analysis retrieval
- Real-time monitoring WebSocket
- Model training endpoint
- Configuration management API

---

## Support

For API questions or issues:
- Open an issue on GitHub
- Check the main README.md for general information
- Review DEPLOYMENT.md for production setup
