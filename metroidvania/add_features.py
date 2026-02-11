#!/usr/bin/env python3
"""Script to add castle background, healing bench, and heart upgrade features"""

with open('game.py', 'r') as f:
    lines = f.readlines()

# Find where to insert new code
output = []
i = 0

while i < len(lines):
    line = lines[i]
    output.append(line)
    
    # Add castle colors after existing colors
    if 'CYAN = (0, 255, 255)' in line:
        output.append('STONE_GRAY = (80, 80, 80)\n')
        output.append('STONE_LIGHT = (110, 110, 110)\n')
        output.append('TORCH_FLAME = (255, 100, 0)\n')
        output.append('\n')
        output.append('def draw_castle_background(screen):\n')
        output.append('    """Draw castle themed background"""\n')
        output.append('    # Stone wall\n')
        output.append('    for y in range(0, SCREEN_HEIGHT, 40):\n')
        output.append('        for x in range(0, SCREEN_WIDTH, 60):\n')
        output.append('            pygame.draw.rect(screen, STONE_GRAY, (x, y, 58, 38))\n')
        output.append('            pygame.draw.rect(screen, STONE_LIGHT, (x+2, y+2, 54, 34))\n')
        output.append('            pygame.draw.line(screen, DARK_GRAY, (x, y), (x+58, y), 1)\n')
        output.append('            pygame.draw.line(screen, DARK_GRAY, (x, y), (x, y+38), 1)\n')
        output.append('    \n')
        output.append('    # Torches\n')
        output.append('    for x in [100, 400, 700]:\n')
        output.append('        # Torch holder\n')
        output.append('        pygame.draw.rect(screen, DARK_GRAY, (x-2, 150, 4, 30))\n')
        output.append('        pygame.draw.circle(screen, TORCH_FLAME, (x, 145), 8)\n')
        output.append('        pygame.draw.circle(screen, ORANGE, (x, 145), 5)\n')
        output.append('        pygame.draw.circle(screen, YELLOW, (x, 145), 2)\n')
        output.append('    \n')
        output.append('    # Banners\n')
        output.append('    for x in [200, 600]:\n')
        output.append('        pygame.draw.rect(screen, BLUE, (x, 80, 30, 60))\n')
        output.append('        pygame.draw.polygon(screen, BLUE, [(x, 140), (x+15, 150), (x+30, 140)])\n')
        output.append('        pygame.draw.circle(screen, GOLD, (x+15, 110), 8)\n')
        output.append('\n')
    
    # Add HealingBench class after Fireball class
    if 'class Fireball:' in line and 'def __init__' in lines[i+1]:
        # Skip to end of Fireball class
        while i < len(lines) and not (i > 0 and lines[i].strip() and not lines[i].startswith(' ')):
            output.append(lines[i])
            i += 1
        i -= 1  # Back up one
        
        output.append('\n')
        output.append('class HealingBench:\n')
        output.append('    """A bench that heals the player"""\n')
        output.append('    def __init__(self, x, y):\n')
        output.append('        self.x = x\n')
        output.append('        self.y = y\n')
        output.append('        self.width = 60\n')
        output.append('        self.height = 20\n')
        output.append('        self.glow = 0\n')
        output.append('    \n')
        output.append('    def update(self):\n')
        output.append('        self.glow = (self.glow + 0.05) % (2 * math.pi)\n')
        output.append('    \n')
        output.append('    def draw(self, screen):\n')
        output.append('        glow_intensity = int(abs(math.sin(self.glow)) * 30)\n')
        output.append('        glow_color = (0, 200 + glow_intensity, 100 + glow_intensity)\n')
        output.append('        \n')
        output.append('        # Glow effect\n')
        output.append('        pygame.draw.ellipse(screen, glow_color, (self.x-5, self.y-5, self.width+10, self.height+10))\n')
        output.append('        \n')
        output.append('        # Bench seat\n')
        output.append('        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, 8))\n')
        output.append('        pygame.draw.rect(screen, DARK_BROWN, (self.x+2, self.y+2, self.width-4, 4))\n')
        output.append('        \n')
        output.append('        # Bench legs\n')
        output.append('        pygame.draw.rect(screen, BROWN, (self.x+5, self.y+8, 6, 12))\n')
        output.append('        pygame.draw.rect(screen, BROWN, (self.x+self.width-11, self.y+8, 6, 12))\n')
        output.append('        \n')
        output.append('        # Healing cross symbol\n')
        output.append('        pygame.draw.rect(screen, WHITE, (self.x+26, self.y-10, 8, 18))\n')
        output.append('        pygame.draw.rect(screen, WHITE, (self.x+21, self.y-5, 18, 8))\n')
        output.append('        pygame.draw.rect(screen, GREEN, (self.x+27, self.y-9, 6, 16))\n')
        output.append('        pygame.draw.rect(screen, GREEN, (self.x+22, self.y-4, 16, 6))\n')
        output.append('\n')
    
    i += 1

