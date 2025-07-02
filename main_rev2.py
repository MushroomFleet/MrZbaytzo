#!/usr/bin/env python3
"""
MR.ZPAYTZO-rev2: Enhanced 1986 Text-to-Speech Synthesis Engine
Configurable quality levels while maintaining vintage character
"""

import sys
import argparse
import os
from pathlib import Path
from src.config_manager import ConfigManager
from src.text_processor import TextProcessor
from src.phoneme_converter import PhonemeConverter
from src.diphone_synthesizer import DiphoneSynthesizer
from src.enhanced_vintage_dsp import EnhancedVintageDSP
from src.enhanced_audio_output import EnhancedAudioOutput


class ZPaytzoEngineRev2:
    """
    Enhanced TTS engine class implementing configurable 1986-era synthesis technology.
    
    Features:
    - JSON-based configuration system
    - Quality presets (Authentic 1986, Enhanced Vintage, Modern Retro)
    - Configurable bit depth and vintage intensity
    - Advanced processing options
    - Backward compatibility with rev0
    """
    
    def __init__(self, config_file: str = None, preset: str = None):
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Load configuration
        if config_file:
            if not self.config_manager.load_config_file(config_file):
                print(f"Failed to load config file '{config_file}', using defaults")
        
        if preset:
            if not self.config_manager.load_preset(preset):
                print(f"Failed to load preset '{preset}', using current config")
        
        # Get configuration sections
        self.audio_config = self.config_manager.get_audio_config()
        self.synthesis_config = self.config_manager.get_synthesis_config()
        self.vintage_config = self.config_manager.get_vintage_config()
        self.prosody_config = self.config_manager.get_prosody_config()
        
        # Extract key parameters
        self.sample_rate = self.audio_config.get('sample_rate', 22050)
        self.bit_depth = self.audio_config.get('bit_depth', 8)
        self.channels = self.audio_config.get('channels', 1)
        
        # Initialize processing pipeline
        self._initialize_pipeline()
        
        # Print initialization info
        self._print_initialization_info()
    
    def _initialize_pipeline(self):
        """Initialize the TTS processing pipeline."""
        try:
            # Core processing components
            self.text_processor = TextProcessor()
            self.phoneme_converter = PhonemeConverter()
            self.synthesizer = DiphoneSynthesizer(self.sample_rate)
            
            # Enhanced vintage DSP with configuration
            full_config = self.config_manager.get_config()
            self.vintage_dsp = EnhancedVintageDSP(full_config)
            
            # Enhanced audio output with padding configuration
            padding_config = self.config_manager.get_padding_config()
            self.audio_output = EnhancedAudioOutput(
                sample_rate=self.sample_rate,
                channels=self.channels,
                buffer_size=self.audio_config.get('buffer_size', 1024),
                padding_config=padding_config
            )
            
            print("✓ TTS pipeline initialized successfully")
            
        except Exception as e:
            print(f"✗ Error initializing TTS pipeline: {e}")
            raise
    
    def _print_initialization_info(self):
        """Print initialization information."""
        print(f"\nMR.ZPAYTZO-rev2 initialized")
        print(f"Quality Level: {self.config_manager.get_quality_level()}")
        print(f"Preset: {self.config_manager.get_current_preset()}")
        print(f"Audio: {self.sample_rate}Hz, {self.bit_depth}-bit, {self.channels} channel(s)")
        
        # Vintage processing info
        vintage_info = self.vintage_dsp.get_processing_info()
        if vintage_info['vintage_enabled']:
            print(f"Vintage Processing: {vintage_info['vintage_intensity']:.1f} intensity, {vintage_info['vintage_preset']} preset")
        else:
            print("Vintage Processing: Disabled")
        
        # Advanced features
        advanced_features = []
        if vintage_info['spectral_enhancement']:
            advanced_features.append("Spectral Enhancement")
        if vintage_info['harmonic_enrichment']:
            advanced_features.append("Harmonic Enrichment")
        if vintage_info['noise_reduction']:
            advanced_features.append("Noise Reduction")
        if vintage_info['temporal_smoothing']:
            advanced_features.append("Temporal Smoothing")
        
        if advanced_features:
            print(f"Advanced Features: {', '.join(advanced_features)}")
    
    def speak(self, text: str, verbose: bool = False):
        """
        Convert text to speech using configurable synthesis technology.
        
        Args:
            text: Text to synthesize
            verbose: Print detailed processing information
        """
        if not text.strip():
            return
        
        if verbose:
            print(f"\nProcessing: '{text}'")
            print("=" * 50)
        
        try:
            # Stage 1: Text normalization and rule application
            if verbose:
                print("1. Text Processing...")
            normalized_text = self.text_processor.normalize(text)
            if verbose:
                print(f"   Normalized: '{normalized_text}'")
            
            # Stage 2: Grapheme-to-phoneme conversion
            if verbose:
                print("2. Phoneme Conversion...")
            phonemes = self.phoneme_converter.convert(normalized_text)
            if verbose:
                print(f"   Phonemes: {phonemes}")
            
            # Stage 3: Diphone concatenation synthesis
            if verbose:
                print("3. Audio Synthesis...")
            audio_samples = self.synthesizer.synthesize(phonemes)
            if verbose:
                print(f"   Generated {len(audio_samples)} audio samples")
                if len(audio_samples) > 0:
                    duration = len(audio_samples) / self.sample_rate
                    print(f"   Duration: {duration:.2f} seconds")
                    print(f"   Audio range: {np.min(audio_samples):.3f} to {np.max(audio_samples):.3f}")
            
            # Stage 4: Apply vintage/enhanced audio processing
            if verbose:
                print("4. Vintage DSP Processing...")
            processed_audio = self.vintage_dsp.process(audio_samples)
            if verbose:
                print(f"   Processed {len(processed_audio)} samples")
                if len(processed_audio) > 0:
                    print(f"   Processed range: {np.min(processed_audio):.3f} to {np.max(processed_audio):.3f}")
            
            # Stage 5: Audio output
            if verbose:
                print("5. Audio Output...")
            self.audio_output.play(processed_audio)
            
            if verbose:
                print("✓ Speech synthesis completed successfully!")
            
        except Exception as e:
            print(f"✗ Error during speech synthesis: {e}")
            raise
    
    def set_preset(self, preset_name: str) -> bool:
        """
        Change quality preset.
        
        Args:
            preset_name: Name of preset to load
            
        Returns:
            True if preset was loaded successfully
        """
        if self.config_manager.load_preset(preset_name):
            # Update audio configuration
            self.audio_config = self.config_manager.get_audio_config()
            self.sample_rate = self.audio_config.get('sample_rate', 22050)
            self.bit_depth = self.audio_config.get('bit_depth', 8)
            
            # Update vintage DSP configuration
            full_config = self.config_manager.get_config()
            self.vintage_dsp.update_config(full_config)
            
            # Reinitialize enhanced audio output if sample rate changed
            padding_config = self.config_manager.get_padding_config()
            self.audio_output = EnhancedAudioOutput(
                sample_rate=self.sample_rate,
                channels=self.channels,
                buffer_size=self.audio_config.get('buffer_size', 1024),
                padding_config=padding_config
            )
            
            print(f"✓ Switched to preset: {preset_name}")
            self._print_initialization_info()
            return True
        
        return False
    
    def list_presets(self):
        """List available quality presets."""
        presets = self.config_manager.list_presets()
        print("\nAvailable Quality Presets:")
        print("=" * 40)
        for preset in presets:
            current = " (current)" if preset['name'] == self.config_manager.get_current_preset() else ""
            print(f"  {preset['display_name']}{current}")
            print(f"    {preset['description']}")
            print()
    
    def configure(self, section: str, key: str, value):
        """
        Configure a specific parameter.
        
        Args:
            section: Configuration section
            key: Parameter key
            value: New value
        """
        if self.config_manager.set_config(section, key, value):
            # Update relevant components
            if section == 'audio':
                self.audio_config = self.config_manager.get_audio_config()
                if key in ['sample_rate', 'channels', 'buffer_size']:
                    # Reinitialize enhanced audio output
                    padding_config = self.config_manager.get_padding_config()
                    self.audio_output = EnhancedAudioOutput(
                        sample_rate=self.audio_config.get('sample_rate', 22050),
                        channels=self.audio_config.get('channels', 1),
                        buffer_size=self.audio_config.get('buffer_size', 1024),
                        padding_config=padding_config
                    )
            
            elif section in ['vintage_processing', 'advanced']:
                # Update vintage DSP
                full_config = self.config_manager.get_config()
                self.vintage_dsp.update_config(full_config)
            
            print(f"✓ Updated {section}.{key} = {value}")
        else:
            print(f"✗ Failed to update {section}.{key}")
    
    def print_config(self):
        """Print current configuration."""
        self.config_manager.print_current_config()
    
    def save_config(self, filename: str):
        """Save current configuration to file."""
        if self.config_manager.save_config(filename):
            print(f"✓ Configuration saved to {filename}")
        else:
            print(f"✗ Failed to save configuration to {filename}")
    
    def get_current_preset(self) -> str:
        """Get the name of the currently loaded preset."""
        return self.config_manager.get_current_preset()
    
    def get_quality_info(self) -> dict:
        """Get information about current quality settings."""
        return {
            'quality_level': self.config_manager.get_quality_level(),
            'preset': self.config_manager.get_current_preset(),
            'sample_rate': self.sample_rate,
            'bit_depth': self.bit_depth,
            'vintage_info': self.vintage_dsp.get_processing_info()
        }


