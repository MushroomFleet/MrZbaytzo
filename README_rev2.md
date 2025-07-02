# MR.ZPAYTZO-rev2: Enhanced 1986 Text-to-Speech Engine

**Configurable quality levels while maintaining authentic vintage character**

MR.ZPAYTZO-rev2 is an enhanced version of the original 1986-era text-to-speech synthesis engine that introduces configurable quality levels, advanced processing options, and a flexible configuration system while preserving the distinctive vintage sound that made the original special.

## 🎯 What's New in Rev2

### Quality Presets
- **Authentic 1986**: Original 8-bit Dr. Sbaitso sound (100% vintage)
- **Enhanced Vintage**: 12-bit with improved clarity while maintaining character
- **Modern Retro**: 16-bit high quality with subtle vintage flavor

### Advanced Features
- JSON-based configuration system
- Runtime quality switching
- Configurable vintage intensity (0.0-1.0)
- Advanced audio processing options
- Interactive mode with preset switching
- Enhanced audio output with padding and fade-in/out
- Backward compatibility with rev0

### Technical Improvements
- Configurable bit depth (8/12/16-bit)
- Enhanced formant synthesis (3-5 formants)
- Smart quantization with dithering
- Spectral enhancement options
- Harmonic enrichment
- Noise reduction capabilities
- Temporal smoothing

## 🚀 Quick Start

### Basic Usage

```bash
# Use default settings (Authentic 1986)
python main_rev2.py "Hello world"

# Use Enhanced Vintage preset
python main_rev2.py --preset enhanced_vintage "Better quality speech"

# Use Modern Retro preset for highest quality
python main_rev2.py --preset modern_retro "High quality speech"
```

### Interactive Mode

Interactive mode provides a powerful real-time interface for experimenting with different quality presets and configurations. You can switch between presets instantly and hear the differences in audio quality.

```bash
# Start interactive mode with default preset (Authentic 1986)
python main_rev2.py --interactive

# Start with a specific preset
python main_rev2.py --interactive --preset enhanced_vintage

# Start with custom configuration
python main_rev2.py --interactive --config my_config.json
```

#### Interactive Commands

| Command | Description | Example |
|---------|-------------|---------|
| `:presets` | List all available quality presets with current indicator | `:presets` |
| `:preset <name>` | Switch to a different quality preset in real-time | `:preset modern_retro` |
| `:config` | Display current configuration details | `:config` |
| `:quit` | Exit interactive mode | `:quit` |
| `Ctrl+C` | Alternative way to exit | |

#### Interactive Session Example

```
> :presets
Available Quality Presets:
  Authentic 1986 (current)
    Original Dr. Sbaitso sound with all vintage characteristics

  Enhanced Vintage
    Improved quality while maintaining vintage character

  Modern Retro
    High quality synthesis with subtle vintage flavor

> :preset modern_retro
✓ Switched to preset: modern_retro
Quality Level: Modern Retro
Audio: 22050Hz, 16-bit, 1 channel(s)
Vintage Processing: 0.3 intensity, subtle_vintage preset
Advanced Features: Spectral Enhancement, Harmonic Enrichment, Noise Reduction

> Hello world with high quality audio
[Synthesizes speech with Modern Retro quality]

> :preset authentic_1986
✓ Switched to preset: authentic_1986
Quality Level: Authentic 1986
Audio: 22050Hz, 8-bit, 1 channel(s)
Vintage Processing: 1.0 intensity, dr_sbaitso preset

> Hello world with vintage sound
[Synthesizes speech with authentic 1986 quality]

> :config
=== Current Configuration ===
Quality Level: Authentic 1986
Current Preset: authentic_1986
Audio: 22050Hz, 8-bit, 1 channel(s)
Synthesis: 3 formants, standard precision
Vintage Processing: Enabled, 1.0 intensity

> :quit
```

#### Real-Time Preset Switching Features

