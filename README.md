# midi-mcp

## 可用工具

- **create_midi**：產生 MIDI 檔案。

  - 參數：
    - `title`：MIDI 檔案標題（作為檔名）。
    - `composition`：描述樂曲的字典（BPM、拍號、軌道、音符）。
    - `composition_file`：包含樂曲資料的 JSON 檔案路徑。
    - `output_path`：輸出檔名（僅檔名，不含路徑），預設儲存於指定輸出目錄。
  - 回傳：成功訊息與檔案路徑。

- **play_midi**：播放指定 MIDI 檔案。
  - 參數：
    - `midi_path`：MIDI 檔案完整路徑。
  - 回傳：播放成功訊息。

## 快速安裝與啟動

1. 安裝依賴：

   從專案根目錄執行：

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

## 使用說明

你可以對支援 MCP 的 LLM 發出如下指令：

```
我想要創作一首純鋼琴曲，請生成一個 C 大調的旋律，並包含和弦，最後播放出來。
```

LLM 會自動呼叫 `create_midi` 產生樂曲，再呼叫 `play_midi` 播放。

### 範例 composition 結構：

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

所有產生的 MIDI 檔案會自動儲存在啟動伺服器時指定的 `--output_directory` 目錄（預設為 `midi_output/`）。

---

## 授權

本專案採用 MIT 授權。詳見 [../LICENCE](../LICENCE)。
