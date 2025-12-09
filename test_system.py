"""
Simple tests for the gearbox fault detection system
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.preprocessor import DataPreprocessor
from backend.analyzer import VibrationAnalyzer


def test_preprocessor():
    """Test data preprocessing functionality"""
    print("Testing DataPreprocessor...")
    
    # Create sample signal
    t = np.linspace(0, 1, 12000)
    signal = np.sin(2 * np.pi * 50 * t) + 0.1 * np.random.randn(len(t))
    
    preprocessor = DataPreprocessor(sampling_rate=12000)
    processed = preprocessor.preprocess(signal)
    
    # Check that required keys are present
    assert 'signal' in processed, "Missing 'signal' key"
    assert 'time_features' in processed, "Missing 'time_features' key"
    assert 'freq_features' in processed, "Missing 'freq_features' key"
    
    # Check time features
    time_features = processed['time_features']
    required_time_features = ['mean', 'std', 'rms', 'peak', 'crest_factor', 'kurtosis']
    for feat in required_time_features:
        assert feat in time_features, f"Missing time feature: {feat}"
    
    # Check frequency features
    freq_features = processed['freq_features']
    assert 'peak_frequency' in freq_features, "Missing peak_frequency"
    assert 'spectral_power' in freq_features, "Missing spectral_power"
    
    print("✓ DataPreprocessor tests passed")
    return processed


def test_analyzer(processed_data):
    """Test fault detection and analysis"""
    print("\nTesting VibrationAnalyzer...")
    
    analyzer = VibrationAnalyzer()
    results = analyzer.analyze(processed_data)
    
    # Check required result keys
    required_keys = ['fault_score', 'damage_level', 'is_faulty', 
                    'fault_types', 'recommendations']
    for key in required_keys:
        assert key in results, f"Missing result key: {key}"
    
    # Check damage level is valid
    valid_levels = ['healthy', 'slight', 'moderate', 'severe', 'critical']
    assert results['damage_level'] in valid_levels, \
        f"Invalid damage level: {results['damage_level']}"
    
    # Check fault score is in valid range
    assert 0 <= results['fault_score'] <= 1, \
        f"Invalid fault score: {results['fault_score']}"
    
    # Check recommendations is a list
    assert isinstance(results['recommendations'], list), \
        "Recommendations should be a list"
    
    print("✓ VibrationAnalyzer tests passed")
    print(f"\n  Fault Score: {results['fault_score']:.3f}")
    print(f"  Damage Level: {results['damage_level']}")
    print(f"  Is Faulty: {results['is_faulty']}")
    
    return results


def test_sample_generation():
    """Test sample data generation"""
    print("\nTesting sample data generation...")
    
    try:
        from generate_sample_data import generate_healthy_signal, generate_faulty_signal
        
        # Generate signals without saving
        healthy = generate_healthy_signal(duration=0.5)
        faulty = generate_faulty_signal(fault_type='bearing', duration=0.5)
        
        assert len(healthy) > 0, "Healthy signal generation failed"
        assert len(faulty) > 0, "Faulty signal generation failed"
        
        print("✓ Sample data generation tests passed")
        return True
    except Exception as e:
        print(f"✗ Sample data generation test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Gearbox Fault Detection System Tests")
    print("=" * 60)
    
    try:
        # Test preprocessing
        processed_data = test_preprocessor()
        
        # Test analysis
        results = test_analyzer(processed_data)
        
        # Test sample generation
        test_sample_generation()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
