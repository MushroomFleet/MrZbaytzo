#!/usr/bin/env python3
"""
Audio Padding Test for MR.ZPAYTZO-rev2
Tests the enhanced audio output with padding to verify clipping is resolved
"""

import numpy as np
import sys
from src.config_manager import ConfigManager
from src.enhanced_audio_output import EnhancedAudioOutput
from main_rev2 import ZPaytzoEngineRev2


def test_audio_padding():
    """Test audio padding functionality."""
    print("Testing Enhanced Audio Output with Padding")
    print("=" * 50)
    
    # Test different quality presets
    presets = ['authentic_1986', 'enhanced_vintage', 'modern_retro']
    
    for preset in presets:
        print(f"\nTesting {preset} preset:")
        print("-" * 30)
        
        try:
            # Initialize engine with preset
            engine = ZPaytzoEngineRev2(preset=preset)
            
            # Get padding info
            padding_info = engine.audio_output.get_padding_info()
            print(f"Padding configuration:")
            print(f"  Start silence: {padding_info['start_silence_ms']}ms")
            print(f"  End silence: {padding_info['end_silence_ms']}ms")
            print(f"  Fade in: {padding_info['fade_in_ms']}ms")
            print(f"  Fade out: {padding_info['fade_out_ms']}ms")
            print(f"  Total padding: {padding_info['total_padding_ms']}ms")
            
            # Test with short phrase
            test_text = "Hello world"
            print(f"\nSynthesizing: '{test_text}'")
            
            # Analyze timing
            # First get raw audio without padding
            normalized_text = engine.text_processor.normalize(test_text)
            phonemes = engine.phoneme_converter.convert(normalized_text)
            raw_audio = engine.synthesizer.synthesize(phonemes)
            processed_audio = engine.vintage_dsp.process(raw_audio)
            
            # Analyze timing with padding
            timing_info = engine.audio_output.analyze_audio_timing(processed_audio)
            print(f"Audio timing analysis:")
            print(f"  Original duration: {timing_info['original_duration_ms']:.1f}ms")
            print(f"  Enhanced duration: {timing_info['enhanced_duration_ms']:.1f}ms")
            print(f"  Added padding: {timing_info['added_padding_ms']:.1f}ms")
            
            # Test actual playback
            print("Playing audio with padding...")
            engine.speak(test_text)
            
            print(f"✓ {preset} test completed successfully")
            
        except Exception as e:
            print(f"✗ {preset} test failed: {e}")
    
    print(f"\n" + "=" * 50)
    print("Audio padding tests completed!")


def test_padding_audio_output_directly():
    """Test the enhanced audio output directly."""
    print("\nDirect Enhanced Audio Output Test")
    print("=" * 40)
    
    # Test with different padding configurations
    padding_configs = [
        {
            'name': 'Minimal Padding',
            'config': {
                'start_silence_ms': 50,
                'end_silence_ms': 100,
                'fade_in_ms': 5,
                'fade_out_ms': 10
            }
        },
        {
            'name': 'Standard Padding',
            'config': {
                'start_silence_ms': 150,
                'end_silence_ms': 250,
                'fade_in_ms': 25,
                'fade_out_ms': 50
            }
        },
        {
            'name': 'Extended Padding',
            'config': {
                'start_silence_ms': 300,
                'end_silence_ms': 500,
                'fade_in_ms': 75,
                'fade_out_ms': 100
            }
        }
    ]
    
    for test_case in padding_configs:
        print(f"\nTesting {test_case['name']}:")
        print("-" * 25)
        
        try:
            # Create enhanced audio output with specific padding
            audio_output = EnhancedAudioOutput(
                sample_rate=22050,
                channels=1,
                padding_config=test_case['config']
            )
            
            # Test with a simple tone
            print("Testing with 440Hz tone...")
            audio_output.test_padding_audio_output(frequency=440.0, duration=0.3)
            
            print(f"✓ {test_case['name']} test completed")
            
        except Exception as e:
            print(f"✗ {test_case['name']} test failed: {e}")


