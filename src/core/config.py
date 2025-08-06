"""
Configuration Module for MIDI MCP Server

This module handles configuration management and default settings.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class ServerConfig:
    """Configuration settings for the MIDI MCP server."""

    # File settings
    output_directory: str = "midi_output"

    # MIDI settings
    default_tempo: int = 120
    default_time_signature: tuple[int, int] = (4, 4)
    default_velocity: int = 80
    ticks_per_beat: int = 480

    # Audio settings
    audio_frequency: int = 22050
    audio_buffer_size: int = 512

    # Generation settings
    default_octave: int = 4
    default_scale: str = "major"
    default_key: str = "C"

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ServerConfig':
        """
        Create configuration from dictionary.

        Args:
            config_dict: Dictionary containing configuration values

        Returns:
            ServerConfig instance
        """
        valid_keys = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        return cls(**filtered_dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Dictionary representation of configuration
        """
        return {
            'output_directory': self.output_directory,
            'default_tempo': self.default_tempo,
            'default_time_signature': self.default_time_signature,
            'default_velocity': self.default_velocity,
            'ticks_per_beat': self.ticks_per_beat,
            'audio_frequency': self.audio_frequency,
            'audio_buffer_size': self.audio_buffer_size,
            'default_octave': self.default_octave,
            'default_scale': self.default_scale,
            'default_key': self.default_key,
        }

    def ensure_output_directory(self) -> Path:
        """
        Ensure output directory exists and return Path object.

        Returns:
            Path to output directory
        """
        output_path = Path(self.output_directory)
        output_path.mkdir(exist_ok=True)
        return output_path


# Global configuration instance
config = ServerConfig()
