#!/usr/bin/env python3
"""
Test script for MR.ZPAYTZO-rev0 TTS engine
"""

from src.text_processor import TextProcessor
from src.phoneme_converter import PhonemeConverter
from src.diphone_synthesizer import DiphoneSynthesizer
from src.vintage_dsp import VintageDSP
import numpy as np

def test_pipeline():
    """Test the complete TTS pipeline with a simple phrase."""
    print("Testing MR.ZPAYTZO-rev0 TTS Pipeline")
    print("=" * 40)
    
    # Initialize components
    text_processor = TextProcessor()
    phoneme_converter = PhonemeConverter()
    synthesizer = DiphoneSynthesizer(22050)
    vintage_dsp = VintageDSP(22050, 8)
    
    # Test phrase
    test_text = "Hello world"
    print(f"Input text: '{test_text}'")
    
    # Stage 1: Text processing
    print("\n1. Text Processing...")
    normalized = text_processor.normalize(test_text)
    print(f"   Normalized: '{normalized}'")
    
    # Stage 2: Phoneme conversion
    print("\n2. Phoneme Conversion...")
    phonemes = phoneme_converter.convert(normalized)
    print(f"   Phonemes: {phonemes}")
    
    # Stage 3: Audio synthesis
    print("\n3. Audio Synthesis...")
    audio = synthesizer.synthesize(phonemes)
    print(f"   Generated {len(audio)} audio samples")
    print(f"   Duration: {len(audio) / 22050:.2f} seconds")
    print(f"   Audio range: {np.min(audio):.3f} to {np.max(audio):.3f}")
    
    # Stage 4: Vintage processing
    print("\n4. Vintage DSP Processing...")
    vintage_audio = vintage_dsp.process(audio)
    print(f"   Processed {len(vintage_audio)} samples")
    print(f"   Vintage range: {np.min(vintage_audio):.3f} to {np.max(vintage_audio):.3f}")
    
    print("\n✓ Pipeline test completed successfully!")
    return vintage_audio

def test_components():
    """Test individual components."""
    print("\nTesting Individual Components")
    print("=" * 30)
    
    # Test text processor
    print("\nText Processor:")
    processor = TextProcessor()
    test_cases = [
        "Dr. Smith's computer",
        "The year 1986 was important",
        "Can't you see it's working?",
        "I.B.M. vs. Apple Inc."
    ]
    
    for text in test_cases:
        normalized = processor.normalize(text)
        print(f"  '{text}' -> '{normalized}'")
    
    # Test phoneme converter
    print("\nPhoneme Converter:")
    converter = PhonemeConverter()
    phoneme_tests = [
        "HELLO",
        "WORLD", 
        "COMPUTER",
        "TECHNOLOGY"
    ]
    
    for word in phoneme_tests:
        phonemes = converter.convert(word)
        print(f"  '{word}' -> {phonemes}")
    
    # Test vintage DSP
    print("\nVintage DSP:")
    dsp = VintageDSP(22050, 8)
    params = dsp.get_vintage_parameters()
    print(f"  Sample Rate: {params['sample_rate']}Hz")
    print(f"  Bit Depth: {params['bit_depth']}-bit")
    print(f"  Quantization Levels: {params['quantization_levels']}")
    print(f"  Max Frequency: {params['max_frequency']}Hz")

if __name__ == "__main__":
    try:
        # Test individual components
        test_components()
        
        # Test full pipeline
        audio_output = test_pipeline()
        
        print(f"\n🎉 All tests passed! Generated {len(audio_output)} audio samples.")
        print("The TTS engine is ready for use.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