- **Instant Quality Changes**: Switch between 8-bit, 12-bit, and 16-bit audio quality
- **Live Configuration Updates**: Audio padding, vintage intensity, and advanced features update automatically
- **No Restart Required**: All changes take effect immediately without restarting the engine
- **Audio Padding Adjustment**: Each preset has optimized silence padding and fade settings:
  - Authentic 1986: 300ms total padding (100ms start + 200ms end)
  - Enhanced Vintage: 400ms total padding (150ms start + 250ms end)
  - Modern Retro: 500ms total padding (200ms start + 300ms end)

#### Interactive Mode Benefits

1. **A/B Testing**: Quickly compare different quality levels with the same text
2. **Configuration Exploration**: Experiment with settings without command-line complexity
3. **Live Demonstration**: Perfect for showcasing the engine's capabilities
4. **Educational Use**: Understand the impact of different vintage processing levels
5. **Development Testing**: Rapid iteration during preset development

### List Available Presets

```bash
python main_rev2.py --list-presets
```

## 📊 Quality Presets Comparison

| Preset | Bit Depth | Vintage Intensity | Formants | Advanced Features | Use Case |
|--------|-----------|-------------------|----------|-------------------|----------|
| **authentic_1986** | 8-bit | 1.0 | 3 | None | Original Dr. Sbaitso experience |
| **enhanced_vintage** | 12-bit | 0.7 | 4 | Spectral Enhancement | Better quality, vintage character |
| **modern_retro** | 16-bit | 0.3 | 5 | All enabled | High quality with vintage flavor |

## ⚙️ Configuration System

### Configuration Files

Rev2 uses JSON configuration files located in the `config/` directory:

- `config/default.json` - Default configuration
- `config/presets/authentic_1986.json` - Original quality preset
- `config/presets/enhanced_vintage.json` - Enhanced quality preset
- `config/presets/modern_retro.json` - Modern quality preset

### Configuration Structure

```json
{
  "audio": {
    "sample_rate": 22050,
    "bit_depth": 12,
    "channels": 1
  },
  "synthesis": {
    "formant_count": 4,
    "formant_precision": "high",
    "diphone_smoothing": true,
    "prosody_enhancement": true
  },
  "vintage_processing": {
    "enabled": true,
    "intensity": 0.7,
    "preset": "dr_sbaitso_enhanced"
  },
  "advanced": {
    "spectral_enhancement": true,
    "harmonic_enrichment": true,
    "noise_reduction": false,
    "temporal_smoothing": true
  }
}
```

### Runtime Configuration

```bash
# Load custom configuration file
python main_rev2.py --config my_config.json "Custom speech"

# Override specific parameters
python main_rev2.py --bit-depth 16 --vintage-intensity 0.5 "Custom quality"
```

## 🎛️ Advanced Usage

### Custom Configuration

Create your own preset by copying and modifying an existing preset file:

```bash
cp config/presets/enhanced_vintage.json config/presets/my_preset.json
# Edit my_preset.json with your preferred settings
python main_rev2.py --config presets/my_preset.json "Custom speech"
```

### Vintage Intensity Control

The vintage intensity parameter (0.0-1.0) controls how much vintage processing is applied:

- **1.0**: Full vintage processing (authentic 1986 sound)
- **0.7**: Moderate vintage character with improved quality
- **0.3**: Subtle vintage flavor with modern clarity
- **0.0**: Clean, modern synthesis (no vintage processing)

```bash
# Adjust vintage intensity
python main_rev2.py --vintage-intensity 0.5 "Half vintage processing"
```

### Advanced Processing Options

Enable advanced features for improved quality:

```json
{
  "advanced": {
    "spectral_enhancement": true,    // Improves clarity in speech frequencies
    "harmonic_enrichment": true,     // Adds warmth and richness
    "noise_reduction": true,         // Reduces background artifacts
    "temporal_smoothing": true       // Smooths transitions between sounds
  }
}
```

## 🔧 Command Line Reference

### Basic Options

```bash
python main_rev2.py [OPTIONS] "text to speak"
```

