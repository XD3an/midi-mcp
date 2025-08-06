"""
MIDI Operations Module

This module contains classes and functions for MIDI file creation, manipulation,
and analysis.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pygame
from mido import Message, MetaMessage, MidiFile, MidiTrack

# Handle imports for both package and script execution
try:
    from .exceptions import MidiFileError, MidiPlaybackError
    from .models import ChordProgression, DrumPattern, MelodyParams, MidiFileInfo, TrackInfo
    from .music_theory import (
        DRUM_MAP,
        NOTES,
        generate_chord_notes,
        generate_scale_notes,
        midi_to_note_name,
        parse_chord_name,
    )
except ImportError:
    from exceptions import MidiFileError, MidiPlaybackError
    from models import ChordProgression, DrumPattern, MelodyParams, MidiFileInfo, TrackInfo
    from music_theory import (
        DRUM_MAP,
        NOTES,
        generate_chord_notes,
        generate_scale_notes,
        midi_to_note_name,
        parse_chord_name,
    )


class MidiFileManager:
    """Manages MIDI file operations including creation, editing, and analysis."""

    def __init__(self, output_directory: str = "midi_output"):
        """
        Initialize MIDI file manager.

        Args:
            output_directory: Directory for saving MIDI files
        """
        self.output_dir = Path(output_directory)
        self.output_dir.mkdir(exist_ok=True)

    def create_midi_file(self, filename: str, tempo: int = 120,
                        time_signature: tuple[int, int] = (4, 4)) -> str:
        """
        Create a new MIDI file with basic setup.

        Args:
            filename: Name of the file to create
            tempo: Tempo in BPM
            time_signature: Time signature as (numerator, denominator)

        Returns:
            Success message with file path

        Raises:
            MidiFileError: If file creation fails
        """
        try:
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)

            # Set tempo
            tempo_value = int(60000000 / tempo)
            track.append(MetaMessage('set_tempo', tempo=tempo_value, time=0))

            # Set time signature
            track.append(MetaMessage('time_signature',
                                   numerator=time_signature[0],
                                   denominator=time_signature[1],
                                   clocks_per_click=24,
                                   notated_32nd_notes_per_beat=8,
                                   time=0))

            # Set instrument (Grand Piano)
            track.append(Message('program_change', program=0, time=0))

            file_path = self.output_dir / filename
            mid.save(str(file_path))

            return f"MIDI file created: {file_path.absolute()}"

        except Exception as e:
            raise MidiFileError(f"Failed to create MIDI file: {str(e)}")

    def add_melody(self, filename: str, melody_params: Dict[str, Any]) -> str:
        """
        Add melody to an existing MIDI file.

        Args:
            filename: Name of the MIDI file
            melody_params: Dictionary containing melody parameters

        Returns:
            Success message

        Raises:
            MidiFileError: If melody addition fails
        """
        try:
            params = MelodyParams(**melody_params)
            file_path = self.output_dir / filename

            # Load existing file or create new
            if file_path.exists():
                mid = MidiFile(str(file_path))
                track = mid.tracks[0]
            else:
                mid = MidiFile()
                track = MidiTrack()
                mid.tracks.append(track)
                track.append(Message('program_change', program=0, time=0))

            # Generate scale notes
            scale_notes = generate_scale_notes(params.key, params.scale, params.octave)

            # Generate melody
            current_time = 0
            for i in range(params.note_count):
                note = np.random.choice(scale_notes)
                duration = 240 if not params.rhythm_pattern else \
                          params.rhythm_pattern[i % len(params.rhythm_pattern)]
                velocity = np.random.randint(60, 100)

                track.append(Message('note_on', note=note, velocity=velocity, time=current_time))
                track.append(Message('note_off', note=note, velocity=velocity, time=duration))
                current_time = 0

            mid.save(str(file_path))
            return f"Melody added to {file_path.absolute()}"

        except Exception as e:
            raise MidiFileError(f"Failed to add melody: {str(e)}")

    def add_chord_progression(self, filename: str, progression_params: Dict[str, Any]) -> str:
        """
        Add chord progression to MIDI file.

        Args:
            filename: Name of the MIDI file
            progression_params: Dictionary containing chord progression parameters

        Returns:
            Success message

        Raises:
            MidiFileError: If chord progression addition fails
        """
        try:
            params = ChordProgression(**progression_params)
            file_path = self.output_dir / filename

            # Load or create file
            if file_path.exists():
                mid = MidiFile(str(file_path))
            else:
                mid = MidiFile()
                main_track = MidiTrack()
                mid.tracks.append(main_track)
                main_track.append(Message('program_change', program=0, time=0))

            # Create chord track
            chord_track = MidiTrack()
            mid.tracks.append(chord_track)
            chord_track.append(Message('program_change', program=0, time=0))

            current_time = 0
            for chord_name in params.chords:
                root, chord_type = parse_chord_name(chord_name)
                chord_notes = generate_chord_notes(root, chord_type, params.octave)

                # Add chord notes
                for note in chord_notes:
                    chord_track.append(Message('note_on', note=note, velocity=70, time=current_time))
                    current_time = 0

                # End chord notes
                for note in chord_notes:
                    chord_track.append(Message('note_off', note=note, velocity=70,
                                             time=params.duration_per_chord // len(chord_notes)))
                current_time = 0

            mid.save(str(file_path))
            return f"Chord progression added to {file_path.absolute()}"

        except Exception as e:
            raise MidiFileError(f"Failed to add chord progression: {str(e)}")

    def add_drum_pattern(self, filename: str, drum_params: Dict[str, Any]) -> str:
        """
        Add drum pattern to MIDI file.

        Args:
            filename: Name of the MIDI file
            drum_params: Dictionary containing drum parameters

        Returns:
            Success message

        Raises:
            MidiFileError: If drum pattern addition fails
        """
        try:
            params = DrumPattern(**drum_params)
            file_path = self.output_dir / filename

            # Load or create file
            if file_path.exists():
                mid = MidiFile(str(file_path))
            else:
                mid = MidiFile()
                main_track = MidiTrack()
                mid.tracks.append(main_track)

            # Create drum track (channel 9)
            drum_track = MidiTrack()
            mid.tracks.append(drum_track)

            beat_duration = 120  # ticks per beat
            max_length = max(len(params.kick_pattern), len(params.snare_pattern),
                           len(params.hihat_pattern))

            for i in range(max_length):
                current_time = i * beat_duration

                # Kick drum
                if i < len(params.kick_pattern) and params.kick_pattern[i]:
                    drum_track.append(Message('note_on', note=DRUM_MAP['kick'],
                                            velocity=100, channel=9,
                                            time=current_time if i == 0 else beat_duration))
                    drum_track.append(Message('note_off', note=DRUM_MAP['kick'],
                                            velocity=100, channel=9, time=10))

                # Snare drum
                if i < len(params.snare_pattern) and params.snare_pattern[i]:
                    drum_track.append(Message('note_on', note=DRUM_MAP['snare'],
                                            velocity=90, channel=9,
                                            time=0 if i > 0 else current_time))
                    drum_track.append(Message('note_off', note=DRUM_MAP['snare'],
                                            velocity=90, channel=9, time=10))

                # Hi-hat
                if i < len(params.hihat_pattern) and params.hihat_pattern[i]:
                    drum_track.append(Message('note_on', note=DRUM_MAP['hihat'],
                                            velocity=70, channel=9, time=0))
                    drum_track.append(Message('note_off', note=DRUM_MAP['hihat'],
                                            velocity=70, channel=9, time=10))

            mid.save(str(file_path))
            return f"Drum pattern added to {file_path.absolute()}"

        except Exception as e:
            raise MidiFileError(f"Failed to add drum pattern: {str(e)}")

    def analyze_file(self, filename: str) -> str:
        """
        Analyze a MIDI file and return detailed information.

        Args:
            filename: Name of the MIDI file

        Returns:
            Formatted analysis results

        Raises:
            MidiFileError: If file analysis fails
        """
        file_path = self._find_file(filename)

        try:
            mid = MidiFile(str(file_path))

            # Create file info
            file_info = MidiFileInfo(
                filename=filename,
                format_type=mid.type,
                track_count=len(mid.tracks),
                ticks_per_beat=mid.ticks_per_beat,
                duration=mid.length
            )

            # Analyze tracks
            track_infos = []
            for i, track in enumerate(mid.tracks):
                track_info = TrackInfo(
                    track_number=i,
                    message_count=len(track),
                    note_events=0,
                    control_events=0,
                    program_changes=0
                )

                notes = []
                for msg in track:
                    if msg.type == 'note_on':
                        track_info.note_events += 1
                        notes.append(msg.note)
                    elif msg.type == 'control_change':
                        track_info.control_events += 1
                    elif msg.type == 'program_change':
                        track_info.program_changes += 1

                if notes:
                    track_info.note_range_low = min(notes)
                    track_info.note_range_high = max(notes)

                track_infos.append(track_info)

            return self._format_analysis(file_info, track_infos)

        except Exception as e:
            raise MidiFileError(f"Failed to analyze file: {str(e)}")

    def convert_to_text(self, filename: str) -> str:
        """
        Convert MIDI file to text representation.

        Args:
            filename: Name of the MIDI file

        Returns:
            Text representation of MIDI content

        Raises:
            MidiFileError: If conversion fails
        """
        file_path = self._find_file(filename)

        try:
            mid = MidiFile(str(file_path))
            result = f"=== MIDI File Content: {file_path.absolute()} ===\n\n"

            for i, track in enumerate(mid.tracks):
                result += f"Track {i}:\n"
                current_time = 0

                for msg in track:
                    current_time += msg.time
                    if msg.type == 'note_on' and msg.velocity > 0:
                        note_name, octave = midi_to_note_name(msg.note)
                        result += (f"  Time:{current_time:4d} - Note On  {note_name}{octave} "
                                 f"(#{msg.note}) Velocity:{msg.velocity} Channel:{msg.channel}\n")
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        note_name, octave = midi_to_note_name(msg.note)
                        result += (f"  Time:{current_time:4d} - Note Off {note_name}{octave} "
                                 f"(#{msg.note}) Velocity:{msg.velocity} Channel:{msg.channel}\n")
                    elif msg.type == 'program_change':
                        result += (f"  Time:{current_time:4d} - Program Change: "
                                 f"{msg.program} Channel:{msg.channel}\n")
                    elif msg.type == 'control_change':
                        result += (f"  Time:{current_time:4d} - Control Change: "
                                 f"Controller:{msg.control} Value:{msg.value} Channel:{msg.channel}\n")
                    elif hasattr(msg, 'type') and msg.type.startswith('set_'):
                        result += f"  Time:{current_time:4d} - Meta: {msg}\n"

                result += "\n"

            return result

        except Exception as e:
            raise MidiFileError(f"Failed to convert file to text: {str(e)}")

    def _find_file(self, filename: str) -> Path:
        """
        Find MIDI file in output directory or current directory.

        Args:
            filename: Name of the file to find

        Returns:
            Path to the file

        Raises:
            MidiFileError: If file not found
        """
        file_path = self.output_dir / filename
        if file_path.exists():
            return file_path

        current_path = Path(filename)
        if current_path.exists():
            return current_path

        raise MidiFileError(f"File not found: {filename} "
                          f"(checked {self.output_dir}/ and current directory)")

    def _format_analysis(self, file_info: MidiFileInfo, track_infos: List[TrackInfo]) -> str:
        """Format analysis results into readable text."""
        result = "=== MIDI File Analysis ===\n\n"
        result += f"File: {file_info.filename}\n"
        result += f"Format: Type {file_info.format_type}\n"
        result += f"Track Count: {file_info.track_count}\n"
        result += f"Time Resolution: {file_info.ticks_per_beat} ticks per beat\n"
        result += f"Total Duration: {file_info.duration:.2f} seconds\n\n"

        for track_info in track_infos:
            result += f"Track {track_info.track_number}:\n"
            result += f"  Message Count: {track_info.message_count}\n"
            result += f"  Note Events: {track_info.note_events}\n"
            result += f"  Control Events: {track_info.control_events}\n"
            result += f"  Program Changes: {track_info.program_changes}\n"

            if track_info.note_range_low is not None:
                result += f"  Note Range: {track_info.note_range_low} - {track_info.note_range_high}\n"
            else:
                result += "  Note Range: No notes\n"
            result += "\n"

        return result


class MidiPlayer:
    """Handles MIDI file playback using pygame."""

    def __init__(self):
        """Initialize MIDI player."""
        self.is_initialized = False

    def play_file(self, file_path: Path) -> str:
        """
        Play a MIDI file.

        Args:
            file_path: Path to the MIDI file

        Returns:
            Success message

        Raises:
            MidiPlaybackError: If playback fails
        """
        try:
            if not self.is_initialized:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.is_initialized = True

            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()

            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            return f"Playback completed: {file_path.absolute()}"

        except Exception as e:
            raise MidiPlaybackError(f"Failed to play file: {str(e)}")
        finally:
            if self.is_initialized:
                pygame.mixer.quit()
                self.is_initialized = False
