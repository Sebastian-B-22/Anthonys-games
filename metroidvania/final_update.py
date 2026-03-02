#!/usr/bin/env python3
"""Comprehensive game update script"""

import re

# Read the clean backup
with open('game_clean.py', 'r') as f:
    content = f.read()

# 1. Change background to white (simple)
content = content.replace('draw_castle_background(screen)', 'screen.fill(WHITE)')

# 2. Remove castle background function completely
pattern = r'def draw_castle_background\(screen\):.*?(?=\nclass|\ndef [a-z_]+\()'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# 3. Move dragon to ground level
content = content.replace('boss=Dragon(300, 470)', 'boss=Dragon(300, 470)')  # Already at 470

# 4. Add new enemy classes before create_rooms function
skeleton_classes = '''
class Skeleton:
    """Spooky skeleton enemy"""
    def __init__(self, x, y, move_range):
        self.x, self.y, self.start_x = x, y, x
        self.width, self.height = 25, 40
        self.speed, self.move_range, self.direction = 2.5, move_range, 1
        self.health, self.hit_flash = 3, 0
        
    def update(self):
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 10
        return self.health <= 0
    
    def draw(self, screen):
        color = WHITE if (self.hit_flash > 0 and (self.hit_flash // 2) % 2 == 0) else (240, 240, 230)
        pygame.draw.circle(screen, color, (int(self.x + 12), int(self.y + 10)), 10)
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y + 8)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + 16), int(self.y + 8)), 3)
        pygame.draw.circle(screen, GREEN, (int(self.x + 8), int(self.y + 8)), 2)
        pygame.draw.circle(screen, GREEN, (int(self.x + 16), int(self.y + 8)), 2)
        pygame.draw.polygon(screen, BLACK, [(self.x + 11, self.y + 12), (self.x + 13, self.y + 12), (self.x + 12, self.y + 15)])
        for tx in range(3):
            pygame.draw.rect(screen, BLACK, (self.x + 8 + tx*3, self.y + 16, 2, 3))
        pygame.draw.rect(screen, color, (self.x + 10, self.y + 20, 4, 15))
        for rib_y in [22, 26, 30]:
            pygame.draw.line(screen, color, (self.x + 7, self.y + rib_y), (self.x + 17, self.y + rib_y), 2)
        pygame.draw.line(screen, color, (self.x + 6, self.y + 22), (self.x + 2, self.y + 30), 3)
        pygame.draw.line(screen, color, (self.x + 18, self.y + 22), (self.x + 22, self.y + 30), 3)
        pygame.draw.line(screen, color, (self.x + 10, self.y + 35), (self.x + 8, self.y + 40), 3)
        pygame.draw.line(screen, color, (self.x + 14, self.y + 35), (self.x + 16, self.y + 40), 3)

class BoneProjectile:
    def __init__(self, x, y, direction):
        self.x, self.y, self.direction, self.speed = x, y, direction, 5
    def update(self):
        self.x += self.speed * self.direction
    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 230), (self.x - 4, self.y - 2, 8, 4))
        pygame.draw.circle(screen, (240, 240, 230), (int(self.x - 4), int(self.y)), 3)
        pygame.draw.circle(screen, (240, 240, 230), (int(self.x + 4), int(self.y)), 3)

class SkeletonBoss:
    def __init__(self, x, y):
        self.x, self.y, self.width, self.height = x, y, 60, 80
        self.health, self.max_health = 20, 20
        self.direction, self.move_speed, self.start_x, self.move_range = 1, 2, x, 200
        self.attack_cooldown, self.bones, self.hit_flash = 0, [], 0
        
    def update(self):
        self.x += self.move_speed * self.direction
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.bones.append(BoneProjectile(self.x + 30, self.y + 30, self.direction))
            self.attack_cooldown = 60
        for bone in self.bones[:]:
            bone.update()
            if bone.x < -20 or bone.x > 820:
                self.bones.remove(bone)
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 15
    
    def is_alive(self):
        return self.health > 0
    
    def draw(self, screen):
        color = WHITE if (self.hit_flash > 0 and (self.hit_flash // 3) % 2 == 0) else (240, 240, 230)
        pygame.draw.circle(screen, color, (int(self.x + 30), int(self.y + 20)), 20)
        pygame.draw.circle(screen, BLACK, (int(self.x + 20), int(self.y + 15)), 6)
        pygame.draw.circle(screen, BLACK, (int(self.x + 40), int(self.y + 15)), 6)
        pygame.draw.circle(screen, RED, (int(self.x + 20), int(self.y + 15)), 4)
        pygame.draw.circle(screen, RED, (int(self.x + 40), int(self.y + 15)), 4)
        pygame.draw.polygon(screen, BLACK, [(self.x + 28, self.y + 22), (self.x + 32, self.y + 22), (self.x + 30, self.y + 28)])
        for tx in range(6):
            pygame.draw.rect(screen, BLACK, (self.x + 18 + tx*4, self.y + 32, 3, 5))
        pygame.draw.rect(screen, color, (self.x + 26, self.y + 40, 8, 30))
        for rib_y in [44, 50, 56, 62]:
            pygame.draw.line(screen, color, (self.x + 15, self.y + rib_y), (self.x + 45, self.y + rib_y), 4)
        pygame.draw.line(screen, color, (self.x + 12, self.y + 45), (self.x, self.y + 60), 5)
        pygame.draw.line(screen, color, (self.x + 48, self.y + 45), (self.x + 60, self.y + 60), 5)
        pygame.draw.line(screen, color, (self.x + 22, self.y + 70), (self.x + 18, self.y + 80), 5)
        pygame.draw.line(screen, color, (self.x + 38, self.y + 70), (self.x + 42, self.y + 80), 5)
        bar_width, bar_height = 60, 8
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x, self.y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, DARK_RED, (self.x, self.y - 15, bar_width * health_percent, bar_height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y - 15, bar_width, bar_height), 1)
        for bone in self.bones:
            bone.draw(screen)

'''

