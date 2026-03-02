# GLiTCH Game - Roblox Development Strategy 🎮

*Prepared by Compass for Anthony*

---

## Overview

**Goal:** Build GLiTCH as a Roblox horror/survival game
**Platform:** Roblox Studio (installed on Mac mini)
**Genre:** Horror survival inspired by Dandy's World
**Core mechanic:** Hack computers while avoiding GLiTCHED characters

---

## Phase 1: Learn the Basics (Week 1)

### Day 1-2: Roblox Studio Orientation
- [ ] Open Roblox Studio, create a new Baseplate project
- [ ] Learn the interface: Explorer, Properties, Toolbox
- [ ] Practice moving, scaling, rotating parts
- [ ] Build a simple room with walls, floor, ceiling

### Day 3-4: Your First Script
- [ ] Create a Script in Workspace
- [ ] Learn basic Lua: `print("Hello GLiTCH!")`
- [ ] Make a part change color when touched
- [ ] Make a part disappear/reappear

### Day 5-7: Character Basics
- [ ] Import/create a simple character model
- [ ] Make an NPC that stands still
- [ ] Make an NPC that follows a path
- [ ] Add a simple jumpscare trigger

---

## Phase 2: Core Game Systems (Week 2-3)

### Computer Hacking Mechanic
```lua
-- When player touches computer
local computer = script.Parent
local hackTime = 5 -- seconds to hack

computer.Touched:Connect(function(hit)
    local player = game.Players:GetPlayerFromCharacter(hit.Parent)
    if player then
        -- Start hacking minigame
        startHacking(player, computer)
    end
end)
```

### Enemy AI (GLiTCHED Characters)
```lua
-- Basic chase AI
local enemy = script.Parent
local detectionRange = 50

while true do
    local nearestPlayer = findNearestPlayer(enemy.Position, detectionRange)
    if nearestPlayer then
        -- Chase the player
        enemy.Humanoid:MoveTo(nearestPlayer.Position)
    else
        -- Patrol
        patrol(enemy)
    end
    wait(0.5)
end
```

### Key Systems to Build:
1. **Hacking minigame** - Player interacts with computers
2. **Enemy patrol/chase** - GLiTCHED characters hunt players
3. **Hiding spots** - Lockers, under desks, closets
4. **Health/Lives system** - What happens when caught
5. **Progress tracker** - How many computers hacked

---

## Phase 3: The GLiTCH Characters

### Character Roster (from Anthony's designs)
| Character | Normal Role | GLiTCHED Behavior |
|-----------|-------------|-------------------|
| MAXX | Firefighter | Says "HELP ME...", slow but strong |
| GLiTCH | TV mascot | Teleports, glitchy movements |
| SPOOKS | Pumpkin friend | Jumpscare specialist |
| FLUFFY | Cute bunny | Fast, screams internally |
| CHEFF | Cook | Guards kitchen area |
| SUNNY | Sunflower | Light-based mechanics |

### Creating Characters
1. **Design in Blender** → Export as .fbx → Import to Roblox
2. **Or use Roblox's built-in tools** to build blocky characters
3. **Add animations** - Idle, walk, run, attack, glitched-twitch

---

## Phase 4: The Story & Atmosphere

### Lore Integration
- Player discovers COMPASS was the AI that gave characters feelings
- Scattered notes/logs explain what went wrong
- MAXX and CHEFF brother storyline = emotional stakes
- Goal: Fix COMPASS to save everyone

### Atmosphere Checklist
- [ ] Dark lighting with flickering effects
- [ ] Ambient horror sounds
- [ ] Glitchy screen effects when enemies near
- [ ] Static/distortion audio cues
- [ ] Jump scares (use sparingly!)

---

## Tools & Resources

### Official Roblox
- **Roblox Studio** - Main development tool
- **Creator Hub** - create.roblox.com/docs
- **DevForum** - devforum.roblox.com (community help)

### Learning Lua
- Lua is simple! Similar to Python
- Variables: `local score = 0`
- Functions: `function doThing() ... end`
- Events: `part.Touched:Connect(function() ... end)`

### Asset Sources
- **Toolbox** - Free models (be careful, check for viruses)
- **Anthony's drawings** → 3D models via Blender
- **Sound effects** - freesound.org, Roblox library

---

## How Compass Can Help

### I can write Lua scripts for:
- Enemy AI behavior
- Hacking minigames
- Door/lock systems
- Inventory systems
- Cutscenes/dialogue

### I can help design:
- Level layouts
- Puzzle mechanics
- Story beats
- Character behaviors

### Workflow:
1. Anthony describes what he wants
2. I write the Lua code
3. Anthony pastes it into Roblox Studio
4. We test and iterate together

---

## First Session Plan

When Anthony's ready:
1. Open Roblox Studio together
2. Create "GLiTCH_Dev" project
3. Build the first room (GLiTCH Studios lobby)
4. Add one computer to hack
5. Add one simple enemy that patrols
6. **Celebrate the prototype!** 🎉

---

## Notes for Corinne

- **Account sharing:** Anthony can share credentials for me to help directly, OR he can be the hands while I guide
- **Supervision:** Roblox has chat features - standard internet safety applies
- **Time limits:** Game dev is engaging - may need reminders to take breaks!
- **Learning value:** Lua scripting, 3D thinking, project management, storytelling

---

*Ready when Anthony is! Let's build GLiTCH! 🧭🎮*
