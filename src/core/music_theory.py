"""
Music Theory Module

This module contains music theory constants, utility functions, and note/chord/scale
generation functionality for the MIDI MCP server.
"""

from typing import Dict, List

# Music theory constants
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

CHORD_TYPES: Dict[str, List[int]] = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    'dom7': [0, 4, 7, 10],
    'sus2': [0, 2, 7],
    'sus4': [0, 5, 7],
    '9': [0, 4, 7, 10, 14],
    'maj9': [0, 4, 7, 11, 14],
    'min9': [0, 3, 7, 10, 14],
}

SCALES: Dict[str, List[int]] = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'pentatonic': [0, 2, 4, 7, 9],
    'blues': [0, 3, 5, 6, 7, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
}

# MIDI constants
MIDDLE_C = 60
DRUM_CHANNEL = 9

# Drum note mapping
DRUM_MAP: Dict[str, int] = {
    'kick': 36,      # Bass Drum
    'snare': 38,     # Snare Drum
    'hihat': 42,     # Closed Hi-hat
    'open_hihat': 46,  # Open Hi-hat
    'crash': 49,     # Crash Cymbal
    'ride': 51,      # Ride Cymbal
    'tom_low': 45,   # Low Tom
    'tom_mid': 47,   # Mid Tom
    'tom_high': 50,  # High Tom
    'clap': 39,      # Hand Clap
}


def note_name_to_midi(note_name: str, octave: int = 4) -> int:
    """
    Convert note name to MIDI number.

    Args:
        note_name: Note name (e.g., 'C', 'C#', 'Db')
        octave: Octave number (0-9)

    Returns:
        MIDI note number (0-127)

    Raises:
        ValueError: If note name is invalid or MIDI number is out of range
    """
    if not (0 <= octave <= 9):
        raise ValueError(f"Octave must be between 0 and 9, got {octave}")

    try:
        if '#' in note_name:
            base_note = note_name[0]
            note_index = NOTES.index(base_note) + 1
        elif 'b' in note_name:
            base_note = note_name[0]
            note_index = (NOTES.index(base_note) - 1) % 12
        else:
            note_index = NOTES.index(note_name)

        midi_number = octave * 12 + note_index + 12

        if not (0 <= midi_number <= 127):
            raise ValueError(f"MIDI note number {midi_number} is out of range (0-127)")

        return midi_number

    except ValueError as e:
        if "not in list" in str(e):
            raise ValueError(f"Invalid note name: {note_name}")
        raise


def midi_to_note_name(midi_number: int) -> tuple[str, int]:
    """
    Convert MIDI number to note name and octave.

    Args:
        midi_number: MIDI note number (0-127)

    Returns:
        Tuple of (note_name, octave)

    Raises:
        ValueError: If MIDI number is out of range
    """
    if not (0 <= midi_number <= 127):
        raise ValueError(f"MIDI note number must be between 0 and 127, got {midi_number}")

    octave = (midi_number - 12) // 12
    note_index = (midi_number - 12) % 12
    note_name = NOTES[note_index]

    return note_name, octave


def generate_chord_notes(chord_name: str, chord_type: str = 'major', octave: int = 4) -> List[int]:
    """
    Generate MIDI note numbers for a chord.

    Args:
        chord_name: Root note name (e.g., 'C', 'F#')
        chord_type: Type of chord (default: 'major')
        octave: Octave for the root note

    Returns:
        List of MIDI note numbers

    Raises:
        ValueError: If chord type is invalid
    """
    if chord_type not in CHORD_TYPES:
        raise ValueError(f"Unknown chord type: {chord_type}. Available types: {list(CHORD_TYPES.keys())}")

    root_note = note_name_to_midi(chord_name, octave)
    intervals = CHORD_TYPES[chord_type]

    return [root_note + interval for interval in intervals]


def generate_scale_notes(key: str, scale_type: str = 'major', octave: int = 4,
                        num_octaves: int = 1) -> List[int]:
    """
    Generate MIDI note numbers for a scale.

    Args:
        key: Root note name (e.g., 'C', 'F#')
        scale_type: Type of scale (default: 'major')
        octave: Starting octave
        num_octaves: Number of octaves to generate

    Returns:
        List of MIDI note numbers

    Raises:
        ValueError: If scale type is invalid
    """
    if scale_type not in SCALES:
        raise ValueError(f"Unknown scale type: {scale_type}. Available types: {list(SCALES.keys())}")

    root_note = note_name_to_midi(key, octave)
    intervals = SCALES[scale_type]

    notes = []
    for oct_offset in range(num_octaves):
        for interval in intervals:
            note = root_note + interval + (oct_offset * 12)
            if 0 <= note <= 127:  # Ensure note is within MIDI range
                notes.append(note)

    return notes


def parse_chord_name(chord_name: str) -> tuple[str, str]:
    """
    Parse a chord name into root note and chord type.

    Args:
        chord_name: Full chord name (e.g., 'Cmaj7', 'Am', 'F#dim')

    Returns:
        Tuple of (root_note, chord_type)
    """
    # Handle sharp/flat notes
    if len(chord_name) > 1 and chord_name[1] in '#b':
        root = chord_name[:2]
        suffix = chord_name[2:]
    else:
        root = chord_name[0]
        suffix = chord_name[1:]

    # Map common chord suffixes
    suffix_map = {
        'm': 'minor',
        'maj': 'major',
        'maj7': 'maj7',
        'm7': 'min7',
        '7': 'dom7',
        'dim': 'dim',
        'aug': 'aug',
        '+': 'aug',
        'sus2': 'sus2',
        'sus4': 'sus4',
        '9': '9',
        'maj9': 'maj9',
        'm9': 'min9',
    }

    chord_type = suffix_map.get(suffix, 'major' if not suffix else suffix)

    return root, chord_type


def get_chord_info() -> str:
    """Get formatted information about available chord types."""
    result = "=== Supported Chord Types ===\n\n"
    for chord_type, intervals in CHORD_TYPES.items():
        result += f"{chord_type:12}: {intervals}\n"
    return result


def get_scale_info() -> str:
    """Get formatted information about available scale types."""
    result = "=== Supported Scale Types ===\n\n"
    for scale_type, intervals in SCALES.items():
        result += f"{scale_type:15}: {intervals}\n"
    return result