def test_latency_measurement():
    """Test audio latency measurement."""
    print("\nAudio Latency Measurement Test")
    print("=" * 35)
    
    try:
        # Create enhanced audio output
        audio_output = EnhancedAudioOutput(sample_rate=22050, channels=1)
        
        # Measure latency
        latency_info = audio_output.measure_device_latency()
        
        print("Latency breakdown:")
        print(f"  Device latency: {latency_info['device_latency_ms']:.1f}ms")
        print(f"  Buffer latency: {latency_info['buffer_latency_ms']:.1f}ms")
        print(f"  Padding latency: {latency_info['padding_latency_ms']:.1f}ms")
        print(f"  Total latency: {latency_info['total_latency_ms']:.1f}ms")
        
        print("✓ Latency measurement completed")
        
    except Exception as e:
        print(f"✗ Latency measurement failed: {e}")


def test_clipping_prevention():
    """Test that audio clipping is prevented."""
    print("\nAudio Clipping Prevention Test")
    print("=" * 35)
    
    try:
        # Create engine with authentic 1986 preset (most likely to clip)
        engine = ZPaytzoEngineRev2(preset='authentic_1986')
        
        # Test phrases that might cause clipping
        test_phrases = [
            "Hello world",
            "Testing one two three",
            "Dr. Smith's computer",
            "The quick brown fox jumps",
            "Can't you see it's working?"
        ]
        
        for phrase in test_phrases:
            print(f"Testing: '{phrase}'")
            
            # Generate audio
            normalized_text = engine.text_processor.normalize(phrase)
            phonemes = engine.phoneme_converter.convert(normalized_text)
            raw_audio = engine.synthesizer.synthesize(phonemes)
            processed_audio = engine.vintage_dsp.process(raw_audio)
            
            # Apply enhanced processing
            enhanced_audio = engine.audio_output._apply_enhanced_processing(processed_audio)
            
            # Check for clipping (values outside -1 to 1 range)
            max_val = np.max(np.abs(enhanced_audio))
            if max_val > 1.0:
                print(f"  ⚠ Potential clipping detected: max value {max_val:.3f}")
            else:
                print(f"  ✓ No clipping: max value {max_val:.3f}")
            
            # Check fade effectiveness
            fade_in_samples = int(engine.audio_output.padding_config['fade_in_ms'] * 22050 / 1000)
            fade_out_samples = int(engine.audio_output.padding_config['fade_out_ms'] * 22050 / 1000)
            
            if len(enhanced_audio) > fade_in_samples:
                start_level = np.abs(enhanced_audio[0])
                fade_level = np.abs(enhanced_audio[fade_in_samples // 2])
                if start_level < fade_level:
                    print(f"  ✓ Fade-in working: {start_level:.3f} -> {fade_level:.3f}")
                else:
                    print(f"  ⚠ Fade-in issue: {start_level:.3f} -> {fade_level:.3f}")
            
            if len(enhanced_audio) > fade_out_samples:
                end_level = np.abs(enhanced_audio[-1])
                fade_level = np.abs(enhanced_audio[-fade_out_samples // 2])
                if end_level < fade_level:
                    print(f"  ✓ Fade-out working: {fade_level:.3f} -> {end_level:.3f}")
                else:
                    print(f"  ⚠ Fade-out issue: {fade_level:.3f} -> {end_level:.3f}")
        
        print("✓ Clipping prevention test completed")
        
    except Exception as e:
        print(f"✗ Clipping prevention test failed: {e}")


def main():
    """Run all audio padding tests."""
    print("MR.ZPAYTZO-rev2 Audio Padding Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Basic padding functionality
        test_audio_padding()
        
        # Test 2: Direct audio output testing
        test_padding_audio_output_directly()
        
        # Test 3: Latency measurement
        test_latency_measurement()
        
        # Test 4: Clipping prevention
        test_clipping_prevention()
        
        print("\n" + "=" * 60)
        print("🎉 All audio padding tests completed!")
        print("The enhanced audio output should prevent clipping issues.")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
