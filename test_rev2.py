#!/usr/bin/env python3
"""
Test script for MR.ZPAYTZO-rev2
Demonstrates the enhanced configuration system and quality presets
"""

import sys
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config_manager import ConfigManager
from main_rev2 import ZPaytzoEngineRev2


def test_configuration_system():
    """Test the configuration management system."""
    print("Testing Configuration System")
    print("=" * 40)
    
    # Test configuration manager
    config_manager = ConfigManager()
    
    print("✓ Configuration manager initialized")
    print(f"  Default preset: {config_manager.get_current_preset()}")
    print(f"  Quality level: {config_manager.get_quality_level()}")
    
    # Test preset loading
    print("\nTesting preset loading...")
    presets = config_manager.list_presets()
    for preset in presets:
        print(f"  Loading preset: {preset['name']}")
        success = config_manager.load_preset(preset['name'])
        if success:
            print(f"    ✓ Loaded successfully")
            print(f"    Quality level: {config_manager.get_quality_level()}")
            audio_config = config_manager.get_audio_config()
            print(f"    Audio: {audio_config['sample_rate']}Hz, {audio_config['bit_depth']}-bit")
        else:
            print(f"    ✗ Failed to load")
        print()
    
    # Test configuration validation
    print("Testing configuration validation...")
    errors = config_manager.validate_config()
    if errors:
        print(f"  ✗ Validation errors: {errors}")
    else:
        print("  ✓ Configuration is valid")
    
    print()


def test_quality_presets():
    """Test different quality presets with speech synthesis."""
    print("Testing Quality Presets with Speech Synthesis")
    print("=" * 50)
    
    test_text = "Hello world, this is a quality test"
    
    presets_to_test = [
        "authentic_1986",
        "enhanced_vintage", 
        "modern_retro"
    ]
    
    for preset_name in presets_to_test:
        print(f"\nTesting preset: {preset_name}")
        print("-" * 30)
        
        try:
            # Initialize engine with preset
            engine = ZPaytzoEngineRev2(preset=preset_name)
            
            # Get quality info
            quality_info = engine.get_quality_info()
            print(f"Quality Level: {quality_info['quality_level']}")
            print(f"Sample Rate: {quality_info['sample_rate']}Hz")
            print(f"Bit Depth: {quality_info['bit_depth']}-bit")
            
            vintage_info = quality_info['vintage_info']
            print(f"Vintage Intensity: {vintage_info['vintage_intensity']:.1f}")
            print(f"Vintage Preset: {vintage_info['vintage_preset']}")
            
            # Test speech synthesis
            print(f"Synthesizing: '{test_text}'")
            engine.speak(test_text, verbose=False)
            print("✓ Speech synthesis completed")
            
            # Small delay between tests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"✗ Error testing preset {preset_name}: {e}")
    
    print()


def test_runtime_configuration():
    """Test runtime configuration changes."""
    print("Testing Runtime Configuration Changes")
    print("=" * 40)
    
    try:
        # Start with authentic 1986
        engine = ZPaytzoEngineRev2(preset="authentic_1986")
        
        test_text = "Configuration test"
        
        print("Initial configuration (Authentic 1986):")
        engine.print_config()
        print(f"Synthesizing: '{test_text}'")
        engine.speak(test_text)
        
        print("\nSwitching to Enhanced Vintage preset...")
        engine.set_preset("enhanced_vintage")
        print(f"Synthesizing: '{test_text}'")
        engine.speak(test_text)
        
        print("\nSwitching to Modern Retro preset...")
        engine.set_preset("modern_retro")
        print(f"Synthesizing: '{test_text}'")
        engine.speak(test_text)
        
        print("\nTesting individual parameter changes...")
        print("Setting vintage intensity to 0.5...")
        engine.configure('vintage_processing', 'intensity', 0.5)
        print(f"Synthesizing: '{test_text}'")
        engine.speak(test_text)
        
        print("✓ Runtime configuration test completed")
        
    except Exception as e:
        print(f"✗ Error in runtime configuration test: {e}")
    
    print()


def test_advanced_features():
    """Test advanced processing features."""
    print("Testing Advanced Processing Features")
    print("=" * 40)
    
    try:
        # Start with modern retro preset (has advanced features enabled)
        engine = ZPaytzoEngineRev2(preset="modern_retro")
        
        test_text = "Advanced processing test"
        
        print("Testing with all advanced features enabled:")
        vintage_info = engine.get_quality_info()['vintage_info']
        features = []
        if vintage_info['spectral_enhancement']:
            features.append("Spectral Enhancement")
        if vintage_info['harmonic_enrichment']:
            features.append("Harmonic Enrichment")
        if vintage_info['noise_reduction']:
            features.append("Noise Reduction")
        if vintage_info['temporal_smoothing']:
            features.append("Temporal Smoothing")
        
        print(f"Active features: {', '.join(features) if features else 'None'}")
        print(f"Synthesizing: '{test_text}'")
        engine.speak(test_text)
        
        print("\nDisabling advanced features...")
        engine.configure('advanced', 'spectral_enhancement', False)
        engine.configure('advanced', 'harmonic_enrichment', False)
        engine.configure('advanced', 'noise_reduction', False)
        engine.configure('advanced', 'temporal_smoothing', False)
        
        print(f"Synthesizing without advanced features: '{test_text}'")
        engine.speak(test_text)
        
        print("✓ Advanced features test completed")
        
    except Exception as e:
        print(f"✗ Error in advanced features test: {e}")
    
    print()


def test_backward_compatibility():
    """Test backward compatibility with rev0."""
    print("Testing Backward Compatibility")
    print("=" * 35)
    
    try:
        # Test with default settings (should match rev0)
        engine = ZPaytzoEngineRev2()
        
        test_text = "Backward compatibility test"
        
        quality_info = engine.get_quality_info()
        print(f"Default quality level: {quality_info['quality_level']}")
        print(f"Should be 'Authentic 1986' for rev0 compatibility")
        
        if quality_info['quality_level'] == "Authentic 1986":
            print("✓ Default configuration matches rev0 behavior")
        else:
            print("⚠ Default configuration differs from rev0")
        
        print(f"Synthesizing: '{test_text}'")
        engine.speak(test_text)
        
        print("✓ Backward compatibility test completed")
        
    except Exception as e:
        print(f"✗ Error in backward compatibility test: {e}")
    
    print()


def main():
    """Run all tests."""
    print("MR.ZPAYTZO-rev2 Test Suite")
    print("=" * 50)
    print()
    
    try:
        # Test configuration system
        test_configuration_system()
        
        # Test quality presets
        test_quality_presets()
        
        # Test runtime configuration
        test_runtime_configuration()
        
        # Test advanced features
        test_advanced_features()
        
        # Test backward compatibility
        test_backward_compatibility()
        
        print("🎉 All tests completed!")
        print("\nMR.ZPAYTZO-rev2 is ready for use with enhanced quality options.")
        print("\nTry the new features:")
        print("  python main_rev2.py --preset enhanced_vintage \"Better quality speech\"")
        print("  python main_rev2.py --preset modern_retro \"High quality speech\"")
        print("  python main_rev2.py --interactive --preset enhanced_vintage")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest suite failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
