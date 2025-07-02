"""
Enhanced Audio Output Module for MR.ZPAYTZO-rev2
Handles audio padding, fade-in/out, and improved playback to prevent clipping
"""

import numpy as np
import sounddevice as sd
import threading
import time
from typing import Optional, Union, Dict, Any
import sys
from .audio_output import AudioOutput


class EnhancedAudioOutput(AudioOutput):
    """
    Enhanced audio output manager with padding and fade support.
    
    Extends the base AudioOutput class to add:
    - Configurable start/end silence padding
    - Fade-in/fade-out to prevent clicks
    - Quality-aware padding settings
    - Improved buffer management
    """
    
    def __init__(self, sample_rate: int = 22050, channels: int = 1, buffer_size: int = 1024,
                 padding_config: Optional[Dict[str, Any]] = None):
        super().__init__(sample_rate, channels, buffer_size)
        
        # Padding configuration
        self.padding_config = padding_config or {
            'start_silence_ms': 150,
            'end_silence_ms': 250,
            'fade_in_ms': 25,
            'fade_out_ms': 50
        }
        
        print(f"Enhanced audio output initialized with padding:")
        print(f"  Start silence: {self.padding_config['start_silence_ms']}ms")
        print(f"  End silence: {self.padding_config['end_silence_ms']}ms")
        print(f"  Fade in: {self.padding_config['fade_in_ms']}ms")
        print(f"  Fade out: {self.padding_config['fade_out_ms']}ms")
    
    def play(self, audio_data: np.ndarray, blocking: bool = True):
        """
        Play audio data with enhanced padding and fade processing.
        
        Args:
            audio_data: Audio samples (float32, normalized -1 to 1)
            blocking: If True, wait for playback to complete
        """
        if len(audio_data) == 0:
            return
        
        # Apply enhanced audio processing
        enhanced_audio = self._apply_enhanced_processing(audio_data)
        
        # Use parent class playback with enhanced audio
        super().play(enhanced_audio, blocking)
    
    def _apply_enhanced_processing(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply enhanced processing including padding and fades."""
        # Ensure audio is in correct format
        audio_data = self._prepare_audio_data(audio_data)
        
        # Add silence padding
        padded_audio = self._add_silence_padding(audio_data)
        
        # Apply fade-in and fade-out
        faded_audio = self._apply_fades(padded_audio)
        
        # Apply vintage playback characteristics
        processed_audio = self._apply_playback_processing(faded_audio)
        
        return processed_audio
    
    def _add_silence_padding(self, audio_data: np.ndarray) -> np.ndarray:
        """Add configurable silence padding at start and end."""
        if len(audio_data) == 0:
            return audio_data
        
        # Calculate padding samples
        start_samples = int(self.padding_config['start_silence_ms'] * self.sample_rate / 1000)
        end_samples = int(self.padding_config['end_silence_ms'] * self.sample_rate / 1000)
        
        # Handle mono/stereo
        if len(audio_data.shape) == 1:
            # Mono
            start_silence = np.zeros(start_samples, dtype=np.float32)
            end_silence = np.zeros(end_samples, dtype=np.float32)
            padded_audio = np.concatenate([start_silence, audio_data, end_silence])
        else:
            # Stereo
            channels = audio_data.shape[1]
            start_silence = np.zeros((start_samples, channels), dtype=np.float32)
            end_silence = np.zeros((end_samples, channels), dtype=np.float32)
            padded_audio = np.concatenate([start_silence, audio_data, end_silence], axis=0)
        
        return padded_audio
    
    def _apply_fades(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply fade-in and fade-out to prevent clicks and pops."""
        if len(audio_data) == 0:
            return audio_data
        
        # Calculate fade samples
        fade_in_samples = int(self.padding_config['fade_in_ms'] * self.sample_rate / 1000)
        fade_out_samples = int(self.padding_config['fade_out_ms'] * self.sample_rate / 1000)
        
        # Ensure fade lengths don't exceed audio length
        total_samples = len(audio_data)
        fade_in_samples = min(fade_in_samples, total_samples // 4)
        fade_out_samples = min(fade_out_samples, total_samples // 4)
        
        # Create fade curves (cosine-based for smooth transitions)
        if fade_in_samples > 0:
            fade_in_curve = 0.5 * (1 - np.cos(np.pi * np.arange(fade_in_samples) / fade_in_samples))
        else:
            fade_in_curve = np.array([])
        
        if fade_out_samples > 0:
            fade_out_curve = 0.5 * (1 + np.cos(np.pi * np.arange(fade_out_samples) / fade_out_samples))
        else:
            fade_out_curve = np.array([])
        
        # Apply fades
        faded_audio = audio_data.copy()
        
        if len(audio_data.shape) == 1:
            # Mono
            if fade_in_samples > 0:
                faded_audio[:fade_in_samples] *= fade_in_curve
            if fade_out_samples > 0:
                faded_audio[-fade_out_samples:] *= fade_out_curve
        else:
            # Stereo
            if fade_in_samples > 0:
                faded_audio[:fade_in_samples] *= fade_in_curve[:, np.newaxis]
            if fade_out_samples > 0:
                faded_audio[-fade_out_samples:] *= fade_out_curve[:, np.newaxis]
        
        return faded_audio
    
    def update_padding_config(self, padding_config: Dict[str, Any]):
        """Update padding configuration at runtime."""
        self.padding_config.update(padding_config)
        print(f"Updated padding configuration:")
        print(f"  Start silence: {self.padding_config['start_silence_ms']}ms")
        print(f"  End silence: {self.padding_config['end_silence_ms']}ms")
        print(f"  Fade in: {self.padding_config['fade_in_ms']}ms")
        print(f"  Fade out: {self.padding_config['fade_out_ms']}ms")
    
    def get_padding_info(self) -> Dict[str, Any]:
        """Get current padding configuration information."""
        total_padding_ms = (self.padding_config['start_silence_ms'] + 
                           self.padding_config['end_silence_ms'])
        
        return {
            'start_silence_ms': self.padding_config['start_silence_ms'],
            'end_silence_ms': self.padding_config['end_silence_ms'],
            'fade_in_ms': self.padding_config['fade_in_ms'],
            'fade_out_ms': self.padding_config['fade_out_ms'],
            'total_padding_ms': total_padding_ms,
            'start_silence_samples': int(self.padding_config['start_silence_ms'] * self.sample_rate / 1000),
            'end_silence_samples': int(self.padding_config['end_silence_ms'] * self.sample_rate / 1000)
        }
    
    def test_padding_audio_output(self, frequency: float = 440.0, duration: float = 0.5):
        """Test audio output with padding using a short tone."""
        print(f"Testing enhanced audio output with padding: {frequency}Hz for {duration}s")
        
        # Generate short test tone
        t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
        test_tone = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Show padding info
        padding_info = self.get_padding_info()
        print(f"Total audio duration with padding: {duration * 1000 + padding_info['total_padding_ms']:.0f}ms")
        
        # Play test tone with padding
        try:
            self.play(test_tone, blocking=True)
            print("Enhanced audio test completed successfully")
        except Exception as e:
            print(f"Enhanced audio test failed: {e}")
    
    def analyze_audio_timing(self, audio_data: np.ndarray) -> Dict[str, Any]:
        """Analyze timing characteristics of audio with padding."""
        if len(audio_data) == 0:
            return {}
        
        # Original audio info
        original_duration_ms = len(audio_data) / self.sample_rate * 1000
        
        # Enhanced audio info
        enhanced_audio = self._apply_enhanced_processing(audio_data)
        enhanced_duration_ms = len(enhanced_audio) / self.sample_rate * 1000
        
        padding_info = self.get_padding_info()
        
        return {
            'original_duration_ms': original_duration_ms,
            'enhanced_duration_ms': enhanced_duration_ms,
            'added_padding_ms': enhanced_duration_ms - original_duration_ms,
            'start_padding_ms': padding_info['start_silence_ms'],
            'end_padding_ms': padding_info['end_silence_ms'],
            'fade_in_ms': padding_info['fade_in_ms'],
            'fade_out_ms': padding_info['fade_out_ms'],
            'original_samples': len(audio_data),
            'enhanced_samples': len(enhanced_audio)
        }
    
    def set_quality_preset_padding(self, preset_name: str):
        """Set padding configuration based on quality preset."""
        preset_padding = {
            'authentic_1986': {
                'start_silence_ms': 100,
                'end_silence_ms': 200,
                'fade_in_ms': 10,
                'fade_out_ms': 25
            },
            'enhanced_vintage': {
                'start_silence_ms': 150,
                'end_silence_ms': 250,
                'fade_in_ms': 25,
                'fade_out_ms': 50
            },
            'modern_retro': {
                'start_silence_ms': 200,
                'end_silence_ms': 300,
                'fade_in_ms': 50,
                'fade_out_ms': 75
            }
        }
        
        if preset_name in preset_padding:
            self.update_padding_config(preset_padding[preset_name])
            print(f"Applied {preset_name} padding preset")
        else:
            print(f"Unknown preset: {preset_name}, keeping current padding")
    
    def create_silence(self, duration_ms: float) -> np.ndarray:
        """Create silence of specified duration."""
        samples = int(duration_ms * self.sample_rate / 1000)
        
        if self.channels == 1:
            return np.zeros(samples, dtype=np.float32)
        else:
            return np.zeros((samples, self.channels), dtype=np.float32)
    
    def measure_device_latency(self) -> Dict[str, float]:
        """Measure actual audio device latency."""
        try:
            # Get device latency information
            device_info = sd.query_devices(self.output_device)
            
            # Calculate various latency components
            device_latency_ms = device_info.get('default_low_output_latency', 0) * 1000
            buffer_latency_ms = (self.buffer_size / self.sample_rate) * 1000
            padding_latency_ms = self.padding_config['start_silence_ms']
            
            total_latency_ms = device_latency_ms + buffer_latency_ms + padding_latency_ms
            
            return {
                'device_latency_ms': device_latency_ms,
                'buffer_latency_ms': buffer_latency_ms,
                'padding_latency_ms': padding_latency_ms,
                'total_latency_ms': total_latency_ms
            }
            
        except Exception as e:
            print(f"Could not measure device latency: {e}")
            return {
                'device_latency_ms': 0,
                'buffer_latency_ms': (self.buffer_size / self.sample_rate) * 1000,
                'padding_latency_ms': self.padding_config['start_silence_ms'],
                'total_latency_ms': self.padding_config['start_silence_ms'] + 
                                   (self.buffer_size / self.sample_rate) * 1000
            }
