"""
Configuration Manager for MR.ZPAYTZO-rev2
Handles JSON configuration loading, validation, and preset management
"""

import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path


class ConfigManager:
    """
    Configuration management system for MR.ZPAYTZO-rev2.
    
    Provides centralized configuration loading, validation, and preset management
    with backward compatibility for rev0 behavior.
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.presets_dir = self.config_dir / "presets"
        self.current_config = {}
        self.available_presets = {}
        
        # Load default configuration
        self._load_default_config()
        self._load_available_presets()
    
    def _load_default_config(self):
        """Load the default configuration."""
        default_config_path = self.config_dir / "default.json"
        
        if default_config_path.exists():
            try:
                with open(default_config_path, 'r') as f:
                    self.current_config = json.load(f)
                print(f"Loaded default configuration from {default_config_path}")
            except Exception as e:
                print(f"Error loading default config: {e}")
                self.current_config = self._get_fallback_config()
        else:
            print("Default config not found, using fallback configuration")
            self.current_config = self._get_fallback_config()
    
    def _load_available_presets(self):
        """Load all available quality presets."""
        if not self.presets_dir.exists():
            print("Presets directory not found")
            return
        
        for preset_file in self.presets_dir.glob("*.json"):
            try:
                with open(preset_file, 'r') as f:
                    preset_data = json.load(f)
                    preset_name = preset_file.stem
                    self.available_presets[preset_name] = preset_data
                    print(f"Loaded preset: {preset_name}")
            except Exception as e:
                print(f"Error loading preset {preset_file}: {e}")
    
    def _get_fallback_config(self) -> Dict[str, Any]:
        """Return fallback configuration for rev0 compatibility."""
        return {
            "version": "2.0",
            "audio": {
                "sample_rate": 22050,
                "bit_depth": 8,
                "channels": 1,
                "buffer_size": 1024
            },
            "synthesis": {
                "formant_count": 3,
                "formant_precision": "standard",
                "diphone_smoothing": False,
                "prosody_enhancement": False
            },
            "vintage_processing": {
                "enabled": True,
                "intensity": 1.0,
                "preset": "dr_sbaitso"
            },
            "quality": {
                "preset": "authentic_1986",
                "adaptive_quality": False
            }
        }
    
    def load_preset(self, preset_name: str) -> bool:
        """
        Load a quality preset.
        
        Args:
            preset_name: Name of the preset to load
            
        Returns:
            True if preset was loaded successfully, False otherwise
        """
        if preset_name not in self.available_presets:
            print(f"Preset '{preset_name}' not found")
            return False
        
        try:
            preset_config = self.available_presets[preset_name].copy()
            
            # Remove metadata fields
            preset_config.pop('name', None)
            preset_config.pop('description', None)
            
            # Merge preset with current config
            self.current_config = self._merge_configs(self.current_config, preset_config)
            self.current_config['quality']['preset'] = preset_name
            
            print(f"Loaded preset: {preset_name}")
            return True
            
        except Exception as e:
            print(f"Error loading preset '{preset_name}': {e}")
            return False
    
    def _merge_configs(self, base_config: Dict, override_config: Dict) -> Dict:
        """Recursively merge configuration dictionaries."""
        result = base_config.copy()
        
        for key, value in override_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Get configuration values.
        
        Args:
            section: Specific section to retrieve, or None for entire config
            
        Returns:
            Configuration dictionary or section
        """
        if section is None:
            return self.current_config.copy()
        
        return self.current_config.get(section, {})
    
    def set_config(self, section: str, key: str, value: Any) -> bool:
        """
        Set a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
            
        Returns:
            True if value was set successfully
        """
        try:
            if section not in self.current_config:
                self.current_config[section] = {}
            
            self.current_config[section][key] = value
            return True
            
        except Exception as e:
            print(f"Error setting config {section}.{key}: {e}")
            return False
    
    def get_audio_config(self) -> Dict[str, Any]:
        """Get audio configuration parameters."""
        return self.get_config('audio')
    
    def get_synthesis_config(self) -> Dict[str, Any]:
        """Get synthesis configuration parameters."""
        return self.get_config('synthesis')
    
    def get_vintage_config(self) -> Dict[str, Any]:
        """Get vintage processing configuration parameters."""
        return self.get_config('vintage_processing')
    
    def get_prosody_config(self) -> Dict[str, Any]:
        """Get prosody configuration parameters."""
        return self.get_config('prosody')
    
    def get_advanced_config(self) -> Dict[str, Any]:
        """Get advanced processing configuration parameters."""
        return self.get_config('advanced')
    
    def list_presets(self) -> List[Dict[str, str]]:
        """
        List available quality presets.
        
        Returns:
            List of preset information dictionaries
        """
        presets = []
        for name, config in self.available_presets.items():
            presets.append({
                'name': name,
                'display_name': config.get('name', name),
                'description': config.get('description', 'No description available')
            })
        return presets
    
    def get_current_preset(self) -> str:
        """Get the name of the currently loaded preset."""
        return self.current_config.get('quality', {}).get('preset', 'custom')
    
    def validate_config(self) -> List[str]:
        """
        Validate current configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate audio settings
        audio_config = self.get_audio_config()
        
        sample_rate = audio_config.get('sample_rate', 22050)
        if not (8000 <= sample_rate <= 48000):
            errors.append(f"Invalid sample rate: {sample_rate} (must be 8000-48000)")
        
        bit_depth = audio_config.get('bit_depth', 8)
        if bit_depth not in [8, 12, 16]:
            errors.append(f"Invalid bit depth: {bit_depth} (must be 8, 12, or 16)")
        
        channels = audio_config.get('channels', 1)
        if channels not in [1, 2]:
            errors.append(f"Invalid channels: {channels} (must be 1 or 2)")
        
        # Validate synthesis settings
        synthesis_config = self.get_synthesis_config()
        
        formant_count = synthesis_config.get('formant_count', 3)
        if not (3 <= formant_count <= 5):
            errors.append(f"Invalid formant count: {formant_count} (must be 3-5)")
        
        # Validate vintage processing settings
        vintage_config = self.get_vintage_config()
        
        intensity = vintage_config.get('intensity', 1.0)
        if not (0.0 <= intensity <= 1.0):
            errors.append(f"Invalid vintage intensity: {intensity} (must be 0.0-1.0)")
        
        return errors
    
    def save_config(self, filename: str) -> bool:
        """
        Save current configuration to file.
        
        Args:
            filename: Name of file to save to
            
        Returns:
            True if saved successfully
        """
        try:
            config_path = self.config_dir / filename
            with open(config_path, 'w') as f:
                json.dump(self.current_config, f, indent=2)
            print(f"Configuration saved to {config_path}")
            return True
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def load_config_file(self, filename: str) -> bool:
        """
        Load configuration from file.
        
        Args:
            filename: Name of file to load from
            
        Returns:
            True if loaded successfully
        """
        try:
            config_path = self.config_dir / filename
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
            
            # Validate loaded configuration
            temp_config = self.current_config
            self.current_config = loaded_config
            errors = self.validate_config()
            
            if errors:
                print(f"Configuration validation failed: {errors}")
                self.current_config = temp_config
                return False
            
            print(f"Configuration loaded from {config_path}")
            return True
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self._load_default_config()
        print("Configuration reset to defaults")
    
    def get_quality_level(self) -> str:
        """
        Get a human-readable quality level description.
        
        Returns:
            Quality level string
        """
        bit_depth = self.get_audio_config().get('bit_depth', 8)
        vintage_intensity = self.get_vintage_config().get('intensity', 1.0)
        smoothing = self.get_synthesis_config().get('diphone_smoothing', False)
        
        if bit_depth == 8 and vintage_intensity >= 0.9 and not smoothing:
            return "Authentic 1986"
        elif bit_depth <= 12 and vintage_intensity >= 0.5:
            return "Enhanced Vintage"
        elif bit_depth >= 16 and vintage_intensity <= 0.5:
            return "Modern Retro"
        else:
            return "Custom"
    
    def auto_configure_for_performance(self, target_performance: str = "balanced"):
        """
        Automatically configure settings based on performance target.
        
        Args:
            target_performance: "fast", "balanced", or "quality"
        """
        if target_performance == "fast":
            self.set_config('synthesis', 'formant_count', 3)
            self.set_config('synthesis', 'diphone_smoothing', False)
            self.set_config('advanced', 'spectral_enhancement', False)
            self.set_config('advanced', 'temporal_smoothing', False)
            
        elif target_performance == "balanced":
            self.set_config('synthesis', 'formant_count', 4)
            self.set_config('synthesis', 'diphone_smoothing', True)
            self.set_config('advanced', 'spectral_enhancement', True)
            self.set_config('advanced', 'temporal_smoothing', False)
            
        elif target_performance == "quality":
            self.set_config('synthesis', 'formant_count', 5)
            self.set_config('synthesis', 'diphone_smoothing', True)
            self.set_config('advanced', 'spectral_enhancement', True)
            self.set_config('advanced', 'temporal_smoothing', True)
        
        print(f"Auto-configured for {target_performance} performance")
    
    def print_current_config(self):
        """Print current configuration in a readable format."""
        print("\n=== Current Configuration ===")
        print(f"Quality Level: {self.get_quality_level()}")
        print(f"Current Preset: {self.get_current_preset()}")
        
        audio = self.get_audio_config()
        print(f"\nAudio: {audio['sample_rate']}Hz, {audio['bit_depth']}-bit, {audio['channels']} channel(s)")
        
        synthesis = self.get_synthesis_config()
        print(f"Synthesis: {synthesis['formant_count']} formants, {synthesis['formant_precision']} precision")
        
        vintage = self.get_vintage_config()
        print(f"Vintage Processing: {'Enabled' if vintage['enabled'] else 'Disabled'}, {vintage['intensity']:.1f} intensity")
        
        errors = self.validate_config()
        if errors:
            print(f"\nValidation Errors: {errors}")
        else:
            print("\nConfiguration is valid ✓")
