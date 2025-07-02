"""
Audio Output Module for MR.ZPAYTZO-rev0
Handles cross-platform audio playback with 1986-era characteristics
"""

import numpy as np
import sounddevice as sd
import threading
import time
from typing import Optional, Union
import sys


class AudioOutput:
    """
    Cross-platform audio output manager implementing vintage playback characteristics.
    
    Supports multiple audio backends with period-appropriate limitations:
    - DirectSound/WASAPI (Windows)
    - CoreAudio (macOS) 
    - ALSA/PulseAudio (Linux)
    
    Emulates Sound Blaster-style audio output behavior.
    """
    
    def __init__(self, sample_rate: int = 22050, channels: int = 1, buffer_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_size = buffer_size
        
        # 1986-era audio characteristics
        self.latency = 'high'  # Higher latency typical of vintage hardware
        self.blocking_playback = True  # Synchronous playback like original
        
        # Audio device configuration
        self.device_info = None
        self.output_device = None
        
        # Playback state
        self._is_playing = False
        self._playback_thread = None
        self._stop_event = threading.Event()
        
        # Initialize audio system
        self._initialize_audio_system()
    
    def _initialize_audio_system(self):
        """Initialize audio system and detect available devices."""
        try:
            # Get default output device
            self.device_info = sd.query_devices(kind='output')
            self.output_device = sd.default.device[1]  # Output device
            
            print(f"Audio system initialized:")
            print(f"  Device: {self.device_info['name']}")
            print(f"  Sample Rate: {self.sample_rate}Hz")
            print(f"  Channels: {self.channels}")
            print(f"  Buffer Size: {self.buffer_size}")
            
        except Exception as e:
            print(f"Warning: Audio initialization failed: {e}")
            print("Audio playback may not work correctly.")
    
    def play(self, audio_data: np.ndarray, blocking: bool = True):
        """
        Play audio data with vintage characteristics.
        
        Args:
            audio_data: Audio samples (float32, normalized -1 to 1)
            blocking: If True, wait for playback to complete
        """
        if len(audio_data) == 0:
            return
        
        # Ensure audio is in correct format
        audio_data = self._prepare_audio_data(audio_data)
        
        # Apply vintage playback characteristics
        audio_data = self._apply_playback_processing(audio_data)
        
        try:
            if blocking:
                # Synchronous playback (vintage behavior)
                self._play_blocking(audio_data)
            else:
                # Asynchronous playback
                self._play_async(audio_data)
                
        except Exception as e:
            print(f"Audio playback error: {e}")
            # Fallback to system beep
            self._fallback_audio_notification()
    
    def _prepare_audio_data(self, audio_data: np.ndarray) -> np.ndarray:
        """Prepare audio data for playback."""
        # Ensure float32 format
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        
        # Handle mono/stereo conversion
        if len(audio_data.shape) == 1:
            # Mono input
            if self.channels == 2:
                # Convert mono to stereo
                audio_data = np.column_stack((audio_data, audio_data))
        elif len(audio_data.shape) == 2:
            # Stereo input
            if self.channels == 1:
                # Convert stereo to mono
                audio_data = np.mean(audio_data, axis=1)
        
        # Ensure proper range
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        return audio_data
    
    def _apply_playback_processing(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply vintage playback processing."""
        # 1. Simulate Sound Blaster output characteristics
        audio_data = self._simulate_sb_output_stage(audio_data)
        
        # 2. Apply output amplifier characteristics
        audio_data = self._apply_output_amplifier_simulation(audio_data)
        
        # 3. Final range limiting
        audio_data = np.clip(audio_data, -0.95, 0.95)  # Avoid hard clipping
        
        return audio_data
    
    def _simulate_sb_output_stage(self, audio_data: np.ndarray) -> np.ndarray:
        """Simulate Sound Blaster output stage characteristics."""
        # Add very subtle output transformer saturation
        # (Sound Blaster cards had small output transformers)
        saturation_threshold = 0.8
        over_threshold = np.abs(audio_data) > saturation_threshold
        
        if np.any(over_threshold):
            # Soft saturation curve
            sign = np.sign(audio_data)
            magnitude = np.abs(audio_data)
            
            # Apply gentle saturation above threshold
            saturated_magnitude = np.where(
                magnitude > saturation_threshold,
                saturation_threshold + (magnitude - saturation_threshold) * 0.3,
                magnitude
            )
            
            audio_data = sign * saturated_magnitude
        
        return audio_data
    
    def _apply_output_amplifier_simulation(self, audio_data: np.ndarray) -> np.ndarray:
        """Simulate vintage output amplifier characteristics."""
        # Add very subtle even harmonic distortion
        harmonic_amount = 0.0005  # Very subtle
        audio_data = audio_data + harmonic_amount * (audio_data ** 2) * np.sign(audio_data)
        
        # Simulate frequency response of vintage output stage
        if len(audio_data) > 1:
            # Very gentle high-frequency roll-off
            cutoff = 0.95  # Very mild filtering
            audio_data[1:] = cutoff * audio_data[1:] + (1 - cutoff) * audio_data[:-1]
        
        return audio_data
    
    def _play_blocking(self, audio_data: np.ndarray):
        """Play audio synchronously (blocking)."""
        self._is_playing = True
        
        try:
            # Use sounddevice for cross-platform playback
            sd.play(
                audio_data,
                samplerate=self.sample_rate,
                device=self.output_device,
                blocking=True
            )
            
        except Exception as e:
            print(f"Blocking playback failed: {e}")
            raise
        finally:
            self._is_playing = False
    
    def _play_async(self, audio_data: np.ndarray):
        """Play audio asynchronously (non-blocking)."""
        if self._is_playing:
            self.stop()
        
        self._stop_event.clear()
        self._playback_thread = threading.Thread(
            target=self._async_playback_worker,
            args=(audio_data,)
        )
        self._playback_thread.start()
    
    def _async_playback_worker(self, audio_data: np.ndarray):
        """Worker thread for asynchronous playback."""
        self._is_playing = True
        
        try:
            sd.play(
                audio_data,
                samplerate=self.sample_rate,
                device=self.output_device,
                blocking=False
            )
            
            # Wait for playback to complete or stop signal
            duration = len(audio_data) / self.sample_rate
            self._stop_event.wait(timeout=duration)
            
        except Exception as e:
            print(f"Async playback failed: {e}")
        finally:
            self._is_playing = False
    
    def stop(self):
        """Stop current playback."""
        if self._is_playing:
            try:
                sd.stop()
                self._stop_event.set()
                
                if self._playback_thread and self._playback_thread.is_alive():
                    self._playback_thread.join(timeout=1.0)
                    
            except Exception as e:
                print(f"Stop playback error: {e}")
            finally:
                self._is_playing = False
    
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        return self._is_playing
    
    def get_device_info(self) -> dict:
        """Get information about current audio device."""
        try:
            devices = sd.query_devices()
            if isinstance(devices, dict):
                return devices
            elif isinstance(devices, list) and self.output_device is not None:
                return devices[self.output_device]
            else:
                return {"name": "Unknown", "channels": self.channels}
        except:
            return {"name": "Unknown", "channels": self.channels}
    
    def list_audio_devices(self):
        """List available audio devices."""
        try:
            print("Available audio devices:")
            devices = sd.query_devices()
            
            if isinstance(devices, list):
                for i, device in enumerate(devices):
                    device_type = "Input" if device['max_input_channels'] > 0 else ""
                    if device['max_output_channels'] > 0:
                        device_type += " Output" if device_type else "Output"
                    
                    print(f"  {i}: {device['name']} ({device_type})")
            else:
                print(f"  Default: {devices['name']}")
                
        except Exception as e:
            print(f"Failed to list audio devices: {e}")
    
    def set_output_device(self, device_id: Optional[int] = None):
        """Set output audio device."""
        try:
            if device_id is not None:
                # Verify device exists and supports output
                device_info = sd.query_devices(device_id)
                if device_info['max_output_channels'] > 0:
                    self.output_device = device_id
                    self.device_info = device_info
                    print(f"Output device set to: {device_info['name']}")
                else:
                    print(f"Device {device_id} does not support output")
            else:
                # Use default
                self.output_device = sd.default.device[1]
                self.device_info = sd.query_devices(self.output_device)
                print(f"Using default output device: {self.device_info['name']}")
                
        except Exception as e:
            print(f"Failed to set output device: {e}")
    
    def test_audio_output(self, frequency: float = 440.0, duration: float = 1.0):
        """Test audio output with a simple tone."""
        print(f"Testing audio output: {frequency}Hz for {duration}s")
        
        # Generate test tone
        t = np.linspace(0, duration, int(duration * self.sample_rate), endpoint=False)
        test_tone = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Apply vintage processing
        test_tone = self._apply_playback_processing(test_tone)
        
        # Play test tone
        try:
            self.play(test_tone, blocking=True)
            print("Audio test completed successfully")
        except Exception as e:
            print(f"Audio test failed: {e}")
    
    def _fallback_audio_notification(self):
        """Fallback audio notification when normal playback fails."""
        try:
            # Try system beep as last resort
            if sys.platform == "win32":
                import winsound
                winsound.Beep(1000, 500)
            elif sys.platform == "darwin":
                import os
                os.system("say 'Audio playback failed'")
            else:
                # Linux/Unix
                print("\a")  # Terminal bell
        except:
            print("Audio playback failed - no sound output available")
    
    def get_latency_info(self) -> dict:
        """Get audio latency information."""
        try:
            device_info = sd.query_devices(self.output_device)
            return {
                'device_latency': device_info.get('default_low_output_latency', 0),
                'buffer_size': self.buffer_size,
                'estimated_latency_ms': (self.buffer_size / self.sample_rate) * 1000
            }
        except:
            return {
                'device_latency': 0,
                'buffer_size': self.buffer_size,
                'estimated_latency_ms': (self.buffer_size / self.sample_rate) * 1000
            }
    
    def cleanup(self):
        """Clean up audio resources."""
        try:
            self.stop()
            sd.stop()
        except:
            pass
    
    def __del__(self):
        """Destructor - clean up resources."""
        self.cleanup()
