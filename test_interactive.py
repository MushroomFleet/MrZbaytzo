#!/usr/bin/env python3
"""
Test script to verify interactive mode preset switching functionality
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from main_rev2 import ZPaytzoEngineRev2


def test_interactive_preset_switching():
    """Test that interactive mode can switch presets correctly."""
    print("Testing Interactive Mode Preset Switching")
    print("=" * 45)
    
    try:
        # Initialize engine with authentic_1986 preset
        print("1. Initializing with authentic_1986 preset...")
        engine = ZPaytzoEngineRev2(preset='authentic_1986')
        
        # Verify initial preset
        initial_preset = engine.get_current_preset()
        initial_quality = engine.get_quality_info()
        print(f"   Initial preset: {initial_preset}")
        print(f"   Initial quality: {initial_quality['quality_level']}")
        print(f"   Initial bit depth: {initial_quality['bit_depth']}")
        
        # Test preset switching
        print("\n2. Testing preset switching...")
        
        # Switch to enhanced_vintage
        print("   Switching to enhanced_vintage...")
        success = engine.set_preset('enhanced_vintage')
        if success:
            current_preset = engine.get_current_preset()
            current_quality = engine.get_quality_info()
            print(f"   ✓ Switched to: {current_preset}")
            print(f"   ✓ Quality level: {current_quality['quality_level']}")
            print(f"   ✓ Bit depth: {current_quality['bit_depth']}")
        else:
            print("   ✗ Failed to switch to enhanced_vintage")
            return False
        
        # Switch to modern_retro
        print("   Switching to modern_retro...")
        success = engine.set_preset('modern_retro')
        if success:
            current_preset = engine.get_current_preset()
            current_quality = engine.get_quality_info()
            print(f"   ✓ Switched to: {current_preset}")
            print(f"   ✓ Quality level: {current_quality['quality_level']}")
            print(f"   ✓ Bit depth: {current_quality['bit_depth']}")
        else:
            print("   ✗ Failed to switch to modern_retro")
            return False
        
        # Switch back to authentic_1986
        print("   Switching back to authentic_1986...")
        success = engine.set_preset('authentic_1986')
        if success:
            current_preset = engine.get_current_preset()
            current_quality = engine.get_quality_info()
            print(f"   ✓ Switched to: {current_preset}")
            print(f"   ✓ Quality level: {current_quality['quality_level']}")
            print(f"   ✓ Bit depth: {current_quality['bit_depth']}")
        else:
            print("   ✗ Failed to switch back to authentic_1986")
            return False
        
        # Test list presets functionality
        print("\n3. Testing preset listing...")
        presets = engine.config_manager.list_presets()
        print(f"   Available presets: {len(presets)}")
        for preset in presets:
            current_marker = " (current)" if preset['name'] == engine.get_current_preset() else ""
            print(f"   - {preset['display_name']}{current_marker}")
        
        # Test audio padding configuration updates
        print("\n4. Testing audio padding updates...")
        for preset_name in ['authentic_1986', 'enhanced_vintage', 'modern_retro']:
            engine.set_preset(preset_name)
            padding_info = engine.audio_output.get_padding_info()
            print(f"   {preset_name}:")
            print(f"     Start silence: {padding_info['start_silence_ms']}ms")
            print(f"     End silence: {padding_info['end_silence_ms']}ms")
            print(f"     Total padding: {padding_info['total_padding_ms']}ms")
        
        print("\n✓ All interactive mode tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Interactive mode test failed: {e}")
        return False


def test_interactive_commands():
    """Test that interactive commands are properly implemented."""
    print("\nTesting Interactive Commands")
    print("=" * 30)
    
    try:
        engine = ZPaytzoEngineRev2(preset='enhanced_vintage')
        
        # Test config display
        print("1. Testing config display...")
        engine.print_config()
        
        # Test preset listing
        print("\n2. Testing preset listing...")
        engine.list_presets()
        
        # Test speech synthesis with different presets
        print("\n3. Testing speech synthesis with preset switching...")
        test_text = "Testing preset switching"
        
        for preset in ['authentic_1986', 'enhanced_vintage', 'modern_retro']:
            print(f"   Testing with {preset}...")
            engine.set_preset(preset)
            
            # Get audio timing info
            normalized_text = engine.text_processor.normalize(test_text)
            phonemes = engine.phoneme_converter.convert(normalized_text)
            raw_audio = engine.synthesizer.synthesize(phonemes)
            processed_audio = engine.vintage_dsp.process(raw_audio)
            timing_info = engine.audio_output.analyze_audio_timing(processed_audio)
            
            print(f"     Original duration: {timing_info['original_duration_ms']:.1f}ms")
            print(f"     With padding: {timing_info['enhanced_duration_ms']:.1f}ms")
            print(f"     Added padding: {timing_info['added_padding_ms']:.1f}ms")
        
        print("\n✓ Interactive commands test passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Interactive commands test failed: {e}")
        return False


def main():
    """Run all interactive mode tests."""
    print("MR.ZPAYTZO-rev2 Interactive Mode Test Suite")
    print("=" * 50)
    
    success = True
    
    # Test 1: Preset switching
    if not test_interactive_preset_switching():
        success = False
    
    # Test 2: Interactive commands
    if not test_interactive_commands():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All interactive mode tests passed!")
        print("Interactive mode is fully functional with preset support.")
    else:
        print("❌ Some interactive mode tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
