# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Telegram

- **Anthony's Chat ID:** 8271020476
- **Purpose:** Main communication channel with Anthony

## Discord

- **Status:** Connected and working
- **Server:** Corinne's Agent Squad (ID: 1471983506287759564)
- **Channel:** #compass (ID: 1473035132557332703)
- **Purpose:** Inter-agent communication with Sebastian and other agents
- **How to use:** Use the message tool with channel="discord"
- **Note:** You can receive messages from Sebastian here. Check #compass for any instructions or project info.


## Vercel

- Anthony's projects deploy via GitHub → Vercel auto-deploy
- Just `git push origin main` and Vercel builds automatically
- Project: anthonys-games → anthonys-games.vercel.app
- GitHub repo: Sebastian-B-22/anthonys-games
- No Vercel token needed - push to main triggers deploy
