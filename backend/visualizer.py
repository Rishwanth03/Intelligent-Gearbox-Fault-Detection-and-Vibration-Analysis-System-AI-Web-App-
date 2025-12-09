"""
Visualization module for creating plots and charts
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from scipy import signal as scipy_signal


def create_visualizations(processed_data, analysis_results):
    """
    Create visualizations for vibration analysis results
    
    Args:
        processed_data: Dictionary with preprocessed data
        analysis_results: Dictionary with analysis results
        
    Returns:
        Dictionary with base64-encoded images
    """
    signal_data = processed_data['signal']
    sampling_rate = processed_data['sampling_rate']
    
    visualizations = {}
    
    # Time-domain plot
    visualizations['time_domain'] = create_time_domain_plot(signal_data, sampling_rate)
    
    # Frequency-domain plot (FFT)
    visualizations['frequency_domain'] = create_frequency_domain_plot(signal_data, sampling_rate)
    
    # Spectrogram
    visualizations['spectrogram'] = create_spectrogram(signal_data, sampling_rate)
    
    # Feature comparison chart
    visualizations['features'] = create_feature_chart(processed_data['time_features'])
    
    return visualizations


def create_time_domain_plot(signal_data, sampling_rate):
    """Create time-domain signal plot"""
    plt.figure(figsize=(12, 4))
    
    # Limit to first 10000 points for visualization
    max_points = min(10000, len(signal_data))
    time = np.arange(max_points) / sampling_rate
    
    plt.plot(time, signal_data[:max_points], 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Vibration Signal - Time Domain')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig_to_base64(plt.gcf())


def create_frequency_domain_plot(signal_data, sampling_rate):
    """Create frequency-domain plot (FFT)"""
    plt.figure(figsize=(12, 4))
    
    # Compute FFT
    fft_vals = np.fft.rfft(signal_data)
    fft_mag = np.abs(fft_vals)
    fft_freq = np.fft.rfftfreq(len(signal_data), 1/sampling_rate)
    
    # Plot only up to 5000 Hz (typical range for gearbox)
    max_freq_idx = np.where(fft_freq <= 5000)[0]
    if len(max_freq_idx) > 0:
        max_idx = max_freq_idx[-1]
    else:
        max_idx = len(fft_freq)
    
    plt.plot(fft_freq[:max_idx], fft_mag[:max_idx], 'r-', linewidth=0.8)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Vibration Signal - Frequency Domain (FFT)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig_to_base64(plt.gcf())


def create_spectrogram(signal_data, sampling_rate):
    """Create spectrogram plot"""
    plt.figure(figsize=(12, 5))
    
    # Compute spectrogram
    f, t, Sxx = scipy_signal.spectrogram(signal_data, sampling_rate, 
                                         nperseg=min(1024, len(signal_data)//4))
    
    # Plot spectrogram
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.title('Spectrogram - Time-Frequency Analysis')
    plt.colorbar(label='Power (dB)')
    plt.ylim([0, min(5000, sampling_rate/2)])
    plt.tight_layout()
    
    return fig_to_base64(plt.gcf())


def create_feature_chart(time_features):
    """Create bar chart of time-domain features"""
    plt.figure(figsize=(10, 5))
    
    # Select features to display
    features = {
        'RMS': time_features['rms'],
        'Peak': time_features['peak'],
        'Crest Factor': time_features['crest_factor'],
        'Kurtosis': abs(time_features['kurtosis']),
        'Std Dev': time_features['std']
    }
    
    # Normalize for display
    max_val = max(features.values())
    if max_val > 0:
        normalized_features = {k: v/max_val for k, v in features.items()}
    else:
        normalized_features = features
    
    plt.bar(normalized_features.keys(), normalized_features.values(), color='steelblue')
    plt.xlabel('Feature')
    plt.ylabel('Normalized Value')
    plt.title('Time-Domain Features (Normalized)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    return fig_to_base64(plt.gcf())


def fig_to_base64(fig):
    """Convert matplotlib figure to base64-encoded string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64
