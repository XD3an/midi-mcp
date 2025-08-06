"""
MIDI MCP Server Data Models

This module contains all the Pydantic data models used by the MIDI MCP server.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class MidiNote(BaseModel):
    """MIDI note data model"""
    note: int = Field(description="MIDI note number (0-127)", ge=0, le=127)
    velocity: int = Field(default=80, description="Note velocity (0-127)", ge=0, le=127)
    duration: int = Field(description="Note duration (ticks)", gt=0)
    channel: int = Field(default=0, description="MIDI channel (0-15)", ge=0, le=15)


class ChordProgression(BaseModel):
    """Chord progression data model"""
    chords: List[str] = Field(description="List of chord names, e.g. ['C', 'Am', 'F', 'G']")
    duration_per_chord: int = Field(default=480, description="Duration per chord (ticks)", gt=0)
    octave: int = Field(default=4, description="Octave (0-9)", ge=0, le=9)
    inversion: int = Field(default=0, description="Inversion (0-2)", ge=0, le=2)


class MelodyParams(BaseModel):
    """Melody parameters model"""
    scale: str = Field(default="major", description="Scale type")
    key: str = Field(default="C", description="Key")
    octave: int = Field(default=4, description="Octave", ge=0, le=9)
    note_count: int = Field(default=16, description="Number of notes", gt=0)
    rhythm_pattern: Optional[List[int]] = Field(default=None, description="Rhythm pattern")


class DrumPattern(BaseModel):
    """Drum pattern model"""
    kick_pattern: List[bool] = Field(description="Kick drum pattern")
    snare_pattern: List[bool] = Field(description="Snare drum pattern")
    hihat_pattern: List[bool] = Field(description="Hi-hat pattern")
    tempo: int = Field(default=120, description="Tempo (BPM)", ge=40, le=200)


class MidiFileInfo(BaseModel):
    """MIDI file information model"""
    filename: str = Field(description="MIDI file name")
    format_type: int = Field(description="MIDI format type")
    track_count: int = Field(description="Number of tracks")
    ticks_per_beat: int = Field(description="Time resolution")
    duration: float = Field(description="Total duration in seconds")


class TrackInfo(BaseModel):
    """MIDI track information model"""
    track_number: int = Field(description="Track number")
    message_count: int = Field(description="Total messages in track")
    note_events: int = Field(description="Number of note events")
    control_events: int = Field(description="Number of control events")
    program_changes: int = Field(description="Number of program changes")
    note_range_low: Optional[int] = Field(default=None, description="Lowest note number")
    note_range_high: Optional[int] = Field(default=None, description="Highest note number")
