"""
MIDI Generation MCP Server

Supports:
- MIDI file generation and editing
- Music theory tools (chords, scales, rhythms)
- Music style generation (classical, jazz, pop, etc.)
- MIDI file analysis and conversion
- Automatic piano playing support
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

from mcp.server.fastmcp import FastMCP

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
for p in [current_dir, parent_dir]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import config
from core.exceptions import MidiFileError, MidiPlaybackError
from core.midi_operations import MidiFileManager, MidiPlayer
from core.music_generators import ClassicalMusicGenerator
from core.music_theory import get_chord_info, get_scale_info

mcp = FastMCP("MIDI Generation Server")


midi_manager = MidiFileManager(config.output_directory)
midi_player = MidiPlayer()
music_generator = ClassicalMusicGenerator(config.output_directory)


# tool
@mcp.tool()
def create_midi_file(
    filename: str = "output.mid",
    tempo: int = 120,
    time_signature_num: int = 4,
    time_signature_den: int = 4
) -> str:
    """Create a new MIDI file in the output directory

    Args:
        filename: File name (without path, will be created in output directory)
        tempo: Tempo (BPM)
        time_signature_num: Time signature numerator (e.g., 4 for 4/4)
        time_signature_den: Time signature denominator (e.g., 4 for 4/4)

    Returns:
        Creation success message with full path
    """
    try:
        time_signature = (time_signature_num, time_signature_den)
        result = midi_manager.create_midi_file(filename, tempo, time_signature)
        return f"{result}\nFile location: {Path(config.output_directory) / filename}"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def add_melody_to_midi(
    filename: str,
    melody_params: Dict[str, Any]
) -> str:
    """Add melody to MIDI file in the output directory

    Args:
        filename: File name (must exist in output directory)
        melody_params: Melody parameters dictionary

    Returns:
        Addition result message with file location
    """
    try:
        result = midi_manager.add_melody(filename, melody_params)
        return f"{result}\nFile location: {Path(config.output_directory) / filename}"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def add_chord_progression(
    filename: str,
    progression_params: Dict[str, Any]
) -> str:
    """Add chord progression to MIDI file in the output directory

    Args:
        filename: File name (must exist in output directory)
        progression_params: Chord progression parameters

    Returns:
        Addition result message with file location
    """
    try:
        result = midi_manager.add_chord_progression(filename, progression_params)
        return f"{result}\nFile location: {Path(config.output_directory) / filename}"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def add_drum_pattern(
    filename: str,
    drum_params: Dict[str, Any]
) -> str:
    """Add drum pattern to MIDI file in the output directory

    Args:
        filename: File name (must exist in output directory)
        drum_params: Drum parameters

    Returns:
        Addition result message with file location
    """
    try:
        result = midi_manager.add_drum_pattern(filename, drum_params)
        return f"{result}\nFile location: {Path(config.output_directory) / filename}"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def generate_beethoven_symphony5() -> str:
    """Generate Beethoven's Symphony No. 5 theme MIDI file in output directory

    Returns:
        Generation result message with file location
    """
    try:
        result = music_generator.generate_beethoven_symphony5()
        return f"{result}\nFile saved in: {config.output_directory}/"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def analyze_midi_file(filename: str) -> str:
    """Analyze detailed information of a MIDI file in output directory

    Args:
        filename: File name (must exist in output directory)

    Returns:
        Analysis results with file location
    """
    try:
        result = midi_manager.analyze_file(filename)
        return f"{result}\nAnalyzed file: {Path(config.output_directory) / filename}"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def play_midi_file(filename: str) -> str:
    """Play a MIDI file from the output directory

    Args:
        filename: File name (must exist in output directory)

    Returns:
        Playback result message with file location
    """
    try:
        file_path = midi_manager._find_file(filename)
        result = midi_player.play_file(file_path)
        return f"{result}\nPlayed file: {Path(config.output_directory) / filename}"
    except (MidiFileError, MidiPlaybackError) as e:
        return f"Error: {str(e)}"


@mcp.tool()
def list_chord_types() -> str:
    """List supported chord types

    Returns:
        List of chord types
    """
    return get_chord_info()


@mcp.tool()
def list_scale_types() -> str:
    """List supported scale types

    Returns:
        List of scale types
    """
    return get_scale_info()


@mcp.tool()
def convert_midi_to_text(filename: str) -> str:
    """Convert MIDI file to text format for analysis

    Args:
        filename: File name (must exist in output directory)

    Returns:
        Text representation of MIDI content
    """
    try:
        result = midi_manager.convert_to_text(filename)
        return f"Text conversion of {Path(config.output_directory) / filename}:\n\n{result}"
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.tool()
def list_midi_files() -> str:
    """List all MIDI files in the output directory

    Returns:
        List of MIDI files with their sizes and modification times
    """
    try:
        output_path = Path(config.output_directory)
        if not output_path.exists():
            return f"Output directory does not exist: {output_path.absolute()}"

        midi_files = list(output_path.glob("*.mid")) + list(output_path.glob("*.midi"))

        if not midi_files:
            return f"No MIDI files found in: {output_path.absolute()}"

        result = f"MIDI files in {output_path.absolute()}:\n\n"
        for file_path in sorted(midi_files):
            size_kb = file_path.stat().st_size / 1024
            mtime = file_path.stat().st_mtime
            from datetime import datetime
            mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            result += f"📄 {file_path.name} ({size_kb:.1f} KB, modified: {mod_time})\n"

        return result

    except Exception as e:
        return f"Error listing MIDI files: {str(e)}"


# Prompt
@mcp.prompt()
def midi_usage_guide() -> str:
    """Complete MIDI MCP Server Usage Guide

    A comprehensive guide covering all features and capabilities of the MIDI Generation MCP Server.
    This guide includes step-by-step instructions, examples, and best practices for music creation,
    analysis, and MIDI file manipulation.
    """
    return """
