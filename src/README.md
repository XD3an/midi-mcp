# midi-mcp

本目錄為 MIDI MCP 伺服器的 Python 實作，支援透過 Model Context Protocol (MCP) 創建與播放 MIDI 檔案。

## 可用工具

- **`create_midi(title: str, composition: dict = None, composition_file: str = None, output_path: str = None)`**

  - 使用 `mido` 函式庫生成 MIDI 檔案。
  - **參數說明：**
    - `title`：MIDI 檔案標題（作為檔名）。
    - `composition`：描述樂曲內容的字典（BPM、拍號、軌道、音符等）。
    - `composition_file`：包含樂曲資料的 JSON 檔案路徑。
    - `output_path`：輸出檔名（僅檔名，不含路徑），預設儲存於指定輸出目錄。
  - **回傳：** 成功訊息與生成的 MIDI 檔案路徑。

- **`play_midi(midi_path: str)`**
  - 使用 `pygame` 播放指定的 MIDI 檔案。
  - **參數說明：**
    - `midi_path`：要播放的 MIDI 檔案完整路徑。
  - **回傳：** 播放完成訊息。

## 快速安裝與啟動

1. 安裝依賴：

```bash
uv sync
```

2. 啟動伺服器（可自訂輸出目錄）：

```bash
uv run server.py --output_directory midi_output
```

在支援 MCP Server 的 Client 端上（例如：Claude Desktop）設定，其中 `\\PATH\\TO\\midi-mcp\\src` 為實際的 MIDI MCP 檔案路徑，`\\PATH\\TO\\midi_output` 為輸出目錄：

### Claude Desktop MCP Server 設定

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

### VSCode MCP Server 設定

在專案下的 [.vscode/mcp.json](.vscode/mcp.json) 檔案中設定：

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

## 使用範例

可透過支援 MCP 的 LLM 進行互動。

**用戶提示：**

```
我想要創作一首純鋼琴曲，請生成一個 C 大調的旋律，並包含和弦，最後播放出來。
```

LLM 會自動呼叫 `create_midi` 產生樂曲，再呼叫 `play_midi` 播放。

### `composition` 結構範例：

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

### 檔案輸出

所有生成的 MIDI 檔案將儲存於啟動伺服器時 `--output_directory` 指定的目錄（預設為上層的 `midi_output/`）。

## 授權

[MIT LICENCE](./LICENCE)
