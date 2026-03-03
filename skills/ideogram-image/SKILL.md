Terminator1322
# Ideogram Image Generation

Generate images using Ideogram API - great for trading cards, text in images, logos.

## Usage

```bash
node /Users/anthony/.openclaw/workspace/skills/ideogram-image/generate.mjs \
  --prompt "A soccer trading card for Anthony, midfielder, age 12" \
  --output ./my-card.png
```

## Options
- `--prompt` - Image description (be detailed!)
- `--output` - Where to save the image
- `--style` - Style preset: AUTO, REALISTIC, DESIGN, RENDER_3D, ANIME

## Tips for Trading Cards
- Include player name, position, stats in the prompt
- Use "trading card design" or "sports card" in prompt
- Mention colors, style (cartoon, realistic, etc.)
- Add "vibrant colors" for eye-catching results

## Example Prompts
- "A colorful soccer trading card for player Anthony, midfielder #10, cartoon style"
- "Sports trading card design, Anthony Rodriguez, youth soccer star, action pose"