# MIDI MCP Server Usage Guide
This MCP server provides comprehensive MIDI music generation, editing, and analysis functionality
with a modern, modular architecture designed for professional music creation workflows.


## Core Concepts & MIDI Fundamentals

### MIDI Technical Specifications
- **Note Numbers**: 0-127 (Middle C = 60, A4 = 69, frequency 440Hz)
- **Velocity**: 0-127 (note attack strength/volume)
- **Duration**: Measured in ticks (standard: 480 ticks per quarter note)
- **Channels**: 0-15 (Channel 9 reserved for percussion)
- **Time Signature**: Standard 4/4, customizable to any meter

### Advanced Features
- **Classical Music Generation**: Pre-programmed famous compositions
- **Enhanced Error Handling**: Robust error recovery and detailed diagnostics
- **Modular Architecture**: Separated concerns for better performance
- **Extended Music Theory**: Comprehensive chord and scale support

## 🛠 Core Tool Functions

### 1. File Creation & Management

#### Create New MIDI File
```
Tool: create_midi_file
Purpose: Initialize new MIDI file with tempo and time signature
Parameters:
- filename: "my_composition.mid" (filename only)
- tempo: 120 (BPM, range: 60-200 recommended)
- time_signature: (4, 4) or (3, 4), (6, 8), etc.
```

#### Analyze Existing MIDI Files
```
Tool: analyze_midi_file
Purpose: Extract comprehensive information from MIDI files
Parameters:
- filename: "song.mid" (filename only)
Returns: Track count, instruments, note ranges, tempo changes
Enhanced: Detailed harmonic and rhythmic analysis
```

#### Convert to Human-Readable Format
```
Tool: convert_midi_to_text
Purpose: Export MIDI events as readable text
Parameters:
- filename: "song.mid" (filename only)
Format: Note names, timing, velocities, control changes
```

