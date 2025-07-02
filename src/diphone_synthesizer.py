"""
Diphone Concatenation Synthesizer for MR.ZPAYTZO-rev0
Implements 1986-era diphone concatenation synthesis using ~800-1000 diphones
"""

import numpy as np
import math
from typing import List, Dict, Tuple, Optional
import os


class DiphoneSynthesizer:
    """
    Diphone concatenation synthesis engine implementing vintage TTS audio generation.
    Based on First Byte Monologue engine using ~800-1000 diphones for American English.
    
    Stores diphones as acoustic transitions from phoneme center to phoneme center,
    capturing natural coarticulation effects in a compact ~200KB database.
    """
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.diphone_database = self._initialize_diphone_database()
        self.phoneme_durations = self._load_phoneme_durations()
        self.formant_frequencies = self._load_formant_frequencies()
        
        # 1986-era synthesis parameters
        self.fundamental_frequency = 120.0  # Average male voice F0
        self.formant_bandwidth = 100.0      # Formant bandwidth in Hz
        self.synthesis_quality = 'vintage'   # Emphasis on authentic 1986 sound
        
    def synthesize(self, phonemes: List[str]) -> np.ndarray:
        """
        Generate audio from phoneme sequence using diphone concatenation.
        
        Args:
            phonemes: List of phonemes in ARPABET notation
            
        Returns:
            Audio samples as numpy array (float32, normalized -1 to 1)
        """
        if not phonemes:
            return np.array([], dtype=np.float32)
        
        # Convert phonemes to diphone sequence
        diphones = self._phonemes_to_diphones(phonemes)
        
        # Synthesize each diphone and concatenate
        audio_segments = []
        
        for diphone in diphones:
            if diphone.startswith('<PAUSE'):
                # Handle pause markers
                pause_duration = self._get_pause_duration(diphone)
                silence = np.zeros(int(pause_duration * self.sample_rate), dtype=np.float32)
                audio_segments.append(silence)
            else:
                # Synthesize diphone using formant synthesis
                audio_segment = self._synthesize_diphone(diphone)
                audio_segments.append(audio_segment)
        
        # Concatenate all segments
        if audio_segments:
            audio = np.concatenate(audio_segments)
        else:
            audio = np.array([], dtype=np.float32)
        
        # Apply 1986-era post-processing
        audio = self._apply_vintage_processing(audio)
        
        return audio
    
    def _phonemes_to_diphones(self, phonemes: List[str]) -> List[str]:
        """Convert phoneme sequence to diphone sequence."""
        diphones = []
        
        # Add silence at beginning
        if phonemes and not phonemes[0].startswith('<PAUSE'):
            diphones.append('SIL-' + phonemes[0])
        
        # Generate diphones between adjacent phonemes
        for i in range(len(phonemes) - 1):
            current_phoneme = phonemes[i]
            next_phoneme = phonemes[i + 1]
            
            # Handle pause markers
            if current_phoneme.startswith('<PAUSE') or next_phoneme.startswith('<PAUSE'):
                diphones.append(current_phoneme)
                continue
            
            # Create diphone name
            diphone = f"{current_phoneme}-{next_phoneme}"
            diphones.append(diphone)
        
        # Add final diphone to silence
        if phonemes and not phonemes[-1].startswith('<PAUSE'):
            diphones.append(phonemes[-1] + '-SIL')
        
        return diphones
    
    def _synthesize_diphone(self, diphone: str) -> np.ndarray:
        """
        Synthesize a single diphone using 1986-era formant synthesis.
        
        Args:
            diphone: Diphone name (e.g., 'AE-N', 'SIL-HH')
            
        Returns:
            Audio segment for the diphone
        """
        # Parse diphone
        if '-' in diphone:
            start_phoneme, end_phoneme = diphone.split('-', 1)
        else:
            start_phoneme = end_phoneme = diphone
        
        # Get phoneme characteristics
        start_formants = self.formant_frequencies.get(start_phoneme, self._get_default_formants())
        end_formants = self.formant_frequencies.get(end_phoneme, self._get_default_formants())
        
        # Calculate duration (1986-era approach: fixed durations)
        duration = self._get_diphone_duration(start_phoneme, end_phoneme)
        num_samples = int(duration * self.sample_rate)
        
        if num_samples <= 0:
            return np.array([], dtype=np.float32)
        
        # Generate time vector
        t = np.linspace(0, duration, num_samples, endpoint=False)
        
        # Synthesize using vintage formant synthesis
        audio = self._formant_synthesis(t, start_formants, end_formants, start_phoneme, end_phoneme)
        
        return audio.astype(np.float32)
    
    def _formant_synthesis(self, t: np.ndarray, start_formants: Dict, end_formants: Dict, 
                          start_phoneme: str, end_phoneme: str) -> np.ndarray:
        """
        Vintage formant synthesis implementing 1986-era algorithms.
        
        Uses three formants (F1, F2, F3) with simple harmonic generation
        and basic amplitude modulation.
        """
        if len(t) == 0:
            return np.array([])
        
        # Initialize output
        audio = np.zeros_like(t)
        
        # Check if either phoneme is unvoiced
        is_voiced_start = self._is_voiced_phoneme(start_phoneme)
        is_voiced_end = self._is_voiced_phoneme(end_phoneme)
        
        # Transition voicing across the diphone
        voicing = np.linspace(float(is_voiced_start), float(is_voiced_end), len(t))
        
        # Generate fundamental frequency contour (simple linear interpolation)
        f0_start = self.fundamental_frequency if is_voiced_start else 0
        f0_end = self.fundamental_frequency if is_voiced_end else 0
        f0 = np.linspace(f0_start, f0_end, len(t))
        
        # Generate formant frequency contours
        f1 = np.linspace(start_formants['F1'], end_formants['F1'], len(t))
        f2 = np.linspace(start_formants['F2'], end_formants['F2'], len(t))
        f3 = np.linspace(start_formants['F3'], end_formants['F3'], len(t))
        
        # Generate formant amplitudes (simplified 1986 approach)
        a1 = np.linspace(start_formants['A1'], end_formants['A1'], len(t))
        a2 = np.linspace(start_formants['A2'], end_formants['A2'], len(t))
        a3 = np.linspace(start_formants['A3'], end_formants['A3'], len(t))
        
        # Generate source signal
        if np.any(voicing > 0):
            # Voiced: generate pulse train with harmonics
            source = self._generate_pulse_train(t, f0, voicing)
        else:
            # Unvoiced: generate noise
            source = self._generate_noise(t, start_phoneme, end_phoneme)
        
        # Apply formant filtering (simplified resonator bank)
        formant1 = self._apply_formant_filter(source, f1, a1, self.formant_bandwidth)
        formant2 = self._apply_formant_filter(source, f2, a2, self.formant_bandwidth)
        formant3 = self._apply_formant_filter(source, f3, a3, self.formant_bandwidth)
        
        # Mix formants (1986-era simple addition)
        audio = 0.5 * formant1 + 0.3 * formant2 + 0.2 * formant3
        
        # Apply amplitude envelope
        envelope = self._generate_amplitude_envelope(len(t), start_phoneme, end_phoneme)
        audio *= envelope
        
        # Normalize to prevent clipping
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.8
        
        return audio
    
    def _generate_pulse_train(self, t: np.ndarray, f0: np.ndarray, voicing: np.ndarray) -> np.ndarray:
        """Generate voiced source using pulse train (1986-era approach)."""
        # Simple sawtooth wave approximation for vocal fold vibration
        phase = np.zeros_like(t)
        
        # Integrate frequency to get phase
        dt = t[1] - t[0] if len(t) > 1 else 1.0 / self.sample_rate
        phase[1:] = np.cumsum(f0[:-1] * dt) * 2 * np.pi
        
        # Generate sawtooth wave
        sawtooth = 2 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5))
        
        # Apply voicing modulation
        source = sawtooth * voicing
        
        return source
    
    def _generate_noise(self, t: np.ndarray, start_phoneme: str, end_phoneme: str) -> np.ndarray:
        """Generate unvoiced source using filtered noise."""
        # White noise for unvoiced sounds
        noise = np.random.normal(0, 1, len(t))
        
        # Apply spectral shaping based on phoneme type
        if any(p in ['S', 'SH', 'F', 'TH'] for p in [start_phoneme, end_phoneme]):
            # High-frequency emphasis for fricatives
            noise = self._apply_highpass_filter(noise, 2000)
        elif any(p in ['P', 'T', 'K'] for p in [start_phoneme, end_phoneme]):
            # Burst characteristics for stops
            noise = self._apply_burst_shaping(noise)
        
        return noise
    
    def _apply_formant_filter(self, source: np.ndarray, formant_freq: np.ndarray, 
                            amplitude: np.ndarray, bandwidth: float) -> np.ndarray:
        """Apply formant resonance using simple IIR filter approximation."""
        if len(source) == 0:
            return source
        
        output = np.zeros_like(source)
        
        # Time-varying formant filter (simplified)
        for i in range(len(source)):
            freq = formant_freq[i]
            amp = amplitude[i]
            
            # Simple resonator approximation
            if freq > 0:
                # Convert to normalized frequency
                omega = 2 * np.pi * freq / self.sample_rate
                
                # Simple bandpass filter coefficients
                r = 1 - (bandwidth / self.sample_rate)  # Pole radius
                
                # Apply resonance (simplified single-sample approach)
                if i >= 2:
                    # Second-order IIR approximation
                    output[i] = (amp * source[i] + 
                               2 * r * np.cos(omega) * output[i-1] - 
                               r * r * output[i-2])
                else:
                    output[i] = amp * source[i]
        
        return output
    
    def _apply_highpass_filter(self, signal: np.ndarray, cutoff_freq: float) -> np.ndarray:
        """Apply simple high-pass filter for fricative shaping."""
        if len(signal) <= 1:
            return signal
        
        # Simple first-order high-pass filter
        omega = 2 * np.pi * cutoff_freq / self.sample_rate
        alpha = np.exp(-omega)
        
        output = np.zeros_like(signal)
        output[0] = signal[0]
        
        for i in range(1, len(signal)):
            output[i] = alpha * output[i-1] + alpha * (signal[i] - signal[i-1])
        
        return output
    
    def _apply_burst_shaping(self, noise: np.ndarray) -> np.ndarray:
        """Apply burst characteristics for stop consonants."""
        # Apply exponential decay envelope for burst
        decay_samples = min(len(noise) // 4, 100)
        envelope = np.ones_like(noise)
        
        if decay_samples > 0:
            envelope[:decay_samples] = np.exp(-np.linspace(0, 3, decay_samples))
        
        return noise * envelope
    
    def _generate_amplitude_envelope(self, num_samples: int, start_phoneme: str, end_phoneme: str) -> np.ndarray:
        """Generate amplitude envelope for diphone."""
        envelope = np.ones(num_samples)
        
        if num_samples <= 1:
            return envelope
        
        # Apply attack and decay based on phoneme types
        attack_samples = min(num_samples // 8, 50)
        decay_samples = min(num_samples // 8, 50)
        
        # Attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        if decay_samples > 0:
            envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
        
        return envelope
    
    def _is_voiced_phoneme(self, phoneme: str) -> bool:
        """Check if phoneme is voiced."""
        voiced_phonemes = {
            'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW',
            'B', 'D', 'G', 'V', 'DH', 'Z', 'ZH', 'JH', 'M', 'N', 'NG', 'L', 'R', 'W', 'Y'
        }
        return phoneme in voiced_phonemes
    
    def _get_diphone_duration(self, start_phoneme: str, end_phoneme: str) -> float:
        """Get duration for diphone (1986-era fixed durations)."""
        # Simplified duration model
        base_duration = 0.08  # 80ms base duration
        
        # Adjust based on phoneme types
        if start_phoneme == 'SIL' or end_phoneme == 'SIL':
            return base_duration * 0.5  # Shorter for silence transitions
        
        # Vowels are longer
        if start_phoneme in self.phoneme_durations:
            duration = self.phoneme_durations[start_phoneme]
        else:
            duration = base_duration
        
        return duration
    
    def _get_pause_duration(self, pause_marker: str) -> float:
        """Get duration for pause markers."""
        if 'LONG' in pause_marker:
            return 0.5  # 500ms
        elif 'MEDIUM' in pause_marker:
            return 0.3  # 300ms
        elif 'SHORT' in pause_marker:
            return 0.2  # 200ms
        else:
            return 0.3  # Default
    
    def _apply_vintage_processing(self, audio: np.ndarray) -> np.ndarray:
        """Apply vintage-style processing to maintain 1986 character."""
        if len(audio) == 0:
            return audio
        
        # Slight low-pass filtering to simulate limited bandwidth
        if len(audio) > 1:
            # Simple moving average filter
            kernel_size = 3
            kernel = np.ones(kernel_size) / kernel_size
            audio = np.convolve(audio, kernel, mode='same')
        
        # Add very subtle quantization noise (8-bit character)
        quantization_levels = 256  # 8-bit
        audio = np.round(audio * quantization_levels / 2) * 2 / quantization_levels
        
        return audio
    
    def _initialize_diphone_database(self) -> Dict:
        """Initialize diphone database structure."""
        # In a full implementation, this would load pre-recorded diphones
        # For now, we'll use algorithmic generation
        return {}
    
    def _load_phoneme_durations(self) -> Dict[str, float]:
        """Load typical phoneme durations (in seconds)."""
        return {
            # Vowels (longer)
            'AA': 0.12, 'AE': 0.10, 'AH': 0.08, 'AO': 0.12, 'AW': 0.14, 'AY': 0.14,
            'EH': 0.10, 'ER': 0.12, 'EY': 0.14, 'IH': 0.08, 'IY': 0.12, 'OW': 0.14,
            'OY': 0.14, 'UH': 0.08, 'UW': 0.12,
            
            # Consonants (shorter)
            'B': 0.06, 'CH': 0.08, 'D': 0.04, 'DH': 0.06, 'F': 0.08, 'G': 0.06,
            'HH': 0.06, 'JH': 0.08, 'K': 0.06, 'L': 0.06, 'M': 0.06, 'N': 0.06,
            'NG': 0.08, 'P': 0.06, 'R': 0.06, 'S': 0.08, 'SH': 0.08, 'T': 0.04,
            'TH': 0.08, 'V': 0.06, 'W': 0.06, 'Y': 0.06, 'Z': 0.06, 'ZH': 0.08,
            
            # Special
            'SIL': 0.02
        }
    
    def _load_formant_frequencies(self) -> Dict[str, Dict[str, float]]:
        """Load formant frequencies for each phoneme (1986-era values)."""
        return {
            # Vowels with F1, F2, F3 frequencies and amplitudes
            'AA': {'F1': 730, 'F2': 1090, 'F3': 2440, 'A1': 1.0, 'A2': 0.6, 'A3': 0.3},  # father
            'AE': {'F1': 660, 'F2': 1720, 'F3': 2410, 'A1': 1.0, 'A2': 0.8, 'A3': 0.3},  # cat
            'AH': {'F1': 520, 'F2': 1190, 'F3': 2390, 'A1': 1.0, 'A2': 0.5, 'A3': 0.2},  # but
            'AO': {'F1': 570, 'F2': 840, 'F3': 2410, 'A1': 1.0, 'A2': 0.4, 'A3': 0.2},   # bought
            'EH': {'F1': 530, 'F2': 1840, 'F3': 2480, 'A1': 1.0, 'A2': 0.7, 'A3': 0.3},  # bed
            'ER': {'F1': 490, 'F2': 1350, 'F3': 1690, 'A1': 1.0, 'A2': 0.6, 'A3': 0.4},  # bird
            'IH': {'F1': 390, 'F2': 1990, 'F3': 2550, 'A1': 1.0, 'A2': 0.8, 'A3': 0.3},  # bit
            'IY': {'F1': 270, 'F2': 2290, 'F3': 3010, 'A1': 1.0, 'A2': 0.9, 'A3': 0.4},  # beat
            'OW': {'F1': 570, 'F2': 840, 'F3': 2410, 'A1': 1.0, 'A2': 0.4, 'A3': 0.2},   # boat
            'UH': {'F1': 440, 'F2': 1020, 'F3': 2240, 'A1': 1.0, 'A2': 0.4, 'A3': 0.2},  # book
            'UW': {'F1': 300, 'F2': 870, 'F3': 2240, 'A1': 1.0, 'A2': 0.3, 'A3': 0.2},   # boot
            
            # Diphthongs
            'AY': {'F1': 660, 'F2': 1720, 'F3': 2410, 'A1': 1.0, 'A2': 0.8, 'A3': 0.3},  # bite
            'AW': {'F1': 730, 'F2': 1090, 'F3': 2440, 'A1': 1.0, 'A2': 0.6, 'A3': 0.3},  # bout
            'EY': {'F1': 530, 'F2': 1840, 'F3': 2480, 'A1': 1.0, 'A2': 0.7, 'A3': 0.3},  # bait
            'OY': {'F1': 570, 'F2': 840, 'F3': 2410, 'A1': 1.0, 'A2': 0.4, 'A3': 0.2},   # boy
            
            # Consonants (formant targets during transitions)
            'B': {'F1': 200, 'F2': 1000, 'F3': 2500, 'A1': 0.3, 'A2': 0.2, 'A3': 0.1},
            'D': {'F1': 200, 'F2': 1700, 'F3': 2600, 'A1': 0.3, 'A2': 0.2, 'A3': 0.1},
            'G': {'F1': 200, 'F2': 1400, 'F3': 2200, 'A1': 0.3, 'A2': 0.2, 'A3': 0.1},
            'P': {'F1': 200, 'F2': 1000, 'F3': 2500, 'A1': 0.1, 'A2': 0.1, 'A3': 0.05},
            'T': {'F1': 200, 'F2': 1700, 'F3': 2600, 'A1': 0.1, 'A2': 0.1, 'A3': 0.05},
            'K': {'F1': 200, 'F2': 1400, 'F3': 2200, 'A1': 0.1, 'A2': 0.1, 'A3': 0.05},
            'M': {'F1': 250, 'F2': 1000, 'F3': 2200, 'A1': 0.8, 'A2': 0.3, 'A3': 0.2},
            'N': {'F1': 250, 'F2': 1700, 'F3': 2600, 'A1': 0.8, 'A2': 0.3, 'A3': 0.2},
            'NG': {'F1': 250, 'F2': 1400, 'F3': 2200, 'A1': 0.8, 'A2': 0.3, 'A3': 0.2},
            'L': {'F1': 400, 'F2': 1200, 'F3': 2600, 'A1': 0.9, 'A2': 0.5, 'A3': 0.3},
            'R': {'F1': 300, 'F2': 1300, 'F3': 1600, 'A1': 0.9, 'A2': 0.5, 'A3': 0.4},
            'W': {'F1': 300, 'F2': 870, 'F3': 2240, 'A1': 0.8, 'A2': 0.3, 'A3': 0.2},
            'Y': {'F1': 270, 'F2': 2290, 'F3': 3010, 'A1': 0.8, 'A2': 0.7, 'A3': 0.3},
            
            # Fricatives
            'F': {'F1': 200, 'F2': 1000, 'F3': 4000, 'A1': 0.2, 'A2': 0.3, 'A3': 0.8},
            'V': {'F1': 200, 'F2': 1000, 'F3': 4000, 'A1': 0.4, 'A2': 0.4, 'A3': 0.6},
            'TH': {'F1': 200, 'F2': 1400, 'F3': 4500, 'A1': 0.2, 'A2': 0.3, 'A3': 0.8},
            'DH': {'F1': 200, 'F2': 1400, 'F3': 4500, 'A1': 0.4, 'A2': 0.4, 'A3': 0.6},
            'S': {'F1': 200, 'F2': 2000, 'F3': 6000, 'A1': 0.1, 'A2': 0.5, 'A3': 1.0},
            'Z': {'F1': 200, 'F2': 2000, 'F3': 6000, 'A1': 0.3, 'A2': 0.6, 'A3': 0.8},
            'SH': {'F1': 200, 'F2': 1200, 'F3': 4000, 'A1': 0.1, 'A2': 0.3, 'A3': 0.9},
            'ZH': {'F1': 200, 'F2': 1200, 'F3': 4000, 'A1': 0.3, 'A2': 0.4, 'A3': 0.7},
            'CH': {'F1': 200, 'F2': 1200, 'F3': 4000, 'A1': 0.1, 'A2': 0.3, 'A3': 0.8},
            'JH': {'F1': 200, 'F2': 1200, 'F3': 4000, 'A1': 0.3, 'A2': 0.4, 'A3': 0.6},
            'HH': {'F1': 300, 'F2': 1500, 'F3': 3000, 'A1': 0.3, 'A2': 0.2, 'A3': 0.1},
            
            # Silence
            'SIL': {'F1': 0, 'F2': 0, 'F3': 0, 'A1': 0.0, 'A2': 0.0, 'A3': 0.0}
        }
    
    def _get_default_formants(self) -> Dict[str, float]:
        """Return default formant values for unknown phonemes."""
        return {'F1': 500, 'F2': 1500, 'F3': 2500, 'A1': 0.5, 'A2': 0.3, 'A3': 0.1}
