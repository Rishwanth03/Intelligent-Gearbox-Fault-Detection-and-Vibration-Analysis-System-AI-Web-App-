"""
Sample data generator for testing the gearbox fault detection system
"""

import numpy as np
import pandas as pd
import os


def generate_healthy_signal(duration=1.0, sampling_rate=12000, save_path=None):
    """
    Generate a healthy gearbox vibration signal
    
    Args:
        duration: Signal duration in seconds
        sampling_rate: Sampling rate in Hz
        save_path: Optional path to save the signal
        
    Returns:
        numpy array with signal data
    """
    t = np.linspace(0, duration, int(duration * sampling_rate))
    
    # Healthy signal: low amplitude, dominated by rotation frequency
    rotation_freq = 30  # Hz (1800 RPM)
    gear_mesh_freq = 360  # Hz (12 teeth gear)
    
    signal = (0.5 * np.sin(2 * np.pi * rotation_freq * t) +
              0.3 * np.sin(2 * np.pi * gear_mesh_freq * t) +
              0.1 * np.random.randn(len(t)))
    
    if save_path:
        df = pd.DataFrame({'vibration': signal})
        df.to_csv(save_path, index=False)
        print(f"Saved healthy signal to {save_path}")
    
    return signal


def generate_faulty_signal(fault_type='bearing', duration=1.0, sampling_rate=12000, save_path=None):
    """
    Generate a faulty gearbox vibration signal
    
    Args:
        fault_type: Type of fault ('bearing', 'unbalance', 'misalignment', 'gear')
        duration: Signal duration in seconds
        sampling_rate: Sampling rate in Hz
        save_path: Optional path to save the signal
        
    Returns:
        numpy array with signal data
    """
    t = np.linspace(0, duration, int(duration * sampling_rate))
    
    rotation_freq = 30  # Hz
    gear_mesh_freq = 360  # Hz
    
    # Base signal
    signal = (0.5 * np.sin(2 * np.pi * rotation_freq * t) +
              0.3 * np.sin(2 * np.pi * gear_mesh_freq * t))
    
    if fault_type == 'bearing':
        # Bearing fault: impulsive impacts at bearing defect frequency
        bearing_defect_freq = 85  # Hz (example BPFO)
        impulse_times = np.arange(0, duration, 1/bearing_defect_freq)
        
        for imp_time in impulse_times:
            idx = int(imp_time * sampling_rate)
            if idx < len(signal):
                # Add impulse with exponential decay
                decay = np.exp(-100 * (t[idx:] - t[idx]))
                signal[idx:] += 5 * decay[:len(signal[idx:])]
    
    elif fault_type == 'unbalance':
        # Unbalance: increased amplitude at rotation frequency
        signal += 2.0 * np.sin(2 * np.pi * rotation_freq * t)
    
    elif fault_type == 'misalignment':
        # Misalignment: increased harmonics
        signal += (1.0 * np.sin(2 * np.pi * 2 * rotation_freq * t) +
                  0.8 * np.sin(2 * np.pi * 3 * rotation_freq * t))
    
    elif fault_type == 'gear':
        # Gear fault: modulation in gear mesh frequency
        modulation_freq = 5  # Hz
        signal += 1.5 * np.sin(2 * np.pi * gear_mesh_freq * t) * \
                  (1 + 0.5 * np.sin(2 * np.pi * modulation_freq * t))
    
    # Add noise
    signal += 0.3 * np.random.randn(len(t))
    
    if save_path:
        df = pd.DataFrame({'vibration': signal})
        df.to_csv(save_path, index=False)
        print(f"Saved {fault_type} fault signal to {save_path}")
    
    return signal


def generate_sample_dataset():
    """Generate a set of sample signals for testing"""
    
    # Create samples directory
    samples_dir = 'data/samples'
    os.makedirs(samples_dir, exist_ok=True)
    
    print("Generating sample vibration data...")
    
    # Generate healthy signal
    generate_healthy_signal(duration=2.0, 
                           save_path=os.path.join(samples_dir, 'healthy_signal.csv'))
    
    # Generate faulty signals
    fault_types = ['bearing', 'unbalance', 'misalignment', 'gear']
    for fault in fault_types:
        generate_faulty_signal(fault_type=fault, 
                              duration=2.0,
                              save_path=os.path.join(samples_dir, f'{fault}_fault_signal.csv'))
    
    print(f"\nSample data generated in '{samples_dir}' directory")
    print("You can use these files to test the application!")


if __name__ == '__main__':
    generate_sample_dataset()
