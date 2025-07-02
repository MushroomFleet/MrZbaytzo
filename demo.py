#!/usr/bin/env python3
"""
Demo script for MR.ZPAYTZO-rev0 - showcasing 1986 TTS technology
"""

import sys
import time
from main import ZPaytzo

def run_demo():
    """Run a demonstration of the TTS capabilities."""
    print("=" * 60)
    print("  MR.ZPAYTZO-rev0: 1986 Text-to-Speech Synthesis Engine")
    print("  Faithful recreation of Dr. Sbaitso technology")
    print("=" * 60)
    
    # Initialize TTS engine
    tts = ZPaytzo(sample_rate=22050, bit_depth=8)
    
    demo_phrases = [
        "Hello, I am a computer speech synthesizer from nineteen eighty six.",
        "This is a demonstration of vintage text to speech technology.",
        "Dr. Sbaitso was an early artificial intelligence program.",
        "The quick brown fox jumps over the lazy dog.",
        "Computing technology has advanced significantly since then.",
        "First Byte Monologue engine used diphone concatenation synthesis.",
        "Sound Blaster cards were the primary audio hardware platform.",
        "Eight bit quantization creates distinctive vintage character.",
        "Thank you for using MR.ZPAYTZO text to speech system."
    ]
    
    print("\nDemonstration will speak 9 phrases...")
    print("Press Ctrl+C to stop at any time.\n")
    
    try:
        for i, phrase in enumerate(demo_phrases, 1):
            print(f"{i:2d}. Speaking: \"{phrase}\"")
            tts.speak(phrase)
            
            # Small pause between phrases
            time.sleep(0.5)
            
        print("\n✓ Demonstration completed successfully!")
        print("\nTo use the TTS engine:")
        print("  python main.py \"Your text here\"")
        print("  python main.py -i  (for interactive mode)")
        
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user.")
    except Exception as e:
        print(f"\nDemo error: {e}")
    finally:
        tts.cleanup()

def show_technical_info():
    """Display technical information about the implementation."""
    print("\nTechnical Information:")
    print("=" * 30)
    print("• Synthesis Method: Diphone concatenation")
    print("• Phoneme Database: ~800-1000 diphones")
    print("• Text Rules: ~1,200 linguistic rules")
    print("• Sample Rate: 8-44.1kHz (default: 22.05kHz)")
    print("• Bit Depth: 8-bit vintage (8/12/16-bit options)")
    print("• Formants: F1, F2, F3 resonator bank")
    print("• Audio Effects: Vintage DSP, Sound Blaster simulation")
    print("• Platform: Cross-platform (Windows/macOS/Linux)")
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        show_technical_info()
    else:
        show_technical_info()
        run_demo()