| Option | Description |
|--------|-------------|
| `--preset, -p` | Quality preset (authentic_1986, enhanced_vintage, modern_retro) |
| `--config, -c` | Configuration file to load |
| `--interactive, -i` | Interactive mode |
| `--verbose, -v` | Verbose output showing processing stages |

### Audio Options

| Option | Description |
|--------|-------------|
| `--sample-rate` | Sample rate (8000-48000 Hz) |
| `--bit-depth` | Bit depth (8, 12, or 16 bits) |
| `--vintage-intensity` | Vintage processing intensity (0.0-1.0) |

### Information Options

| Option | Description |
|--------|-------------|
| `--list-presets` | List available quality presets |
| `--print-config` | Print current configuration |

## 🧪 Testing

Run the comprehensive test suite to verify all features:

```bash
python test_rev2.py
```

The test suite covers:
- Configuration system functionality
- Quality preset loading and switching
- Runtime configuration changes
- Advanced processing features
- Backward compatibility with rev0

### Audio Padding Test

Test the enhanced audio output with padding to verify clipping prevention:

```bash
python test_audio_padding.py
```

This test verifies:
- Configurable silence padding at start and end of speech
- Fade-in/fade-out to prevent audio clicks and pops
- Quality-specific padding settings for each preset
- Audio clipping prevention and level analysis

### Interactive Mode Test

Test the interactive mode functionality and preset switching:

```bash
python test_interactive.py
```

This test verifies:
- Real-time preset switching between all quality levels
- Interactive command functionality (`:presets`, `:preset`, `:config`, `:quit`)
- Audio padding configuration updates when switching presets
- Speech synthesis with different presets in interactive mode
- Configuration display and preset listing features

## 🔄 Migration from Rev0

Rev2 is fully backward compatible with rev0. By default, it uses the "Authentic 1986" preset which provides identical behavior to the original version.

### Gradual Quality Improvement

1. **Start with Authentic 1986**: Identical to rev0
   ```bash
   python main_rev2.py "Hello world"  # Same as rev0
   ```

2. **Try Enhanced Vintage**: Better quality, vintage character
   ```bash
   python main_rev2.py --preset enhanced_vintage "Hello world"
   ```

3. **Explore Modern Retro**: High quality with vintage flavor
   ```bash
   python main_rev2.py --preset modern_retro "Hello world"
   ```

### Rev0 vs Rev2 Command Comparison

| Rev0 | Rev2 Equivalent |
|------|-----------------|
| `python main.py "text"` | `python main_rev2.py "text"` |
| `python main.py --bit-depth 8 "text"` | `python main_rev2.py --preset authentic_1986 "text"` |
| `python main.py --interactive` | `python main_rev2.py --interactive` |

## 🎵 Audio Quality Characteristics

### Authentic 1986 (8-bit)
- **Dynamic Range**: 48 dB
- **Frequency Response**: Limited to 8 kHz
- **Quantization**: 256 levels with noise
- **Character**: Full vintage artifacts, authentic Dr. Sbaitso sound

### Enhanced Vintage (12-bit)
- **Dynamic Range**: 72 dB
- **Frequency Response**: Extended to 11 kHz
- **Quantization**: 4096 levels with smart dithering
- **Character**: Improved clarity while maintaining vintage feel

### Modern Retro (16-bit)
- **Dynamic Range**: 96 dB
- **Frequency Response**: Up to 16 kHz
- **Quantization**: 65536 levels with advanced processing
- **Character**: High quality with subtle vintage warmth

## 🛠️ Technical Architecture

### Core Components

1. **ConfigManager**: JSON configuration loading and validation
2. **EnhancedVintageDSP**: Configurable vintage audio processing
3. **ZPaytzoEngineRev2**: Main engine with preset support
4. **Quality Presets**: Predefined configuration sets

### Processing Pipeline

```
Text Input → Text Processor → Phoneme Converter → Diphone Synthesizer → Enhanced Vintage DSP → Audio Output
                                                                              ↑
                                                                    Configuration System
```

