"""
Enhanced Vintage DSP Module for MR.ZPAYTZO-rev2
Configurable vintage audio processing with quality scaling
"""

import numpy as np
from typing import Union, Tuple, Dict, Any
import math
from .vintage_dsp import VintageDSP


class EnhancedVintageDSP(VintageDSP):
    """
    Enhanced vintage DSP with configurable quality levels and processing intensity.
    
    Extends the original VintageDSP with:
    - Configurable vintage intensity (0.0 = clean, 1.0 = full vintage)
    - Quality-aware processing chains
    - Advanced spectral enhancement options
    - Adaptive bit depth handling
    """
    
    def __init__(self, config: Dict[str, Any]):
        # Extract configuration
        audio_config = config.get('audio', {})
        vintage_config = config.get('vintage_processing', {})
        advanced_config = config.get('advanced', {})
        
        sample_rate = audio_config.get('sample_rate', 22050)
        bit_depth = audio_config.get('bit_depth', 8)
        
        # Initialize base class
        super().__init__(sample_rate, bit_depth)
        
        # Enhanced configuration
        self.vintage_intensity = vintage_config.get('intensity', 1.0)
        self.vintage_enabled = vintage_config.get('enabled', True)
        self.vintage_preset = vintage_config.get('preset', 'dr_sbaitso')
        self.quantization_noise = vintage_config.get('quantization_noise', True)
        self.analog_simulation = vintage_config.get('analog_simulation', True)
        self.frequency_response_shaping = vintage_config.get('frequency_response_shaping', True)
        
        # Advanced processing options
        self.spectral_enhancement = advanced_config.get('spectral_enhancement', False)
        self.harmonic_enrichment = advanced_config.get('harmonic_enrichment', False)
        self.noise_reduction = advanced_config.get('noise_reduction', False)
        self.temporal_smoothing = advanced_config.get('temporal_smoothing', False)
        
        # Quality-dependent parameters
        self._setup_quality_parameters()
    
    def _setup_quality_parameters(self):
        """Setup quality-dependent processing parameters."""
        # Adjust processing based on bit depth and vintage intensity
        if self.bit_depth >= 16:
            self.quantization_levels = 65536
            self.dynamic_range = 96.0  # 16-bit dynamic range
            self.noise_floor = -90  # dB
        elif self.bit_depth >= 12:
            self.quantization_levels = 4096
            self.dynamic_range = 72.0  # 12-bit dynamic range
            self.noise_floor = -66  # dB
        else:
            self.quantization_levels = 256
            self.dynamic_range = 48.0  # 8-bit dynamic range
            self.noise_floor = -42  # dB
        
        # Adjust filter quality based on vintage intensity
        self.filter_quality = 1.0 - (self.vintage_intensity * 0.5)
        
        # Adjust frequency response based on configuration
        if self.vintage_intensity > 0.8:
            self.max_frequency = 8000  # Heavy vintage limiting
        elif self.vintage_intensity > 0.5:
            self.max_frequency = 11025  # Moderate vintage limiting
        else:
            self.max_frequency = min(self.sample_rate // 2, 16000)  # Less limiting
    
    def process(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply enhanced vintage processing chain with configurable quality.
        
        Args:
            audio: Input audio samples (float32, -1 to 1 range)
            
        Returns:
            Processed audio with vintage characteristics
        """
        if len(audio) == 0:
            return audio
        
        # Start with clean audio
        processed_audio = audio.copy()
        
        # Apply pre-processing enhancements if enabled
        if self.spectral_enhancement:
            processed_audio = self._apply_spectral_enhancement(processed_audio)
        
        if self.harmonic_enrichment:
            processed_audio = self._apply_harmonic_enrichment(processed_audio)
        
        # Apply vintage processing if enabled
        if self.vintage_enabled and self.vintage_intensity > 0:
            processed_audio = self._apply_vintage_processing_chain(processed_audio)
        
        # Apply post-processing enhancements
        if self.noise_reduction:
            processed_audio = self._apply_noise_reduction(processed_audio)
        
        if self.temporal_smoothing:
            processed_audio = self._apply_temporal_smoothing(processed_audio)
        
        return processed_audio
    
    def _apply_vintage_processing_chain(self, audio: np.ndarray) -> np.ndarray:
        """Apply the vintage processing chain with configurable intensity."""
        # Scale vintage effects by intensity
        vintage_audio = audio.copy()
        
        # Stage 1: Analog frontend simulation (if enabled)
        if self.analog_simulation:
            vintage_audio = self._simulate_analog_frontend_enhanced(vintage_audio)
        
        # Stage 2: Frequency response shaping (if enabled)
        if self.frequency_response_shaping:
            vintage_audio = self._apply_frequency_response_shaping_enhanced(vintage_audio)
        
        # Stage 3: Bit crushing with intensity scaling
        vintage_audio = self._apply_enhanced_bit_crushing(vintage_audio)
        
        # Stage 4: Vintage compression
        vintage_audio = self._apply_vintage_compression_enhanced(vintage_audio)
        
        # Stage 5: Apply preset-specific processing
        vintage_audio = self._apply_preset_processing(vintage_audio)
        
        # Blend vintage and clean audio based on intensity
        if self.vintage_intensity < 1.0:
            clean_ratio = 1.0 - self.vintage_intensity
            vintage_audio = (self.vintage_intensity * vintage_audio + 
                           clean_ratio * audio)
        
        return vintage_audio
    
    def _simulate_analog_frontend_enhanced(self, audio: np.ndarray) -> np.ndarray:
        """Enhanced analog frontend simulation with intensity scaling."""
        # Scale analog artifacts by vintage intensity
        distortion_amount = 0.002 * self.vintage_intensity
        dc_offset = 0.001 * self.vintage_intensity
        
        # Add harmonic distortion
        audio = audio + distortion_amount * np.sign(audio) * (audio ** 2)
        
        # Add DC offset
        audio = audio + dc_offset
        
        # Add subtle thermal noise (higher quality = less noise)
        if self.bit_depth <= 8:
            thermal_noise_level = 0.0001 * self.vintage_intensity
            thermal_noise = np.random.normal(0, thermal_noise_level, len(audio))
            audio = audio + thermal_noise
        
        return audio
    
    def _apply_frequency_response_shaping_enhanced(self, audio: np.ndarray) -> np.ndarray:
        """Enhanced frequency response shaping with quality awareness."""
        if len(audio) <= 1:
            return audio
        
        # Apply vintage frequency response based on intensity
        cutoff_freq = self.max_frequency * (1.0 - self.vintage_intensity * 0.3)
        
        # High-quality filtering for lower vintage intensity
        if self.vintage_intensity < 0.5:
            audio = self._apply_high_quality_lowpass(audio, cutoff_freq)
        else:
            audio = self._apply_vintage_lowpass(audio, cutoff_freq)
        
        # Bass reduction (vintage characteristic)
        bass_cutoff = 200 * (1.0 + self.vintage_intensity * 0.5)
        audio = self._apply_vintage_highpass(audio, bass_cutoff)
        
        # Speech emphasis (intensity-dependent)
        if self.vintage_intensity > 0.3:
            emphasis_gain = 1.0 + (0.2 * self.vintage_intensity)
            audio = self._apply_speech_emphasis_enhanced(audio, emphasis_gain)
        
        return audio
    
    def _apply_enhanced_bit_crushing(self, audio: np.ndarray) -> np.ndarray:
        """Enhanced bit crushing with smart quantization."""
        if self.bit_depth >= 16 and self.vintage_intensity < 0.3:
            return audio  # Skip crushing for high quality, low vintage
        
        # Calculate effective bit depth based on vintage intensity
        effective_bits = self.bit_depth
        if self.vintage_intensity < 1.0:
            # Interpolate between full bit depth and vintage bit depth
            max_bits = 16 if self.bit_depth > 8 else self.bit_depth
            effective_bits = int(self.bit_depth + 
                               (max_bits - self.bit_depth) * (1.0 - self.vintage_intensity))
        
        # Apply quantization
        max_level = 2 ** (effective_bits - 1) - 1
        quantized = np.round(audio * max_level) / max_level
        
        # Add quantization noise (scaled by intensity)
        if self.quantization_noise and self.vintage_intensity > 0:
            noise_amplitude = (1.0 / (2 ** effective_bits)) * 0.5 * self.vintage_intensity
            quantization_noise = np.random.uniform(-noise_amplitude, noise_amplitude, len(audio))
            quantized += quantization_noise
        
        # Apply dithering for smoother quantization (higher quality)
        if self.bit_depth >= 12 and self.vintage_intensity < 0.8:
            dither_amplitude = 1.0 / (2 ** (effective_bits + 1))
            dither = np.random.triangular(-dither_amplitude, 0, dither_amplitude, len(audio))
            quantized += dither
        
        return np.clip(quantized, -1.0, 1.0)
    
    def _apply_vintage_compression_enhanced(self, audio: np.ndarray) -> np.ndarray:
        """Enhanced vintage compression with quality scaling."""
        if len(audio) == 0:
            return audio
        
        # Adjust compression parameters based on vintage intensity
        threshold = 0.8 - (self.vintage_intensity * 0.2)  # Lower threshold for more vintage
        ratio = 2.0 + (self.vintage_intensity * 2.0)  # Higher ratio for more vintage
        
        # Calculate envelope with quality-dependent smoothing
        envelope = np.abs(audio)
        smooth_envelope = np.zeros_like(envelope)
        
        # Adjust attack/release based on quality
        attack_coef = 0.1 * (1.0 + self.vintage_intensity)
        release_coef = 0.001 * (1.0 + self.vintage_intensity * 2.0)
        
        smooth_envelope[0] = envelope[0]
        for i in range(1, len(envelope)):
            if envelope[i] > smooth_envelope[i-1]:
                smooth_envelope[i] = attack_coef * envelope[i] + (1 - attack_coef) * smooth_envelope[i-1]
            else:
                smooth_envelope[i] = release_coef * envelope[i] + (1 - release_coef) * smooth_envelope[i-1]
        
        # Apply compression
        gain_reduction = np.ones_like(smooth_envelope)
        over_threshold = smooth_envelope > threshold
        
        if np.any(over_threshold):
            excess = smooth_envelope[over_threshold] - threshold
            gain_reduction[over_threshold] = threshold / smooth_envelope[over_threshold] * (1.0 + excess / ratio)
        
        return audio * gain_reduction
    
    def _apply_spectral_enhancement(self, audio: np.ndarray) -> np.ndarray:
        """Apply spectral enhancement for improved clarity."""
        if len(audio) <= 1:
            return audio
        
        # Harmonic enhancement in speech frequencies
        enhanced = audio.copy()
        
        # Add subtle harmonic content
        harmonic_gain = 0.05
        enhanced = enhanced + harmonic_gain * np.sin(2 * np.pi * np.arange(len(audio)) / self.sample_rate * 1000)
        
        return enhanced
    
    def _apply_harmonic_enrichment(self, audio: np.ndarray) -> np.ndarray:
        """Apply harmonic enrichment for warmer sound."""
        if len(audio) == 0:
            return audio
        
        # Add subtle even harmonics
        harmonic_amount = 0.01
        enriched = audio + harmonic_amount * (audio ** 2) * np.sign(audio)
        
        return np.clip(enriched, -1.0, 1.0)
    
    def _apply_noise_reduction(self, audio: np.ndarray) -> np.ndarray:
        """Apply intelligent noise reduction."""
        if len(audio) <= 1:
            return audio
        
        # Simple spectral gating
        # Calculate signal energy
        window_size = min(512, len(audio) // 4)
        if window_size < 2:
            return audio
        
        # Apply gentle noise gate
        threshold = 0.01  # -40dB threshold
        gate_ratio = 0.5
        
        windowed_energy = np.convolve(audio ** 2, np.ones(window_size) / window_size, mode='same')
        gate_factor = np.where(windowed_energy < threshold, gate_ratio, 1.0)
        
        return audio * gate_factor
    
    def _apply_temporal_smoothing(self, audio: np.ndarray) -> np.ndarray:
        """Apply temporal smoothing for reduced artifacts."""
        if len(audio) <= 1:
            return audio
        
        # Apply gentle smoothing filter
        kernel_size = 3
        kernel = np.ones(kernel_size) / kernel_size
        smoothed = np.convolve(audio, kernel, mode='same')
        
        # Blend with original based on signal level
        blend_factor = 0.3
        return (1.0 - blend_factor) * audio + blend_factor * smoothed
    
    def _apply_high_quality_lowpass(self, audio: np.ndarray, cutoff_freq: float) -> np.ndarray:
        """Apply high-quality low-pass filter."""
        # Improved filter for higher quality modes
        omega = 2 * np.pi * cutoff_freq / self.sample_rate
        alpha = np.exp(-omega)
        
        # Two-pole filter for better response
        y1 = np.zeros_like(audio)
        y2 = np.zeros_like(audio)
        
        # First pole
        y1[0] = audio[0] * (1 - alpha)
        for i in range(1, len(audio)):
            y1[i] = alpha * y1[i-1] + (1 - alpha) * audio[i]
        
        # Second pole
        y2[0] = y1[0] * (1 - alpha)
        for i in range(1, len(y1)):
            y2[i] = alpha * y2[i-1] + (1 - alpha) * y1[i]
        
        return y2
    
    def _apply_speech_emphasis_enhanced(self, audio: np.ndarray, gain: float) -> np.ndarray:
        """Enhanced speech emphasis with configurable gain."""
        if len(audio) <= 2:
            return audio * gain
        
        # Improved peaking filter
        center_freq = 3000
        bandwidth = 1500
        
        omega_c = 2 * np.pi * center_freq / self.sample_rate
        omega_bw = 2 * np.pi * bandwidth / self.sample_rate
        
        # Better filter implementation
        output = np.zeros_like(audio)
        output[0] = audio[0]
        output[1] = audio[1]
        
        a = 0.95  # Higher Q for better response
        b = (gain - 1.0) * 0.5
        
        for i in range(2, len(audio)):
            resonance = a * np.cos(omega_c) * output[i-1] - a * a * output[i-2]
            output[i] = audio[i] + b * resonance
        
        return output
    
    def _apply_preset_processing(self, audio: np.ndarray) -> np.ndarray:
        """Apply preset-specific processing."""
        if self.vintage_preset == "dr_sbaitso":
            return self.apply_sound_blaster_characteristics(audio)
        elif self.vintage_preset == "dr_sbaitso_enhanced":
            # Enhanced Dr. Sbaitso with better quality
            audio = self.apply_sound_blaster_characteristics(audio)
            if self.bit_depth >= 12:
                # Reduce some artifacts for enhanced version
                audio = self._apply_high_quality_lowpass(audio, 10000)
            return audio
        elif self.vintage_preset == "subtle_vintage":
            # Minimal vintage processing
            audio = self._apply_enhanced_bit_crushing(audio)
            audio = self._apply_high_quality_lowpass(audio, 12000)
            return audio
        else:
            return audio
    
    def update_config(self, config: Dict[str, Any]):
        """Update configuration parameters."""
        vintage_config = config.get('vintage_processing', {})
        advanced_config = config.get('advanced', {})
        
        self.vintage_intensity = vintage_config.get('intensity', self.vintage_intensity)
        self.vintage_enabled = vintage_config.get('enabled', self.vintage_enabled)
        self.vintage_preset = vintage_config.get('preset', self.vintage_preset)
        
        self.spectral_enhancement = advanced_config.get('spectral_enhancement', self.spectral_enhancement)
        self.harmonic_enrichment = advanced_config.get('harmonic_enrichment', self.harmonic_enrichment)
        self.noise_reduction = advanced_config.get('noise_reduction', self.noise_reduction)
        self.temporal_smoothing = advanced_config.get('temporal_smoothing', self.temporal_smoothing)
        
        # Recalculate quality parameters
        self._setup_quality_parameters()
    
    def get_processing_info(self) -> Dict[str, Any]:
        """Get information about current processing configuration."""
        return {
            'vintage_enabled': self.vintage_enabled,
            'vintage_intensity': self.vintage_intensity,
            'vintage_preset': self.vintage_preset,
            'effective_bit_depth': self.bit_depth,
            'max_frequency': self.max_frequency,
            'dynamic_range': self.dynamic_range,
            'spectral_enhancement': self.spectral_enhancement,
            'harmonic_enrichment': self.harmonic_enrichment,
            'noise_reduction': self.noise_reduction,
            'temporal_smoothing': self.temporal_smoothing
        }
