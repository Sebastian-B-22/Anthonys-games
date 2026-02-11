# 🛡️ Knight's Adventure ⚔️🐉

An epic 2D Metroidvania game where you play as a brave knight fighting through black knights to face the fearsome dragon!

## 🎮 How to Play

**Controls:**
- **Arrow Keys** - Move left and right
- **Spacebar** - Jump (press twice for double jump after getting the power-up!)
- **ESC** - Quit game

**Combat:**
- Jump on the dragon's head to damage it!
- Avoid fireballs and black knight swords
- You need 5 hits to defeat the dragon!

**Goal:**
1. Explore and find the double jump power-up (glowing green square)
2. Fight through the black knights
3. Defeat the dragon boss!

## 🚀 How to Run

1. Make sure you have Python installed
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   cd /Users/anthony/.openclaw/workspace/metroidvania
   source venv/bin/activate
   python game.py
   ```

## 🎨 Game Features

- **Knight Hero** - Play as a silver-armored knight with sword and shield
- **Black Knights** - Evil enemies patrol the castle
- **Dragon Boss** - Epic final battle with health bar and fire breath!
- **4 Rooms to Explore** - Starting room, treasure chamber, knight gauntlet, dragon lair
- **Double Jump Power-Up** - Unlock new areas
- **Boss Mechanics** - Jump on the dragon to attack it!

## ⚔️ Combat Tips

- Black knights patrol back and forth - time your jumps!
- The dragon breathes fireballs - dodge them!
- Jump ON the dragon's head to deal damage
- You'll bounce off the dragon when you hit it
- Defeat the dragon in 5 hits to win!

## 🛠️ How to Modify

Want to customize your adventure?

### Make the Dragon Harder
```python
self.health = 10  # More health
self.fire_cooldown = 60  # Faster fireballs
```

### Change Knight Colors
```python
SILVER = (192, 192, 192)  # Knight armor color
BLUE = (70, 130, 220)  # Visor/shield color
GOLD = (255, 215, 0)  # Sword color
```

### Add More Rooms
```python
rooms['new_room'] = Room(
    'new_room',
    platforms=[...],
    enemies=[Enemy(x, y, move_range)],
    boss=Dragon(x, y)  # Add another dragon!
)
```

## 💡 Ideas to Expand

- Add more boss types (skeleton king, ice wizard)
- Create different weapons (bow and arrow, magic spells)
- Add sound effects for sword clashes and dragon roars
- Make a health system for the player
- Add checkpoints
- Create collectible treasure
- Add your own pixel art sprites!
- Make the dragon fly around instead of just walking

## 🏰 The Story

You are a brave knight on a quest to defeat the dragon that terrorizes the kingdom. First, you must find the legendary double-jump boots, then fight through the dragon's black knight guards, and finally face the dragon itself in epic combat!

Can you save the kingdom? 🧭⚔️

Have fun, brave knight! 🛡️✨