### Advanced DSP Features

- **Configurable Formant Synthesis**: 3-5 formants for improved vowel clarity
- **Smart Quantization**: Adaptive bit crushing with dithering
- **Spectral Enhancement**: Harmonic enrichment in speech frequencies
- **Temporal Processing**: Smoothing and noise reduction
- **Vintage Intensity Blending**: Mix clean and vintage processing

## 📝 Configuration Examples

### Custom High-Quality Preset

```json
{
  "name": "Studio Quality",
  "description": "Maximum quality with minimal vintage processing",
  "audio": {
    "sample_rate": 22050,
    "bit_depth": 16,
    "channels": 1
  },
  "synthesis": {
    "formant_count": 5,
    "formant_precision": "ultra",
    "diphone_smoothing": true,
    "prosody_enhancement": true
  },
  "vintage_processing": {
    "enabled": true,
    "intensity": 0.1,
    "preset": "subtle_vintage"
  },
  "advanced": {
    "spectral_enhancement": true,
    "harmonic_enrichment": true,
    "noise_reduction": true,
    "temporal_smoothing": true
  }
}
```

### Extreme Vintage Preset

```json
{
  "name": "Ultra Vintage",
  "description": "Maximum vintage character with heavy processing",
  "audio": {
    "sample_rate": 22050,
    "bit_depth": 8,
    "channels": 1
  },
  "vintage_processing": {
    "enabled": true,
    "intensity": 1.0,
    "preset": "dr_sbaitso",
    "quantization_noise": true,
    "analog_simulation": true,
    "frequency_response_shaping": true
  },
  "advanced": {
    "spectral_enhancement": false,
    "harmonic_enrichment": false,
    "noise_reduction": false,
    "temporal_smoothing": false
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing sounddevice module**
   ```bash
   pip install sounddevice
   ```

2. **Configuration validation errors**
   ```bash
   python main_rev2.py --print-config  # Check current config
   ```

3. **Preset not found**
   ```bash
   python main_rev2.py --list-presets  # See available presets
   ```

### Performance Optimization

For better performance on slower systems:

```bash
# Use fast performance mode
python main_rev2.py --preset authentic_1986 "text"  # Fastest

# Or configure manually
python main_rev2.py --bit-depth 8 --vintage-intensity 1.0 "text"
```

## 📚 API Reference

### ZPaytzoEngineRev2 Class

```python
from main_rev2 import ZPaytzoEngineRev2

# Initialize with preset
engine = ZPaytzoEngineRev2(preset="enhanced_vintage")

# Synthesize speech
engine.speak("Hello world", verbose=True)

# Change preset at runtime
engine.set_preset("modern_retro")

# Configure individual parameters
engine.configure('vintage_processing', 'intensity', 0.5)

# Get quality information
info = engine.get_quality_info()
print(f"Current quality: {info['quality_level']}")
```

### ConfigManager Class

```python
from src.config_manager import ConfigManager

# Initialize configuration manager
config = ConfigManager()

# Load preset
config.load_preset("enhanced_vintage")

# Get configuration sections
audio_config = config.get_audio_config()
vintage_config = config.get_vintage_config()

# Validate configuration
errors = config.validate_config()
```

## 🎯 Future Enhancements

Potential areas for future development:

- **Voice Personas**: Multiple character voices (male/female/robotic)
- **SSML Support**: Speech Synthesis Markup Language
- **Real-time Processing**: Live audio streaming
- **Plugin System**: Extensible effect processing
- **GUI Interface**: Graphical configuration tool
- **Batch Processing**: Multiple file synthesis
- **Export Formats**: WAV, MP3, OGG output options

## 📄 License

Same license as the original MR.ZPAYTZO project.

## 🙏 Acknowledgments

- Original Dr. Sbaitso TTS engine inspiration
- 1986-era speech synthesis research
- Modern audio processing techniques
- Community feedback and testing

---

**MR.ZPAYTZO-rev2**: Where vintage character meets modern quality. 🎙️✨
