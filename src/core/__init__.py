"""
MIDI MCP Server Package

A modular MIDI generation, editing, and analysis server built with the Model Context Protocol (MCP).

This package provides:
- MIDI file generation and manipulation
- Music theory tools and generators
- Complex piano piece generation with difficulty levels
- MIDI file analysis and conversion
- Audio playback capabilities

Modules:
- server: Main MCP server with tool definitions
- models: Pydantic data models
- music_theory: Music theory constants and utilities
- midi_operations: MIDI file operations and analysis
- music_generators: Specialized music generation tools
- config: Configuration management
- exceptions: Custom exception classes
"""

# 全部使用絕對 import，避免 ModuleNotFoundError
from core.config import config
from core.exceptions import (
    ConfigurationError,
    MidiFileError,
    MidiMCPError,
    MidiPlaybackError,
    MusicTheoryError,
)
from core.midi_operations import MidiFileManager, MidiPlayer
from core.music_generators import ClassicalMusicGenerator
from core.music_theory import (
    CHORD_TYPES,
    DRUM_MAP,
    NOTES,
    SCALES,
    generate_chord_notes,
    generate_scale_notes,
    get_chord_info,
    get_scale_info,
    midi_to_note_name,
    note_name_to_midi,
    parse_chord_name,
)

__version__ = "2.0.0"
__author__ = "MIDI MCP Server Team"
__description__ = "Modular MIDI Generation MCP Server"

# Export main components
__all__ = [
    # Configuration
    "config", "ServerConfig",

    # Exceptions
    "MidiMCPError", "MidiFileError", "MidiPlaybackError",
    "MusicTheoryError", "ConfigurationError",

    # Core operations
    "MidiFileManager", "MidiPlayer", "ClassicalMusicGenerator",

    # Music theory
    "NOTES", "CHORD_TYPES", "SCALES", "DRUM_MAP",
    "note_name_to_midi", "midi_to_note_name",
    "generate_chord_notes", "generate_scale_notes",
    "parse_chord_name", "get_chord_info", "get_scale_info",

    # Metadata
    "__version__", "__author__", "__description__"
]
