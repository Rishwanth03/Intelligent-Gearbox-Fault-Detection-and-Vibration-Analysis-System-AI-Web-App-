"""
Vibration analysis and fault detection module
"""

import numpy as np
from config import Config


class VibrationAnalyzer:
    """Analyze vibration data to detect faults and assess damage levels"""
    
    def __init__(self):
        self.config = Config()
        self.fault_threshold = self.config.FAULT_THRESHOLD
        self.damage_levels = self.config.DAMAGE_LEVELS
    
    def analyze(self, processed_data):
        """
        Analyze processed vibration data for faults
        
        Args:
            processed_data: Dictionary with preprocessed signal and features
            
        Returns:
            Dictionary with analysis results
        """
        time_features = processed_data['time_features']
        freq_features = processed_data['freq_features']
        
        # Calculate fault indicators
        fault_score = self._calculate_fault_score(time_features, freq_features)
        
        # Determine damage level
        damage_level = self._classify_damage_level(fault_score)
        
        # Detect specific fault types
        fault_types = self._detect_fault_types(time_features, freq_features)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(damage_level, fault_types)
        
        return {
            'fault_score': float(fault_score),
            'damage_level': damage_level,
            'is_faulty': bool(fault_score > self.fault_threshold),
            'fault_types': fault_types,
            'recommendations': recommendations,
            'time_features': time_features,
            'freq_features': freq_features
        }
    
    def _calculate_fault_score(self, time_features, freq_features):
        """
        Calculate overall fault score based on features
        
        Higher values indicate more severe faults
        """
        # Normalize features and compute weighted score
        # These weights are example values - in practice, would be learned from data
        
        # High RMS indicates high vibration energy
        rms_score = min(time_features['rms'] / 10.0, 1.0)
        
        # High kurtosis indicates impulsive behavior (common in bearing faults)
        kurtosis_score = min(abs(time_features['kurtosis']) / 10.0, 1.0)
        
        # High crest factor indicates impact/shock
        crest_score = min(time_features['crest_factor'] / 10.0, 1.0)
        
        # Imbalance in frequency bands can indicate issues
        band_powers = freq_features['frequency_bands']
        total_band_power = sum(band_powers.values())
        if total_band_power > 0:
            band_imbalance = np.std(list(band_powers.values())) / (total_band_power / 3)
        else:
            band_imbalance = 0
        band_score = min(band_imbalance, 1.0)
        
        # Weighted combination
        fault_score = (0.3 * rms_score + 
                      0.3 * kurtosis_score + 
                      0.2 * crest_score + 
                      0.2 * band_score)
        
        return min(fault_score, 1.0)
    
    def _classify_damage_level(self, fault_score):
        """Classify damage level based on fault score"""
        for level, (low, high) in self.damage_levels.items():
            if low <= fault_score < high:
                return level
        return 'critical'  # Default to critical if score is 1.0
    
    def _detect_fault_types(self, time_features, freq_features):
        """
        Detect specific types of faults
        
        Returns list of detected fault types
        """
        faults = []
        
        # Bearing fault detection (high kurtosis, impulsive)
        if time_features['kurtosis'] > 5:
            faults.append({
                'type': 'bearing_fault',
                'confidence': min(time_features['kurtosis'] / 10.0, 1.0),
                'description': 'Possible bearing defect detected'
            })
        
        # Unbalance detection (dominant low frequency)
        if freq_features['peak_frequency'] < 100:
            faults.append({
                'type': 'unbalance',
                'confidence': 0.6,
                'description': 'Possible rotor unbalance detected'
            })
        
        # Misalignment detection (high harmonics)
        band_powers = freq_features['frequency_bands']
        if band_powers['high'] > band_powers['low'] * 0.5:
            faults.append({
                'type': 'misalignment',
                'confidence': 0.5,
                'description': 'Possible shaft misalignment detected'
            })
        
        # Gear fault detection (modulation in mid frequencies)
        if 500 < freq_features['peak_frequency'] < 2000:
            faults.append({
                'type': 'gear_fault',
                'confidence': 0.6,
                'description': 'Possible gear mesh fault detected'
            })
        
        # If no specific faults detected but score is high
        if not faults and time_features['rms'] > 5:
            faults.append({
                'type': 'general_abnormality',
                'confidence': 0.5,
                'description': 'Abnormal vibration levels detected'
            })
        
        return faults
    
    def _generate_recommendations(self, damage_level, fault_types):
        """Generate maintenance recommendations based on analysis"""
        recommendations = []
        
        # Level-based recommendations
        if damage_level == 'healthy':
            recommendations.append("System is operating normally. Continue routine monitoring.")
        elif damage_level == 'slight':
            recommendations.append("Minor abnormalities detected. Increase monitoring frequency.")
        elif damage_level == 'moderate':
            recommendations.append("Moderate wear detected. Schedule inspection within 2-4 weeks.")
        elif damage_level == 'severe':
            recommendations.append("Severe damage detected. Schedule immediate inspection.")
            recommendations.append("Consider reducing operational load until maintenance.")
        elif damage_level == 'critical':
            recommendations.append("CRITICAL: Shutdown recommended to prevent catastrophic failure.")
            recommendations.append("Immediate maintenance required.")
        
        # Fault-specific recommendations
        for fault in fault_types:
            if fault['type'] == 'bearing_fault':
                recommendations.append("Inspect bearings for wear, contamination, or lubrication issues.")
            elif fault['type'] == 'unbalance':
                recommendations.append("Check rotor balance and perform balancing if necessary.")
            elif fault['type'] == 'misalignment':
                recommendations.append("Check shaft alignment and realign if necessary.")
            elif fault['type'] == 'gear_fault':
                recommendations.append("Inspect gear teeth for wear, pitting, or damage.")
        
        return recommendations
