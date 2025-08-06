# MIDI MCP Server

支援 MIDI 檔案創建、旋律/和弦/鼓點自動生成、MIDI 分析、播放與音樂理論查詢，適合自動鋼琴、AI 音樂生成、教學與研究。

## 可用工具

- `create_midi_file(filename, tempo, time_signature_num, time_signature_den)`：創建新 MIDI 檔案
- `add_chord_progression(filename, progression_params)`：新增和弦進行
- `add_melody_to_midi(filename, melody_params)`：新增旋律
- `add_drum_pattern(filename, drum_params)`：新增鼓點
- `generate_beethoven_symphony5()`：生成貝多芬第五號交響曲主題
- `analyze_midi_file(filename)`：分析 MIDI 檔案
- `convert_midi_to_text(filename)`：MIDI 轉文字
- `play_midi_file(filename)`：播放 MIDI 檔案
- `list_chord_types()`：列出支援的和弦類型
- `list_scale_types()`：列出支援的音階類型
- `list_midi_files()`：列出所有 MIDI 檔案

## 快速安裝與啟動

1. 安裝依賴：

```bash
uv sync
```

2. 啟動伺服器（可自訂輸出目錄）：

```bash
uv run server.py --output_directory midi_output
```

在支援 MCP Server 的 Client 端上（例如：Claude Desktop）設定：

## Claude Desktop MCP Server 設定

```json
"midi-mcp": {
  "command": "uv",
  "args": [
    "--directory",
    "D:/All_In_One/Documents/Project/github/auto-midi-piano/src/ai/midi-mcp/",
    "run",
    "server.py",
    "--output_directory",
    "D:/All_In_One/Documents/Project/github/auto-midi-piano/src/ai/midi-mcp/midi_output"
  ]
}
```

### VSCde MCP Server 設定

在專案下的 [.vscode/mcp.json](.vscode/mcp.json) 檔案中設定，其中 \\PATH\\TO\\midi-mcp\\src 為實際的 MIDI MCP 檔案路徑，\\PATH\\TO\\midi_output 為輸出目錄：

````json
{
  "version": "1.0",
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


## 使用說明

告訴 LLM:

```
我想要創作一首純鋼琴曲，請生成一個 C 大調的旋律，並包含和弦，最後播放出來。
```

## LLM 會自動使用以下工具：

### 常用範例

```python
# 創建 MIDI 檔案
create_midi_file("my_song.mid", tempo=120, time_signature_num=4, time_signature_den=4)

# 新增和弦進行
add_chord_progression("my_song.mid", {"chords": ["C", "Am", "F", "G"], "duration_per_chord": 1920, "octave": 3})

# 新增旋律
add_melody_to_midi("my_song.mid", {"scale": "major", "key": "C", "octave": 5, "note_count": 32})

# 新增鼓點
add_drum_pattern("my_song.mid", {"kick_pattern": [True, False] * 4})

# 播放
play_midi_file("my_song.mid")

# 分析
analyze_midi_file("my_song.mid")

# 轉文字
convert_midi_to_text("my_song.mid")
```

### 檔案輸出

所有生成的 MIDI 檔案如果未指定，會自動儲存在 `midi_output/` 目錄。

## LICENSE

[MIT License](LICENSE)

## 參考資料

- [Mido Documentation](https://mido.readthedocs.io/en/stable/)
````