def main():
    """Main entry point for MR.ZPAYTZO-rev2."""
    parser = argparse.ArgumentParser(
        description='MR.ZPAYTZO-rev2: Enhanced 1986 Text-to-Speech Synthesis Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality Presets:
  authentic_1986    - Original Dr. Sbaitso sound (8-bit, full vintage)
  enhanced_vintage  - Improved quality with vintage character (12-bit)
  modern_retro      - High quality with subtle vintage flavor (16-bit)

Examples:
  python main_rev2.py "Hello world"
  python main_rev2.py --preset enhanced_vintage "Better quality speech"
  python main_rev2.py --config my_config.json "Custom configuration"
  python main_rev2.py --interactive --preset modern_retro
        """
    )
    
    parser.add_argument('text', nargs='?', help='Text to synthesize')
    
    # Configuration options
    parser.add_argument('--preset', '-p', type=str,
                      help='Quality preset (authentic_1986, enhanced_vintage, modern_retro)')
    parser.add_argument('--config', '-c', type=str,
                      help='Configuration file to load')
    
    # Legacy compatibility options
    parser.add_argument('--sample-rate', type=int,
                      help='Sample rate (8000-48000 Hz)')
    parser.add_argument('--bit-depth', type=int, choices=[8, 12, 16],
                      help='Bit depth (8, 12, or 16 bits)')
    parser.add_argument('--vintage-intensity', type=float,
                      help='Vintage processing intensity (0.0-1.0)')
    
    # Mode options
    parser.add_argument('--interactive', '-i', action='store_true',
                      help='Interactive mode')
    parser.add_argument('--list-presets', action='store_true',
                      help='List available quality presets')
    parser.add_argument('--print-config', action='store_true',
                      help='Print current configuration')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        # Initialize TTS engine
        engine = ZPaytzoEngineRev2(
            config_file=args.config,
            preset=args.preset
        )
        
        # Apply legacy command-line overrides
        if args.sample_rate:
            engine.configure('audio', 'sample_rate', args.sample_rate)
        if args.bit_depth:
            engine.configure('audio', 'bit_depth', args.bit_depth)
        if args.vintage_intensity is not None:
            engine.configure('vintage_processing', 'intensity', args.vintage_intensity)
        
        # Handle special modes
        if args.list_presets:
            engine.list_presets()
            return
        
        if args.print_config:
            engine.print_config()
            return
        
        # Interactive mode
        if args.interactive:
            print("\nInteractive mode - Enter text to speak")
            print("Commands:")
            print("  :preset <name>     - Change quality preset")
            print("  :config            - Show current configuration")
            print("  :presets           - List available presets")
            print("  :quit              - Exit")
            print("  Ctrl+C             - Exit")
            print()
            
            try:
                while True:
                    text = input("> ").strip()
                    
                    if not text:
                        continue
                    
                    if text.startswith(':'):
                        # Handle commands
                        parts = text[1:].split()
                        command = parts[0].lower()
                        
                        if command == 'quit':
                            break
                        elif command == 'config':
                            engine.print_config()
                        elif command == 'presets':
                            engine.list_presets()
                        elif command == 'preset' and len(parts) > 1:
                            engine.set_preset(parts[1])
                        else:
                            print("Unknown command. Available: :preset, :config, :presets, :quit")
                    else:
                        # Synthesize speech
                        engine.speak(text, verbose=args.verbose)
                        
            except KeyboardInterrupt:
                print("\nGoodbye!")
        
        # Single synthesis mode
        elif args.text:
            engine.speak(args.text, verbose=args.verbose)
        
        # No text provided
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Import numpy here to avoid issues if not available
    try:
        import numpy as np
    except ImportError:
        print("Error: numpy is required but not installed")
        print("Please install with: pip install numpy")
        sys.exit(1)
    
    main()