#### List MIDI Files
```
Tool: list_midi_files
Purpose: Display all MIDI files in the current directory
Returns: File names, sizes, modification dates
```

### 2. Advanced Music Generation

#### Classical Music Generation
```
Tool: generate_beethoven_symphony5
Purpose: Generate the famous opening of Beethoven's 5th Symphony
Features: Orchestral arrangement, proper voice leading
Output: Multi-track MIDI with melody and bass
```

### 3. Musical Element Addition

#### Chord Progressions
```
Tool: add_chord_progression
Purpose: Add harmonic foundation to compositions
Parameters:
- filename: "song.mid"
- progression_params: {
    "chords": ["Cmaj7", "Am7", "Fmaj7", "G7"],
    "duration_per_chord": 1920 (2 beats at 480 tpqn),
    "octave": 3,
    "inversion": 0 (root position),
    "voicing": "close" or "open"
  }
Supported Chord Types:
- Triads: C, Cm, Cdim, Caug
- Sevenths: Cmaj7, Cm7, C7, Cdim7, Cm7b5
- Extensions: C9, Cmaj9, Cm9, C11, C13
- Suspended: Csus2, Csus4
```

#### Melodic Content
```
Tool: add_melody_to_midi
Purpose: Generate melodic lines based on scales and patterns
Parameters:
- filename: "song.mid"
- melody_params: {
    "scale": "major", "minor", "dorian", "pentatonic", "blues"
    "key": "C", "F#", "Bb" (any chromatic pitch)
    "octave": 5 (recommended: 4-6 for melody)
    "note_count": 32,
    "rhythm_pattern": [240, 240, 480, 240] (custom rhythms)
    "phrase_length": 8 (notes per phrase)
  }
```

#### Drum Patterns
```
Tool: add_drum_pattern
Purpose: Add rhythmic foundation
Parameters:
- filename: "song.mid"
- drum_params: {
    "pattern": "rock", "jazz", "latin", "electronic"
    "bars": 8,
    "complexity": "simple", "medium", "complex"
  }
```

### 4. Playback & Testing

#### MIDI Playback
```
Tool: play_midi_file
Purpose: Immediate playback for testing compositions
Parameters:
- filename: "song.mid"
Requirements: System MIDI output or software synthesizer
Enhanced: Better error handling, file validation
```

## Complete Workflow Examples

### Example 1: Creating a Jazz Ballad
```
1. create_midi_file("jazz_ballad.mid", 80, (4, 4))
2. add_chord_progression("jazz_ballad.mid", {
     "chords": ["Cmaj7", "A7", "Dm7", "G7", "Em7", "A7", "Dm7", "G7"],
     "duration_per_chord": 1920,
     "octave": 3
   })
3. add_melody_to_midi("jazz_ballad.mid", {
     "scale": "major",
     "key": "C",
     "octave": 5,
     "note_count": 64,
     "rhythm_pattern": [480, 240, 240, 480, 480]
   })
4. play_midi_file("jazz_ballad.mid")
5. analyze_midi_file("jazz_ballad.mid")
```

### Example 2: Classical Composition Study
```
1. generate_beethoven_symphony5()
2. list_midi_files()  # See all available files
3. analyze_midi_file("beethoven_symphony5.mid")
4. convert_midi_to_text("beethoven_symphony5.mid")
```

## Music Theory Reference

### Extended Scale Types
- **Major Modes**: Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian
- **Minor Variations**: Natural, Harmonic, Melodic minor
- **Pentatonic**: Major pentatonic, Minor pentatonic, Blues scale
- **Exotic**: Whole tone, Diminished, Chromatic

### Advanced Chord Theory
- **Functional Harmony**: I-vi-IV-V progressions, Secondary dominants
- **Jazz Harmony**: Altered dominants, Tritone substitutions, Extended chords
- **Modal Harmony**: Chord progressions from church modes
- **Contemporary**: Quartal/quintal harmony, Polychords

