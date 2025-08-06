"""
Music Generation Tools

This module contains specialized functions for generating specific musical pieces
and complex musical structures.
"""

from pathlib import Path
from typing import List, Tuple

from mido import Message, MidiFile, MidiTrack

# Handle imports for both package and script execution
try:
    from .config import config
    from .exceptions import MidiFileError
except ImportError:
    from config import config
    from exceptions import MidiFileError


class ClassicalMusicGenerator:
    """Generator for classical music pieces."""

    def __init__(self, output_directory: str = None):
        """
        Initialize classical music generator.

        Args:
            output_directory: Directory for saving generated files
        """
        self.output_dir = Path(output_directory or config.output_directory)
        self.output_dir.mkdir(exist_ok=True)

    def generate_beethoven_symphony5(self) -> str:
        """
        Generate Beethoven's Symphony No. 5 opening theme.

        Returns:
            Success message with file path

        Raises:
            MidiFileError: If generation fails
        """
        try:
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)

            # Set instrument to Acoustic Grand Piano
            track.append(Message('program_change', program=0, time=0))

            # Beethoven's Symphony No. 5 theme notes (G minor)
            main_melody = [
                # Famous "fate knocking" motif
                (67, 240), (67, 240), (67, 240), (62, 720),  # G-G-G-D
                (65, 240), (65, 240), (65, 240), (60, 720),  # F-F-F-C
                (67, 240), (67, 240), (67, 240), (62, 720),  # Repeat
                (65, 240), (65, 240), (65, 240), (60, 720),

                # Development section
                (67, 240), (69, 240), (71, 240), (72, 480), (71, 240), (69, 240), (67, 480),
                (65, 240), (67, 240), (69, 240), (71, 480), (69, 240), (67, 240), (65, 480),

                # Powerful chord sequence (broken chords)
                (72, 120), (76, 120), (79, 120), (76, 120), (72, 120), (67, 240),
                (65, 120), (60, 120), (62, 120), (65, 240), (67, 480),

                # Dramatic ending
                (67, 480), (65, 480), (62, 720), (60, 960),
            ]

            # Bass accompaniment
            bass_notes = [
                # Bass line for fate theme
                (43, 240), (43, 240), (43, 240), (38, 720),  # G-G-G-D (octave lower)
                (41, 240), (41, 240), (41, 240), (36, 720),  # F-F-F-C (octave lower)
                (43, 240), (43, 240), (43, 240), (38, 720),
                (41, 240), (41, 240), (41, 240), (36, 720),

                # Bass development
                (43, 240), (45, 240), (47, 240), (48, 480), (47, 240), (45, 240), (43, 480),
                (41, 240), (43, 240), (45, 240), (47, 480), (45, 240), (43, 240), (41, 480),

                # Bass for chord sequence
                (48, 120), (52, 120), (55, 120), (52, 120), (48, 120), (43, 240),
                (41, 120), (36, 120), (38, 120), (41, 240), (43, 480),

                # Bass ending
                (43, 480), (41, 480), (38, 720), (36, 960),
            ]

            # Add main melody
            self._add_notes_to_track(track, main_melody, velocity=80)

            # Add bass track
            bass_track = MidiTrack()
            mid.tracks.append(bass_track)
            bass_track.append(Message('program_change', program=0, time=0))
            self._add_notes_to_track(bass_track, bass_notes, velocity=60)

            # Save file
            filename = "beethoven_symphony5.mid"
            file_path = self.output_dir / filename
            mid.save(str(file_path))

            return f"Beethoven's Symphony No. 5 theme generated: {file_path.absolute()}"

        except Exception as e:
            raise MidiFileError(f"Failed to generate Beethoven Symphony No. 5: {str(e)}")

    def generate_complex_piano_piece(self, filename: str = "complex_piano.mid",
                                   tempo: int = 160, difficulty_level: str = "hard") -> str:
        """
        Generate a complex piano piece with varying difficulty levels.

        Args:
            filename: Name of the file to create
            tempo: Tempo in BPM
            difficulty_level: "easy", "medium", "hard", or "extreme"

        Returns:
            Success message with file path

        Raises:
            MidiFileError: If generation fails
        """
        try:
            mid = MidiFile()

            # Set tempo
            track = MidiTrack()
            mid.tracks.append(track)
            tempo_value = int(60000000 / tempo)
            track.append(Message('set_tempo', tempo=tempo_value, time=0))
            track.append(Message('program_change', program=0, time=0))

            # Generate piece based on difficulty
            if difficulty_level == "easy":
                notes = self._generate_easy_piece()
            elif difficulty_level == "medium":
                notes = self._generate_medium_piece()
            elif difficulty_level == "hard":
                notes = self._generate_hard_piece()
            elif difficulty_level == "extreme":
                notes = self._generate_extreme_piece()
            else:
                raise ValueError(f"Unknown difficulty level: {difficulty_level}")

            # Add right hand (main melody)
            right_hand_track = MidiTrack()
            mid.tracks.append(right_hand_track)
            right_hand_track.append(Message('program_change', program=0, time=0))
            self._add_notes_to_track(right_hand_track, notes['right_hand'], velocity=85)

            # Add left hand (accompaniment)
            left_hand_track = MidiTrack()
            mid.tracks.append(left_hand_track)
            left_hand_track.append(Message('program_change', program=0, time=0))
            self._add_notes_to_track(left_hand_track, notes['left_hand'], velocity=70)

            # Save file
            file_path = self.output_dir / filename
            mid.save(str(file_path))

            return f"Complex piano piece ({difficulty_level}) generated: {file_path.absolute()}"

        except Exception as e:
            raise MidiFileError(f"Failed to generate complex piano piece: {str(e)}")

    def _add_notes_to_track(self, track: MidiTrack, notes: List[Tuple[int, int]],
                          velocity: int = 80) -> None:
        """
        Add notes to a MIDI track.

        Args:
            track: MIDI track to add notes to
            notes: List of (note_number, duration) tuples
            velocity: Note velocity
        """
        current_time = 0
        for note_num, duration in notes:
            track.append(Message('note_on', note=note_num, velocity=velocity, time=current_time))
            track.append(Message('note_off', note=note_num, velocity=velocity, time=duration))
            current_time = 0

    def _generate_easy_piece(self) -> dict:
        """Generate an easy piano piece."""
        right_hand = [
            # Simple C major scale runs
            (60, 240), (62, 240), (64, 240), (65, 240), (67, 240), (69, 240), (71, 240), (72, 480),
            (72, 240), (71, 240), (69, 240), (67, 240), (65, 240), (64, 240), (62, 240), (60, 480),
            # Simple melody
            (67, 480), (69, 240), (71, 240), (72, 480), (71, 240), (69, 240), (67, 720),
            (65, 480), (64, 240), (62, 240), (60, 960),
        ]

        left_hand = [
            # Simple bass accompaniment
            (36, 480), (43, 480), (36, 480), (43, 480),
            (41, 480), (48, 480), (41, 480), (48, 480),
            (39, 480), (46, 480), (39, 480), (46, 480),
            (36, 480), (43, 480), (36, 960),
        ]

        return {'right_hand': right_hand, 'left_hand': left_hand}

    def _generate_medium_piece(self) -> dict:
        """Generate a medium difficulty piano piece."""
        right_hand = [
            # Faster scale runs with some jumps
            (60, 120), (64, 120), (67, 120), (72, 120), (76, 120), (79, 120), (84, 240),
            (84, 120), (79, 120), (76, 120), (72, 120), (67, 120), (64, 120), (60, 240),
            # Arpeggiated melody
            (72, 180), (76, 180), (79, 180), (84, 360), (79, 180), (76, 180), (72, 360),
            (69, 180), (72, 180), (76, 180), (81, 360), (76, 180), (72, 180), (69, 360),
            # Octave jumps
            (48, 120), (60, 120), (72, 120), (84, 240), (72, 120), (60, 120), (48, 480),
        ]

        left_hand = [
            # Alberti bass pattern
            (36, 120), (43, 120), (48, 120), (43, 120), (36, 120), (43, 120), (48, 120), (43, 120),
            (41, 120), (48, 120), (53, 120), (48, 120), (41, 120), (48, 120), (53, 120), (48, 120),
            (39, 120), (46, 120), (51, 120), (46, 120), (39, 120), (46, 120), (51, 120), (46, 120),
            (36, 120), (43, 120), (48, 120), (43, 120), (36, 480),
        ]

        return {'right_hand': right_hand, 'left_hand': left_hand}

    def _generate_hard_piece(self) -> dict:
        """Generate a hard difficulty piano piece."""
        right_hand = [
            # Fast chromatic runs
            (60, 60), (61, 60), (62, 60), (63, 60), (64, 60), (65, 60), (66, 60), (67, 60),
            (68, 60), (69, 60), (70, 60), (71, 60), (72, 60), (73, 60), (74, 60), (75, 60),
            (76, 120), (79, 120), (83, 120), (87, 240),
            # Complex arpeggios
            (72, 90), (79, 90), (84, 90), (91, 90), (96, 180), (91, 90), (84, 90), (79, 90), (72, 180),
            (69, 90), (76, 90), (81, 90), (88, 90), (93, 180), (88, 90), (81, 90), (76, 90), (69, 180),
            # Wide interval jumps
            (36, 60), (84, 60), (40, 60), (88, 60), (43, 60), (91, 60), (48, 240),
        ]

        left_hand = [
            # Complex accompaniment patterns
            (24, 90), (36, 90), (43, 90), (48, 90), (55, 90), (60, 90), (67, 90), (72, 90),
            (29, 90), (41, 90), (48, 90), (53, 90), (60, 90), (65, 90), (72, 90), (77, 90),
            (27, 90), (39, 90), (46, 90), (51, 90), (58, 90), (63, 90), (70, 90), (75, 90),
            (24, 120), (36, 120), (48, 120), (60, 240),
        ]

        return {'right_hand': right_hand, 'left_hand': left_hand}

    def _generate_extreme_piece(self) -> dict:
        """Generate an extremely difficult piano piece."""
        right_hand = [
            # Lightning-fast chromatic runs
            (48, 30), (49, 30), (50, 30), (51, 30), (52, 30), (53, 30), (54, 30), (55, 30),
            (56, 30), (57, 30), (58, 30), (59, 30), (60, 30), (61, 30), (62, 30), (63, 30),
            (64, 30), (65, 30), (66, 30), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30),
            (72, 30), (73, 30), (74, 30), (75, 30), (76, 30), (77, 30), (78, 30), (79, 30),
            (80, 30), (81, 30), (82, 30), (83, 30), (84, 60),
            # Virtuosic arpeggios
            (84, 45), (91, 45), (96, 45), (103, 45), (108, 90), (103, 45), (96, 45), (91, 45), (84, 90),
            (81, 45), (88, 45), (93, 45), (100, 45), (105, 90), (100, 45), (93, 45), (88, 45), (81, 90),
            # Extreme interval jumps and trills
            (36, 30), (96, 30), (36, 30), (96, 30), (36, 30), (96, 30), (36, 30), (96, 30),
            (72, 15), (74, 15), (72, 15), (74, 15), (72, 15), (74, 15), (72, 15), (74, 15),
            (76, 15), (78, 15), (76, 15), (78, 15), (76, 15), (78, 15), (76, 240),
        ]

        left_hand = [
            # Complex polyrhythmic accompaniment
            (12, 60), (24, 60), (36, 60), (48, 60), (60, 60), (72, 60), (84, 60), (96, 60),
            (17, 60), (29, 60), (41, 60), (53, 60), (65, 60), (77, 60), (89, 60), (101, 60),
            (15, 60), (27, 60), (39, 60), (51, 60), (63, 60), (75, 60), (87, 60), (99, 60),
            (12, 45), (24, 45), (36, 45), (48, 45), (60, 45), (72, 45), (84, 45), (96, 180),
            # Bass octaves
            (24, 30), (36, 30), (24, 30), (36, 30), (29, 30), (41, 30), (29, 30), (41, 30),
            (27, 30), (39, 30), (27, 30), (39, 30), (24, 120),
        ]

        return {'right_hand': right_hand, 'left_hand': left_hand}