# Write the modified content
with open('game_temp.py', 'w') as f:
    f.writelines(output)

print("Features added! Now updating item collection and room definitions...")

# Read the temp file and add item collection logic
with open('game_temp.py', 'r') as f:
    content = f.read()

# Add heart upgrade collection logic
old_collect = '''if item.item_type == 'double_jump':
                            player.has_double_jump = True
                            message = "DOUBLE JUMP unlocked! Press UP twice!"
                            message_timer = 180'''

new_collect = '''if item.item_type == 'double_jump':
                            player.has_double_jump = True
                            message = "DOUBLE JUMP unlocked! Press UP twice!"
                            message_timer = 180
                        elif item.item_type == 'heart_upgrade':
                            player.max_health += 1
                            player.health = player.max_health
                            message = "MAX HEALTH INCREASED! +1 Heart!"
                            message_timer = 180'''

content = content.replace(old_collect, new_collect)

# Add new rooms in create_rooms function
old_dragon_room = '''    rooms['dragon'] = Room(
        'dragon',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 400, 100, 20),
            pygame.Rect(600, 400, 100, 20),
        ],
        boss=Dragon(300, 470)
    )
    
    return rooms'''

new_rooms = '''    rooms['dragon'] = Room(
        'dragon',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 400, 100, 20),
            pygame.Rect(600, 400, 100, 20),
        ],
        boss=Dragon(300, 470)
    )
    
    # NEW: Heart Upgrade Room
    rooms['heart_upgrade'] = Room(
        'heart_upgrade',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(350, 450, 100, 20),
        ],
        items=[
            Item(370, 410, 'heart_upgrade', CRIMSON)
        ]
    )
    
    # NEW: Healing Bench Room  
    rooms['healing'] = Room(
        'healing',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(300, 480, 200, 20),
        ]
    )
    
    return rooms'''

content = content.replace(old_dragon_room, new_rooms)

# Add Room class bench support
old_room_init = '''class Room:
    def __init__(self, name, platforms, items=None, enemies=None, elite_enemies=None, gates=None, boss=None):
        self.name = name
        self.platforms = platforms
        self.items = items if items else []
        self.enemies = enemies if enemies else []
        self.elite_enemies = elite_enemies if elite_enemies else []
        self.gates = gates if gates else []
        self.boss = boss'''

new_room_init = '''class Room:
    def __init__(self, name, platforms, items=None, enemies=None, elite_enemies=None, gates=None, boss=None, bench=None):
        self.name = name
        self.platforms = platforms
        self.items = items if items else []
        self.enemies = enemies if enemies else []
        self.elite_enemies = elite_enemies if elite_enemies else []
        self.gates = gates if gates else []
        self.boss = boss
        self.bench = bench'''

content = content.replace(old_room_init, new_room_init)

# Add bench to healing room
content = content.replace(
    "rooms['healing'] = Room(\n        'healing',\n        platforms=[\n            pygame.Rect(0, 550, 800, 50),\n            pygame.Rect(300, 480, 200, 20),\n        ]\n    )",
    "rooms['healing'] = Room(\n        'healing',\n        platforms=[\n            pygame.Rect(0, 550, 800, 50),\n            pygame.Rect(300, 480, 200, 20),\n        ],\n        bench=HealingBench(370, 460)\n    )"
)

# Write final version
with open('game.py', 'w') as f:
    f.write(content)

print("All features added successfully!")
