"""
Custom Exceptions for MIDI MCP Server

This module defines custom exception classes used throughout the MIDI MCP server.
"""


class MidiMCPError(Exception):
    """Base exception class for MIDI MCP server errors."""
    pass


class MidiFileError(MidiMCPError):
    """Raised when MIDI file operations fail."""
    pass


class MidiPlaybackError(MidiMCPError):
    """Raised when MIDI playback fails."""
    pass


class MusicTheoryError(MidiMCPError):
    """Raised when music theory operations fail."""
    pass


class ConfigurationError(MidiMCPError):
    """Raised when configuration is invalid."""
    pass
