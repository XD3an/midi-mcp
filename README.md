# midi-mcp

A Model Context Protocol (MCP) server that provides MIDI file generation and playback features.

## Available Tools

- **create_midi**: Generate a MIDI file.

  - Parameters:
    - `title`: MIDI file title (used as filename).
    - `composition`: A dictionary describing the composition (BPM, time signature, tracks, notes).
    - `composition_file`: Path to a JSON file containing the composition data.
    - `output_path`: Output filename (name only, no path), default is saved to the specified output directory.
  - Returns: Success message and file path.

- **play_midi**: Play a specified MIDI file.
  - Parameters:
    - `midi_path`: Full path to the MIDI file.
  - Returns: Playback success message.

## Quick Installation & Startup

1. Install dependencies:

   From the project root directory, run:

   ```bash
   uv sync
   ```

2. Start the server (output directory can be customized):

Configure your MCP-compatible client (e.g., Claude Desktop) as follows, where `\\PATH\\TO\\midi-mcp\\src` is the actual path to the MIDI MCP source, and `\\PATH\\TO\\midi_output` is the output directory:

### Claude Desktop MCP Server Configuration

```json
{
  "mcpServers": {
    "midi-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "\\PATH\\TO\\midi-mcp\\src",
        "run",
        "server.py",
        "--output_directory",
        "\\PATH\\TO\\midi_output"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

### VSCode MCP Server Configuration

In your project, configure [.vscode/mcp.json](.vscode/mcp.json):

```json
{
  "servers": {
    "midi-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "\\PATH\\TO\\midi-mcp\\src",
        "run",
        "server.py",
        "--output_directory",
        "\\PATH\\TO\\midi_output"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

## Usage

You can tell the LLM to generate MIDI compositions by providing a description of the desired piece. The server will handle the creation and playback of the MIDI files.

### Example Prompts

> I want to compose a pure piano piece. Please generate a C major melody with chords and play it.

> Create a fast-paced rock-style MIDI with drum beats and electric bass at 150 BPM. Then play the result.

> Compose a classical-style waltz in D minor, 3/4 time, 90 BPM. Include arpeggiated chords in the left hand and a lyrical melody in the right hand. Generate and play the MIDI.

> I want a relaxing jazz piano solo in F major, 4/4, 120 BPM. Include some swing feel. Create and play the MIDI.

> I'm feeling melancholic. Please compose a slow, sad piano piece in A minor with a gentle melody and subtle harmonies. Then play it.

> I’m in a good mood today. Create a cheerful and bright piano tune in C major, 4/4, 120 BPM with upbeat rhythms and catchy melody. Play the MIDI.

> I just went through heartbreak. Compose a solo piano piece that expresses deep emotional pain and longing in D minor. Slow tempo. Then play it.

> I want to relax and clear my mind. Generate a minimalistic, ambient-style composition with soft piano and slow BPM (around 60). Play the result.

> I’m feeling angry. Create a high-intensity MIDI piece with fast, aggressive rhythms and dissonant chords, preferably using orchestral percussion and strings. Play it.

> I feel nervous and anxious. Compose a tense, repetitive piano motif in a minor key with uneven rhythm to reflect unease. Play the composition.

> I’m falling in love. Please write a romantic and dreamy piano piece in E♭ major, moderate tempo, with expressive harmonies. Then play it.

> Compose an uplifting orchestral piece using multiple instruments, including piano, strings, brass, woodwinds, and percussion.
>
> The composition should be in 4/4 time at 110 BPM and evoke a sense of adventure and triumph.
>
> Structure it into 3 sections:
>
> Intro with soft strings and solo flute
>
> Build-up with horns, piano chords, and rhythmic percussion
>
> Climax with full orchestration and layered harmonies
>
> Then generate the MIDI file and play it.

The LLM will automatically call `create_midi` to generate the composition, then call `play_midi` to play it.

### Example composition structure:

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

All generated MIDI files are automatically saved in the `--output_directory` specified when starting the server (default is `midi_output/`).

## Reference

- [tubone24/midi-mcp-server](https://github.com/tubone24/midi-mcp-server)

## License

This project is licensed under the MIT License. See [../LICENCE](../LICENCE) for details.
