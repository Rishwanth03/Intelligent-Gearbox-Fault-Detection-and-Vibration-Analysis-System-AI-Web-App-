"""
Data preprocessing module for vibration signals
"""

import numpy as np
import pandas as pd
from scipy import signal
import os


class DataPreprocessor:
    """Preprocess vibration data for analysis"""
    
    def __init__(self, sampling_rate=12000):
        self.sampling_rate = sampling_rate
    
    def load_data(self, filepath):
        """
        Load data from various file formats
        
        Args:
            filepath: Path to the data file
            
        Returns:
            numpy array or pandas DataFrame with vibration data
        """
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.csv':
            data = pd.read_csv(filepath)
        elif ext == '.txt':
            data = np.loadtxt(filepath)
        elif ext in ['.xlsx', '.xls']:
            data = pd.read_excel(filepath)
        elif ext == '.mat':
            # For .mat files, would need scipy.io.loadmat
            try:
                from scipy.io import loadmat
                mat_data = loadmat(filepath)
                # Extract first data array found
                for key in mat_data.keys():
                    if not key.startswith('__'):
                        data = mat_data[key]
                        break
            except:
                raise ValueError("Could not load .mat file")
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        return data
    
    def preprocess(self, data):
        """
        Preprocess vibration data
        
        Args:
            data: Raw vibration data
            
        Returns:
            Dictionary with preprocessed data and features
        """
        # Convert to numpy array if needed
        if isinstance(data, pd.DataFrame):
            if data.shape[1] == 1:
                signal_data = data.iloc[:, 0].values
            else:
                # Use first numeric column
                signal_data = data.select_dtypes(include=[np.number]).iloc[:, 0].values
        else:
            signal_data = np.array(data).flatten()
        
        # Remove DC component
        signal_data = signal_data - np.mean(signal_data)
        
        # Apply bandpass filter (typical range for gearbox vibrations: 10-5000 Hz)
        if len(signal_data) > 100:
            nyquist = self.sampling_rate / 2
            low = 10 / nyquist
            high = min(5000 / nyquist, 0.99)
            
            try:
                b, a = signal.butter(4, [low, high], btype='band')
                signal_data = signal.filtfilt(b, a, signal_data)
            except:
                pass  # Skip filtering if it fails
        
        # Compute time-domain features
        time_features = self._extract_time_features(signal_data)
        
        # Compute frequency-domain features
        freq_features = self._extract_frequency_features(signal_data)
        
        return {
            'signal': signal_data,
            'time_features': time_features,
            'freq_features': freq_features,
            'sampling_rate': self.sampling_rate
        }
    
    def _extract_time_features(self, signal_data):
        """Extract time-domain statistical features"""
        return {
            'mean': float(np.mean(signal_data)),
            'std': float(np.std(signal_data)),
            'rms': float(np.sqrt(np.mean(signal_data**2))),
            'peak': float(np.max(np.abs(signal_data))),
            'peak_to_peak': float(np.ptp(signal_data)),
            'crest_factor': float(np.max(np.abs(signal_data)) / np.sqrt(np.mean(signal_data**2))) if np.mean(signal_data**2) > 0 else 0,
            'kurtosis': float(self._kurtosis(signal_data)),
            'skewness': float(self._skewness(signal_data))
        }
    
    def _extract_frequency_features(self, signal_data):
        """Extract frequency-domain features using FFT"""
        # Compute FFT
        fft_vals = np.fft.rfft(signal_data)
        fft_mag = np.abs(fft_vals)
        fft_freq = np.fft.rfftfreq(len(signal_data), 1/self.sampling_rate)
        
        # Find peak frequency
        peak_idx = np.argmax(fft_mag)
        peak_freq = float(fft_freq[peak_idx])
        
        # Compute spectral features
        total_power = np.sum(fft_mag**2)
        
        return {
            'peak_frequency': peak_freq,
            'spectral_power': float(total_power),
            'frequency_bands': self._compute_band_powers(fft_freq, fft_mag)
        }
    
    def _compute_band_powers(self, freq, magnitude):
        """Compute power in different frequency bands"""
        bands = {
            'low': (0, 500),
            'mid': (500, 2000),
            'high': (2000, 5000)
        }
        
        band_powers = {}
        for band_name, (low, high) in bands.items():
            mask = (freq >= low) & (freq < high)
            band_powers[band_name] = float(np.sum(magnitude[mask]**2))
        
        return band_powers
    
    def _kurtosis(self, data):
        """Compute kurtosis (measure of tailedness)"""
        n = len(data)
        if n < 4:
            return 0.0
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * \
               np.sum(((data - mean) / std) ** 4) - \
               (3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))
    
    def _skewness(self, data):
        """Compute skewness (measure of asymmetry)"""
        n = len(data)
        if n < 3:
            return 0.0
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return (n / ((n - 1) * (n - 2))) * np.sum(((data - mean) / std) ** 3)
