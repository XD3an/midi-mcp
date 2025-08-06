# MIDI MCP Server (Python)

This directory contains the Python implementation of the MIDI MCP server. It allows for the creation and playback of MIDI files through the Model Context Protocol (MCP).

## Available Tools

- **`create_midi(title: str, composition: dict = None, composition_file: str = None, output_path: str = None)`**

  - Generates a MIDI file using the `mido` library.
  - **Parameters:**
    - `title`: The title of the MIDI file (used for the filename).
    - `composition`: A dictionary describing the musical piece (BPM, time signature, tracks, notes).
    - `composition_file`: Path to a JSON file containing the composition data.
    - `output_path`: The name of the output file (filename only, no path). Defaults to saving in the specified output directory.
  - **Returns:** A success message with the path to the generated MIDI file.

- **`play_midi(midi_path: str)`**
  - Plays a specified MIDI file using `pygame`.
  - **Parameters:**
    - `midi_path`: The full path to the MIDI file to be played.
  - **Returns:** A success message upon completion.

## Quick Installation and Startup

1.  **Install dependencies:**
    From the root directory of the project, run:

    ```bash
    uv sync
    ```

2.  **Start the server:**
    Navigate to the `src` directory or use the `--directory` flag to run the server. You can specify an output directory for the MIDI files.
    ```bash
    uv run server.py --output_directory ../midi_output
    ```

## Usage Example

To use the server, you can send a request to an LLM capable of interacting with MCP servers.

**User Prompt:**

```
I want to create a piano piece. Please generate a melody in C major with some chords, and then play it for me.
```

The LLM will then use the available tools to fulfill the request. It will first call `create_midi` with a composition structure, and then call `play_midi` to play the resulting file.

### Example `composition` structure:

```json
{
  "bpm": 120,
  "timeSignature": { "numerator": 4, "denominator": 4 },
  "tracks": [
    {
      "name": "Piano Melody",
      "instrument": 0,
      "notes": [
        { "pitch": 60, "velocity": 100, "duration": "4", "beat": 1 },
        { "pitch": 62, "velocity": 100, "duration": "4", "beat": 2 },
        { "pitch": 64, "velocity": 100, "duration": "4", "beat": 3 },
        { "pitch": 65, "velocity": 100, "duration": "4", "beat": 4 }
      ]
    },
    {
      "name": "Piano Chords",
      "instrument": 0,
      "notes": [
        { "pitch": 48, "velocity": 80, "duration": "2", "beat": 1 },
        { "pitch": 52, "velocity": 80, "duration": "2", "beat": 1 },
        { "pitch": 55, "velocity": 80, "duration": "2", "beat": 1 },
        { "pitch": 53, "velocity": 80, "duration": "2", "beat": 3 },
        { "pitch": 57, "velocity": 80, "duration": "2", "beat": 3 },
        { "pitch": 60, "velocity": 80, "duration": "2", "beat": 3 }
      ]
    }
  ]
}
```

### File Output

All generated MIDI files will be saved to the directory specified by the `--output_directory` argument when starting the server (defaults to `midi_output/` in the parent directory).

---

## 授權

本專案採用 MIT 授權。詳見 [../LICENCE](../LICENCE)。
