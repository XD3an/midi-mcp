import argparse
import json
import os

import mido
import pygame
from mcp.server.fastmcp import FastMCP

parser = argparse.ArgumentParser(description="MIDI MCP server")
parser.add_argument(
    "--output_directory",
    type=str,
    default="midi_output",
    help="MIDI output directory (default: midi_output)"
)
args, unknown = parser.parse_known_args()
default_output_dir = args.output_directory

mcp = FastMCP(
    name="midi-mcp-server"
)

@mcp.tool()
def create_midi(title: str = None, composition: dict = None, composition_file: str = None, output_path: str = None):
    """
    Generate a MIDI file using the mido library.

    參數說明：
    - title: MIDI 檔案標題（英文，作為檔名）。
    - composition: 樂曲內容的 dict，需包含 bpm、timeSignature、tracks。
    - composition_file: 樂曲內容的 JSON 檔案路徑（若有則優先讀取）。
    - output_path: 輸出檔名（僅檔名，不含路徑，預設為 output_directory 下的 title.mid）。

    回傳：
    - 成功訊息，包含產生的 MIDI 檔案路徑。
    - 若參數錯誤或檔案寫入失敗會拋出例外。
    """
    if not title:
        raise ValueError("You must provide 'title' (in English) as the filename.")
    # If output_path is specified, it must be a filename only (no path)
    if output_path:
        if os.path.basename(output_path) != output_path:
            raise ValueError("output_path must be a filename only, not a path.")
        output_path = os.path.join(default_output_dir, output_path)
    else:
        output_path = os.path.join(default_output_dir, f"{title}.mid")

    if not (composition or composition_file):
        raise ValueError("You must provide either composition or composition_file.")

    if composition_file:
        try:
            with open(composition_file, 'r', encoding='utf-8') as f:
                composition = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to read JSON file: {e}")

    # Handle case where composition is a JSON string
    if isinstance(composition, str):
        try:
            composition = json.loads(composition)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse composition JSON string: {e}")

    if not isinstance(composition, dict):
        raise ValueError("Composition must be a dictionary or valid JSON string.")

    abs_output_dir = os.path.abspath(default_output_dir)
    abs_output_path = os.path.abspath(output_path)
    if not abs_output_path.startswith(abs_output_dir + os.sep):
        raise ValueError(f"Output path must be inside the output directory: {default_output_dir}")

    # MIDI file generation
    mid = mido.MidiFile()
    bpm = composition['bpm'] if 'bpm' in composition else 120
    time_signature = composition['timeSignature'] if 'timeSignature' in composition else {'numerator': 4, 'denominator': 4}
    tracks = composition['tracks'] if 'tracks' in composition else []

    for track_data in tracks:
        track = mido.MidiTrack()
        mid.tracks.append(track)
        # 軌道名稱
        if 'name' in track_data:
            track.append(mido.MetaMessage('track_name', name=track_data['name']))
        # 設定速度
        tempo = mido.bpm2tempo(bpm)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))
        # 設定拍號
        ts = time_signature
        track.append(mido.MetaMessage('time_signature', numerator=ts['numerator'] if 'numerator' in ts else 4, denominator=ts['denominator'] if 'denominator' in ts else 4))
        # 設定樂器
        if 'instrument' in track_data:
            track.append(mido.Message('program_change', program=track_data['instrument'], time=0))
        # 音符
        abs_time = 0
        for note in track_data['notes'] if 'notes' in track_data else []:
            pitch = note['pitch'] if 'pitch' in note else 60
            velocity = note['velocity'] if 'velocity' in note else 100
            duration = note['duration'] if 'duration' in note else '4'
            # 時值轉換為 tick
            duration_map = {'1': 1920, '2': 960, '4': 480, '8': 240, '16': 120, '32': 60, '64': 30}
            ticks = duration_map[str(duration)] if str(duration) in duration_map else 480
            # 處理起始時間
            start_tick = 0
            if 'beat' in note:
                start_tick = int((float(note['beat']) - 1) * 480)
            elif 'startTime' in note:
                start_tick = int(float(note['startTime']) * 480)
            # 計算等待時間
            delta = max(0, start_tick - abs_time)
            abs_time = start_tick
            track.append(mido.Message('note_on', note=int(pitch), velocity=velocity, time=delta))
            track.append(mido.Message('note_off', note=int(pitch), velocity=velocity, time=ticks))
            abs_time += ticks

    # 處理輸出目錄
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    mid.save(output_path)
    return f'MIDI file "{title}" has been generated and saved to {output_path}.'

@mcp.tool()
def play_midi(midi_path: str):
    """
    Play the specified MIDI file using pygame.

    參數說明：
    - midi_path: MIDI 檔案的完整路徑。

    回傳：
    - 播放成功訊息。
    - 若檔案不存在或播放失敗會拋出例外。
    """
    pygame.init()
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(midi_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        raise RuntimeError(f"Failed to play MIDI: {e}")
    finally:
        pygame.mixer.music.stop()
        pygame.quit()
    return f'MIDI file {midi_path} played successfully.'

@mcp.prompt(title="How to compose music with midi-mcp")
def midi_mcp_composing_guide() -> str:
    """
    Prompt for LLM: How to use midi-mcp to compose music (English).

    本函式為 LLM 提供 midi-mcp 使用說明。
    包含 composition 結構、工具參數、範例、注意事項等。
    """
    return (
        "You are an AI music assistant. To compose music using the midi-mcp server, follow these steps:\n"
        "1. Prepare a composition dictionary in Python or JSON format.\n"
        "   - The structure should include: bpm, timeSignature, and one or more tracks.\n"
        "   - Each track should have: name, instrument (as General MIDI program number), and a list of notes.\n"
        "   - Each note should specify: pitch (MIDI number), velocity, duration (note length, e.g., 4 for quarter note), and beat (start position).\n"
        "2. To create a MIDI file, call the create_midi tool with arguments: title, composition (dict), and output_path (filename only, no path).\n"
        "3. To play a MIDI file, call the play_midi tool with the midi_path (full file path).\n"
        "4. Example composition dict:\n"
        "   {\n"
        "     'bpm': 120,\n"
        "     'timeSignature': {'numerator': 4, 'denominator': 4},\n"
        "     'tracks': [\n"
        "       {\n"
        "         'name': 'Piano',\n"
        "         'instrument': 0,\n"
        "         'notes': [\n"
        "           {'pitch': 60, 'velocity': 100, 'duration': 4, 'beat': 1},\n"
        "           {'pitch': 64, 'velocity': 100, 'duration': 4, 'beat': 2},\n"
        "           {'pitch': 67, 'velocity': 100, 'duration': 4, 'beat': 3}\n"
        "         ]\n"
        "       }\n"
        "     ]\n"
        "   }\n"
        "5. For chords, add multiple notes with the same beat.\n"
        "6. For polyphonic/multi-track music, add more tracks.\n"
        "7. Use only filename (not path) for output_path.\n"
        "8. The server will save MIDI files to the default output directory.\n"
        "9. For more details, see the midi-mcp server documentation or ask for more examples.\n"
    )

if __name__ == "__main__":
    mcp.run()
