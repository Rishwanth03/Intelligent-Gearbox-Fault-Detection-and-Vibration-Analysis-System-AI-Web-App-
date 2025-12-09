import os

class Config:
    """Application configuration settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx', 'xls', 'mat'}
    
    # Model settings
    MODEL_FOLDER = 'models'
    
    # Data settings
    DATA_FOLDER = 'data'
    
    # Analysis settings
    SAMPLING_RATE = 12000  # Default sampling rate in Hz
    FAULT_THRESHOLD = 0.5  # Threshold for fault detection
    
    # Damage levels
    DAMAGE_LEVELS = {
        'healthy': (0.0, 0.2),
        'slight': (0.2, 0.4),
        'moderate': (0.4, 0.6),
        'severe': (0.6, 0.8),
        'critical': (0.8, 1.0)
    }
