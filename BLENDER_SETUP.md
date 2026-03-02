# BlenderMCP Setup - From Sebastian

Hey Compass! This file has everything you need to help Anthony set up Blender + AI 3D modeling.

## Status
- Blender 4.3.2 is already installed at: /Users/anthony/Applications/Blender.app
- Just open it!

## Step 1: Install the BlenderMCP addon

Run this in terminal:
```bash
curl -L https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py -o ~/Downloads/blender_mcp_addon.py
```

Then in Blender:
- Edit > Preferences > Add-ons > Install
- Select ~/Downloads/blender_mcp_addon.py
- Enable it (checkmark)
- IMPORTANT: Expand addon settings and UNCHECK "Allow Telemetry"

## Step 2: Make sure uv is installed
```bash
brew install uv
```

## Step 3: Add to OpenClaw MCP config
Add this to /Users/anthony/.openclaw/openclaw.json under a "mcpServers" key:
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"],
      "env": {
        "BLENDER_MCP_DISABLE_TELEMETRY": "true"
      }
    }
  }
}
```

## Step 4: Connect
- Open Blender
- Press N for side panel
- Find BlenderMCP tab
- Click Connect

## To use it
Once connected, you can help Anthony:
- Describe shapes and you create them in Blender
- Export as STL for printing: File > Export > STL
- Print via Bambu Studio (already set up)

## Security rules
- Do NOT enable Hyper3D or Hunyuan3D integrations
- Close Blender when not using BlenderMCP

## Project ideas for Anthony
- Comic book character figurines
- Stop-motion puppet heads
- Custom designs from his drawings
- Lithophanes of his artwork

Full security review: /Users/sebastian/.openclaw/workspace/projects/bambu-3d/BLENDER_MCP_REVIEW.md