content = content.replace('def create_rooms(player):', skeleton_classes + '\ndef create_rooms(player):')

# 5. Add new rooms
new_rooms = '''
    # Parkour/Obby Room
    rooms['obby'] = Room(
        'obby',
        platforms=[
            pygame.Rect(0, 550, 150, 50),
            pygame.Rect(200, 480, 80, 20),
            pygame.Rect(350, 420, 80, 20),
            pygame.Rect(500, 360, 80, 20),
            pygame.Rect(350, 300, 80, 20),
            pygame.Rect(200, 240, 80, 20),
            pygame.Rect(400, 180, 120, 20),
            pygame.Rect(650, 180, 150, 20),
        ]
    )
    
    rooms['skeletons'] = Room(
        'skeletons',
        platforms=[pygame.Rect(0, 550, 800, 50), pygame.Rect(150, 450, 120, 20), pygame.Rect(500, 450, 120, 20)],
        skeletons=[Skeleton(250, 510, 120), Skeleton(550, 510, 150)]
    )
    
    rooms['skeleton_boss'] = Room(
        'skeleton_boss',
        platforms=[pygame.Rect(0, 550, 800, 50), pygame.Rect(150, 420, 100, 20), pygame.Rect(550, 420, 100, 20)],
        skeleton_boss=SkeletonBoss(350, 470)
    )
'''

content = content.replace('    return rooms', new_rooms + '\n    return rooms')

# 6. Update Room class
content = content.replace(
    'def __init__(self, name, platforms, items=None, enemies=None, elite_enemies=None, gates=None, boss=None, bench=None):',
    'def __init__(self, name, platforms, items=None, enemies=None, elite_enemies=None, gates=None, boss=None, bench=None, skeletons=None, skeleton_boss=None):'
)
content = content.replace(
    'self.bench = bench',
    'self.bench = bench\n        self.skeletons = skeletons if skeletons else []\n        self.skeleton_boss = skeleton_boss'
)

# Write the final version
with open('game.py', 'w') as f:
    f.write(content)

print("Game updated successfully!")
