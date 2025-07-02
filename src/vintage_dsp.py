"""
Vintage DSP Module for MR.ZPAYTZO-rev0
Implements 1986-era audio processing effects for authentic retro sound
"""

import numpy as np
from typing import Union, Tuple
import math


class VintageDSP:
    """
    Vintage digital signal processing implementing 1986-era audio characteristics.
    
    Recreates the distinctive sound limitations and artifacts of early TTS systems:
    - 8-bit quantization artifacts
    - Limited frequency response (22kHz max)
    - Primitive filtering algorithms
    - Sound Blaster-style audio processing
    """
    
    def __init__(self, sample_rate: int = 22050, bit_depth: int = 8):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.quantization_levels = 2 ** bit_depth
        
        # 1986-era processing parameters
        self.max_frequency = min(sample_rate // 2, 11025)  # Nyquist limit, typical 1986 max
        self.dynamic_range = 48.0  # dB, limited by 8-bit quantization
        
        # Initialize vintage filter states
        self._filter_state = {'lowpass': [0.0, 0.0], 'highpass': [0.0, 0.0]}
        
    def process(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply complete vintage processing chain to audio.
        
        Args:
            audio: Input audio samples (float32, -1 to 1 range)
            
        Returns:
            Processed audio with vintage characteristics
        """
        if len(audio) == 0:
            return audio
        
        # Stage 1: Apply analog limitations simulation
        audio = self._simulate_analog_frontend(audio)
        
        # Stage 2: Apply vintage anti-aliasing filter
        audio = self._apply_vintage_antialiasing(audio)
        
        # Stage 3: Bit crushing for quantization artifacts
        audio = self._apply_bit_crushing(audio)
        
        # Stage 4: Sample rate reduction effects
        audio = self._apply_sample_rate_artifacts(audio)
        
        # Stage 5: Vintage frequency response shaping
        audio = self._apply_frequency_response_shaping(audio)
        
        # Stage 6: Dynamic range compression (1986-style)
        audio = self._apply_vintage_compression(audio)
        
        # Stage 7: Final vintage output characteristics
        audio = self._apply_output_stage_processing(audio)
        
        return audio
    
    def _simulate_analog_frontend(self, audio: np.ndarray) -> np.ndarray:
        """Simulate analog input stage characteristics of 1986 hardware."""
        # Add subtle harmonic distortion
        # Very light non-linearity to simulate analog input circuits
        audio = audio + 0.002 * np.sign(audio) * (audio ** 2)
        
        # Add very subtle DC offset (common in vintage hardware)
        dc_offset = 0.001
        audio = audio + dc_offset
        
        return audio
    
    def _apply_vintage_antialiasing(self, audio: np.ndarray) -> np.ndarray:
        """Apply 1986-era anti-aliasing filter (simple low-pass)."""
        # Simple first-order low-pass filter at ~10kHz
        cutoff_freq = 10000  # Hz
        omega = 2 * np.pi * cutoff_freq / self.sample_rate
        alpha = np.exp(-omega)
        
        if len(audio) <= 1:
            return audio
        
        # Apply filter
        filtered = np.zeros_like(audio)
        filtered[0] = audio[0] * (1 - alpha)
        
        for i in range(1, len(audio)):
            filtered[i] = alpha * filtered[i-1] + (1 - alpha) * audio[i]
        
        return filtered
    
    def _apply_bit_crushing(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply bit crushing to simulate vintage quantization artifacts.
        
        Implements the characteristic staircase effect of early digital audio.
        """
        if self.bit_depth >= 16:
            return audio  # No crushing needed for 16-bit
        
        # Calculate quantization step
        max_level = 2 ** (self.bit_depth - 1) - 1  # Account for sign bit
        
        # Quantize
        quantized = np.round(audio * max_level) / max_level
        
        # Add quantization noise (characteristic of 1986 converters)
        noise_amplitude = 1.0 / (2 ** self.bit_depth) * 0.5
        quantization_noise = np.random.uniform(-noise_amplitude, noise_amplitude, len(audio))
        quantized += quantization_noise
        
        # Clamp to valid range
        quantized = np.clip(quantized, -1.0, 1.0)
        
        return quantized
    
    def _apply_sample_rate_artifacts(self, audio: np.ndarray) -> np.ndarray:
        """Apply sample rate reduction artifacts for vintage character."""
        # For 22kHz operation, this simulates the artifacts of the original sampling
        
        # Add subtle aliasing artifacts by introducing high-frequency content
        # that would alias down due to insufficient anti-aliasing in 1986
        if len(audio) > 1:
            # Generate subtle high-frequency noise that will alias
            t = np.arange(len(audio)) / self.sample_rate
            alias_freq = self.sample_rate * 0.7  # Above Nyquist when downsampled
            aliasing_signal = 0.001 * np.sin(2 * np.pi * alias_freq * t)
            
            # Add aliased content
            audio = audio + aliasing_signal
        
        return audio
    
    def _apply_frequency_response_shaping(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply vintage frequency response characteristics.
        
        Simulates the limited frequency response of 1986 audio hardware:
        - Roll-off above 8kHz
        - Slight emphasis around 2-4kHz (speech clarity region)
        - Reduced bass response
        """
        if len(audio) <= 1:
            return audio
        
        # Apply high-frequency roll-off (primitive low-pass)
        audio = self._apply_vintage_lowpass(audio, 8000)
        
        # Apply bass reduction (high-pass)
        audio = self._apply_vintage_highpass(audio, 200)
        
        # Mild mid-frequency emphasis (speech intelligibility)
        audio = self._apply_speech_emphasis(audio)
        
        return audio
    
    def _apply_vintage_lowpass(self, audio: np.ndarray, cutoff_freq: float) -> np.ndarray:
        """Apply simple vintage-style low-pass filter."""
        # Second-order Butterworth approximation using cascade of first-order
        omega = 2 * np.pi * cutoff_freq / self.sample_rate
        alpha = np.exp(-omega)
        
        # First stage
        y1 = np.zeros_like(audio)
        y1[0] = audio[0] * (1 - alpha)
        for i in range(1, len(audio)):
            y1[i] = alpha * y1[i-1] + (1 - alpha) * audio[i]
        
        # Second stage for steeper rolloff
        y2 = np.zeros_like(y1)
        y2[0] = y1[0] * (1 - alpha)
        for i in range(1, len(y1)):
            y2[i] = alpha * y2[i-1] + (1 - alpha) * y1[i]
        
        return y2
    
    def _apply_vintage_highpass(self, audio: np.ndarray, cutoff_freq: float) -> np.ndarray:
        """Apply simple vintage-style high-pass filter."""
        omega = 2 * np.pi * cutoff_freq / self.sample_rate
        alpha = np.exp(-omega)
        
        if len(audio) <= 1:
            return audio
        
        output = np.zeros_like(audio)
        output[0] = audio[0]
        
        for i in range(1, len(audio)):
            output[i] = alpha * output[i-1] + alpha * (audio[i] - audio[i-1])
        
        return output
    
    def _apply_speech_emphasis(self, audio: np.ndarray) -> np.ndarray:
        """Apply mild emphasis in speech frequency range (2-4kHz)."""
        # Simple peaking filter around 3kHz
        center_freq = 3000  # Hz
        bandwidth = 2000   # Hz
        gain = 1.2         # Mild 1.5dB boost
        
        # Convert to normalized frequencies
        omega_c = 2 * np.pi * center_freq / self.sample_rate
        omega_bw = 2 * np.pi * bandwidth / self.sample_rate
        
        # Simple resonant filter approximation
        if len(audio) <= 2:
            return audio * gain
        
        # Simplified peaking filter using difference equation
        output = np.zeros_like(audio)
        output[0] = audio[0]
        output[1] = audio[1]
        
        # Filter coefficients (simplified)
        a = 0.9  # Pole radius
        b = gain - 1.0  # Gain adjustment
        
        for i in range(2, len(audio)):
            # Simple biquad approximation
            resonance = a * np.cos(omega_c) * output[i-1] - a * a * output[i-2]
            output[i] = audio[i] + b * resonance
        
        return output
    
    def _apply_vintage_compression(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply 1986-style dynamic range compression.
        
        Simulates the primitive AGC (Automatic Gain Control) circuits
        used in early audio hardware.
        """
        if len(audio) == 0:
            return audio
        
        # Simple soft limiting (primitive compressor)
        threshold = 0.8
        ratio = 4.0  # 4:1 compression ratio
        
        # Calculate envelope (simple peak detector)
        envelope = np.abs(audio)
        
        # Smooth envelope (attack/release simulation)
        smooth_envelope = np.zeros_like(envelope)
        attack_coef = 0.1   # Fast attack
        release_coef = 0.001  # Slow release
        
        smooth_envelope[0] = envelope[0]
        for i in range(1, len(envelope)):
            if envelope[i] > smooth_envelope[i-1]:
                # Attack
                smooth_envelope[i] = attack_coef * envelope[i] + (1 - attack_coef) * smooth_envelope[i-1]
            else:
                # Release
                smooth_envelope[i] = release_coef * envelope[i] + (1 - release_coef) * smooth_envelope[i-1]
        
        # Apply compression
        gain_reduction = np.ones_like(smooth_envelope)
        
        # Calculate gain reduction for levels above threshold
        over_threshold = smooth_envelope > threshold
        if np.any(over_threshold):
            excess = smooth_envelope[over_threshold] - threshold
            gain_reduction[over_threshold] = threshold / smooth_envelope[over_threshold] * (1.0 + excess / ratio)
        
        # Apply gain reduction
        compressed = audio * gain_reduction
        
        return compressed
    
    def _apply_output_stage_processing(self, audio: np.ndarray) -> np.ndarray:
        """Apply final output stage processing characteristic of 1986 hardware."""
        # Simulate output DAC characteristics
        
        # 1. Add subtle even-order harmonic distortion (typical of 1986 DACs)
        harmonic_content = 0.001 * (audio ** 2)
        audio = audio + harmonic_content
        
        # 2. Apply output coupling capacitor effect (high-pass)
        if len(audio) > 1:
            audio = self._apply_vintage_highpass(audio, 20)  # Remove subsonic
        
        # 3. Final amplitude scaling for vintage output levels
        audio = audio * 0.9  # Slightly reduce to avoid clipping
        
        # 4. Final clipping protection (hard limiting)
        audio = np.clip(audio, -1.0, 1.0)
        
        return audio
    
    def apply_sound_blaster_characteristics(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply specific Sound Blaster audio characteristics.
        
        Recreates the distinctive sound of early Sound Blaster cards
        which were the primary target platform for Dr. Sbaitso.
        """
        # Sound Blaster specific processing
        
        # 1. 8-bit mono characteristics
        if self.bit_depth == 8:
            # Convert to unsigned 8-bit range (0-255) and back
            unsigned_audio = ((audio + 1.0) * 127.5).astype(np.uint8)
            audio = (unsigned_audio.astype(np.float32) / 127.5) - 1.0
        
        # 2. Limited frequency response of SB cards
        audio = self._apply_vintage_lowpass(audio, 11000)  # SB Pro limit
        
        # 3. SB-specific noise floor
        noise_floor = -48  # dB, typical for early SB cards
        noise_amplitude = 10 ** (noise_floor / 20)
        sb_noise = np.random.normal(0, noise_amplitude, len(audio))
        audio = audio + sb_noise
        
        return audio
    
    def apply_preset_vintage_effect(self, audio: np.ndarray, preset: str = "dr_sbaitso") -> np.ndarray:
        """
        Apply preset vintage effects for specific TTS systems.
        
        Args:
            audio: Input audio
            preset: Effect preset name
                   - "dr_sbaitso": Dr. Sbaitso characteristics
                   - "early_tts": Generic early TTS sound
                   - "sound_blaster": Sound Blaster card sound
        """
        if preset == "dr_sbaitso":
            # Specific Dr. Sbaitso processing chain
            audio = self._apply_bit_crushing(audio)
            audio = self._apply_vintage_lowpass(audio, 8000)
            audio = self._apply_speech_emphasis(audio)
            audio = self.apply_sound_blaster_characteristics(audio)
            
        elif preset == "early_tts":
            # Generic early TTS processing
            audio = self._apply_bit_crushing(audio)
            audio = self._apply_vintage_lowpass(audio, 6000)
            audio = self._apply_vintage_compression(audio)
            
        elif preset == "sound_blaster":
            # Sound Blaster specific
            audio = self.apply_sound_blaster_characteristics(audio)
            
        return audio
    
    def get_vintage_parameters(self) -> dict:
        """Return current vintage processing parameters."""
        return {
            'sample_rate': self.sample_rate,
            'bit_depth': self.bit_depth,
            'quantization_levels': self.quantization_levels,
            'max_frequency': self.max_frequency,
            'dynamic_range': self.dynamic_range
        }
    
    def set_bit_depth(self, bit_depth: int):
        """Set bit depth for quantization."""
        if bit_depth in [8, 12, 16]:
            self.bit_depth = bit_depth
            self.quantization_levels = 2 ** bit_depth
        else:
            raise ValueError("Bit depth must be 8, 12, or 16")
    
    def reset_filter_states(self):
        """Reset internal filter states."""
        self._filter_state = {'lowpass': [0.0, 0.0], 'highpass': [0.0, 0.0]}