### Rhythm Patterns (in ticks, 480 = quarter note)
- **Simple**: [480, 480, 480, 480] (quarter notes)
- **Syncopated**: [240, 720, 240, 240] (eighth-dotted quarter-eighth)
- **Triplets**: [320, 320, 320] (quarter note triplets)
- **Complex**: [120, 360, 240, 480, 240] (mixed subdivisions)

## Resource Access

### MIDI File Resources
```
Resource: midi://file/{filename}
Purpose: Direct access to MIDI file content as text
Usage: For debugging, analysis, and custom processing
```

### Analysis Resources
```
Resource: midi://analysis/{filename}
Purpose: Structured analysis data
Content: JSON-formatted track and harmonic information
```

## Best Practices & Tips

### For Beginners
- Start with simple chord progressions: C-Am-F-G or I-vi-IV-V
- Use basic major and minor scales initially
- Set moderate tempos (80-120 BPM) for learning
- Always analyze generated files to understand MIDI structure

### For Intermediate Users
- Use extended chords: maj7, min7, dom7 for richer harmony
- Try different modes: Dorian, Mixolydian for variety
- Combine multiple generation techniques in single compositions
- Study classical examples for voice leading principles

### For Advanced Users
- Create complex chord progressions with secondary dominants
- Use multiple scales within compositions for modulation
- Analyze and modify MIDI programmatically using text conversion
- Experiment with polyrhythms and metric modulation

## Technical Implementation Notes

### File Management
- File naming: Use descriptive names with .mid extension (filename only)
- File listing: Use list_midi_files() to see all available files
- All operations work with filenames only, no paths needed

### Performance Optimization
- Modular architecture reduces memory usage
- Enhanced error handling prevents crashes
- Efficient MIDI parsing for large files
- Optimized playback system with hardware acceleration

### Error Handling
- Specific error types: MidiFileError, MidiPlaybackError, MusicTheoryError
- Graceful degradation: Partial results when possible
- Detailed error messages with suggested solutions
- Automatic recovery for common issues

## Audio Setup & Playback

### System Requirements
- Windows: Built-in MIDI support
- macOS: Core Audio MIDI services
- Linux: ALSA/PulseAudio with MIDI support

### Software Synthesizers (Recommended)
- FluidSynth: High-quality sample-based synthesis
- TiMidity++: Classic software synthesizer
- Virtual Studio Technology (VST): Professional plugin support

### Hardware MIDI
- USB MIDI keyboards: Plug-and-play compatibility
- Professional audio interfaces: Low-latency performance
- Dedicated sound modules: Hardware synthesis

This comprehensive guide covers all aspects of the MIDI Generation MCP Server.
Experiment with different combinations of tools and parameters to create unique musical compositions!
"""


# Resource
@mcp.resource("midi://file/{filename}")
def get_midi_file_content(filename: str) -> str:
    """Get detailed content of MIDI file"""
    try:
        return midi_manager.convert_to_text(filename)
    except MidiFileError as e:
        return f"Error: {str(e)}"


@mcp.resource("midi://analysis/{filename}")
def get_midi_analysis(filename: str) -> str:
    """Get analysis results of MIDI file"""
    try:
        return midi_manager.analyze_file(filename)
    except MidiFileError as e:
        return f"Error: {str(e)}"


def main():
    """Start MCP server with optional output directory parameter"""
    parser = argparse.ArgumentParser(description="MIDI Generation MCP Server")
    parser.add_argument(
        "--output_directory",
        type=str,
        default="midi_output",
        help="Directory for MIDI file output (default: midi_output)"
    )

    args = parser.parse_args()

    try:
        # Set the output directory from command line argument
        config.output_directory = args.output_directory
        output_path = config.ensure_output_directory()

        # Initialize components with the specified directory
        global midi_manager, music_generator
        midi_manager = MidiFileManager(str(output_path))
        music_generator = ClassicalMusicGenerator(str(output_path))


        # Start server
        mcp.run()

    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
