import argparse
import json
import os

import mido
import pygame
from mcp.server.fastmcp import FastMCP

parser = argparse.ArgumentParser(description="MIDI MCP server (Python version)")
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
    使用 mido 庫生成 MIDI 檔案。

    參數:
    - title: MIDI 檔案的標題（用於檔名）。
    - composition: 音樂作品的字典格式，包含 bpm、timeSignature 和 tracks。
    - composition_file: 音樂作品的 JSON 檔案路徑（如果提供，則忽略 composition 參數）。
    - output_path: 輸出檔案的路徑（只允許檔名，不含路徑，預設為 output_directory 下的檔名）。

    返回:
    - 成功訊息，包含生成的 MIDI 檔案路徑。
    """
    if not title:
        raise ValueError("You must provide 'title' (英文) 作為檔名。")
    # 若未指定輸出路徑，則自動放到 output_directory 下
    # output_path 只允許檔名（不含路徑）
    if output_path:
        if os.path.basename(output_path) != output_path:
            raise ValueError("output_path 只能是檔名，不能包含路徑。")
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

    abs_output_dir = os.path.abspath(default_output_dir)
    abs_output_path = os.path.abspath(output_path)
    if not abs_output_path.startswith(abs_output_dir + os.sep):
        raise ValueError(f"Output path must be inside the output directory: {default_output_dir}")

    # MIDI 生成
    mid = mido.MidiFile()
    bpm = composition.get('bpm', 120)
    time_signature = composition.get('timeSignature', {'numerator': 4, 'denominator': 4})
    tracks = composition.get('tracks', [])

    for track_data in tracks:
        track = mido.MidiTrack()
        mid.tracks.append(track)
        # 軌道名稱
        if track_data.get('name'):
            track.append(mido.MetaMessage('track_name', name=track_data['name']))
        # 設定速度
        tempo = mido.bpm2tempo(bpm)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))
        # 設定拍號
        ts = time_signature
        track.append(mido.MetaMessage('time_signature', numerator=ts.get('numerator',4), denominator=ts.get('denominator',4)))
        # 設定樂器
        if 'instrument' in track_data:
            track.append(mido.Message('program_change', program=track_data['instrument'], time=0))
        # 音符
        abs_time = 0
        for note in track_data.get('notes', []):
            pitch = note.get('pitch', 60)
            velocity = note.get('velocity', 100)
            duration = note.get('duration', '4')
            # 時值轉換為 tick
            duration_map = {'1': 1920, '2': 960, '4': 480, '8': 240, '16': 120, '32': 60, '64': 30}
            ticks = duration_map.get(str(duration), 480)
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
    使用 pygame 播放指定的 MIDI 檔案。
    """
    # 初始化 pygame mixer
    pygame.init()
    try:
        pygame.mixer.init()
        # 載入 MIDI 檔案
        pygame.mixer.music.load(midi_path)
        # 播放 MIDI
        pygame.mixer.music.play()
        # 等待播放結束
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
    """Prompt for LLM: How to use midi-mcp to compose music (English)."""
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
    mcp.run()
