#!/usr/bin/env python3
"""
MR.ZPAYTZO-rev0: 1986 Text-to-Speech Synthesis Engine
A faithful recreation of vintage TTS technology using diphone concatenation.
"""

import sys
import argparse
from src.text_processor import TextProcessor
from src.phoneme_converter import PhonemeConverter
from src.diphone_synthesizer import DiphoneSynthesizer
from src.vintage_dsp import VintageDSP
from src.audio_output import AudioOutput


class ZPaytzoEngine:
    """Main TTS engine class implementing 1986-era synthesis technology."""
    
    def __init__(self, sample_rate=22050, bit_depth=8):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        
        # Initialize processing pipeline
        self.text_processor = TextProcessor()
        self.phoneme_converter = PhonemeConverter()
        self.synthesizer = DiphoneSynthesizer(sample_rate)
        self.vintage_dsp = VintageDSP(sample_rate, bit_depth)
        self.audio_output = AudioOutput(sample_rate)
        
        print(f"MR.ZPAYTZO-rev0 initialized: {sample_rate}Hz, {bit_depth}-bit")
    
    def speak(self, text):
        """Convert text to speech using 1986 synthesis technology."""
        if not text.strip():
            return
        
        print(f"Processing: {text}")
        
        # Stage 1: Text normalization and rule application
        normalized_text = self.text_processor.normalize(text)
        
        # Stage 2: Grapheme-to-phoneme conversion
        phonemes = self.phoneme_converter.convert(normalized_text)
        
        # Stage 3: Diphone concatenation synthesis
        audio_samples = self.synthesizer.synthesize(phonemes)
        
        # Stage 4: Apply vintage audio characteristics
        vintage_audio = self.vintage_dsp.process(audio_samples)
        
        # Stage 5: Audio output
        self.audio_output.play(vintage_audio)


def main():
    parser = argparse.ArgumentParser(
        description='MR.ZPAYTZO-rev0: 1986 Text-to-Speech Synthesis Engine'
    )
    parser.add_argument('text', nargs='?', help='Text to synthesize')
    parser.add_argument('--sample-rate', type=int, default=22050,
                      help='Sample rate (8000-44100 Hz, default: 22050)')
    parser.add_argument('--bit-depth', type=int, choices=[8, 12, 16], default=8,
                      help='Bit depth (8, 12, or 16 bits, default: 8)')
    parser.add_argument('--interactive', '-i', action='store_true',
                      help='Interactive mode')
    
    args = parser.parse_args()
    
    # Initialize TTS engine
    engine = ZPaytzoEngine(args.sample_rate, args.bit_depth)
    
    if args.interactive:
        print("Interactive mode - Enter text to speak (Ctrl+C to exit)")
        try:
            while True:
                text = input("> ")
                if text.strip():
                    engine.speak(text)
        except KeyboardInterrupt:
            print("\nGoodbye!")
    elif args.text:
        engine.speak(args.text)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
