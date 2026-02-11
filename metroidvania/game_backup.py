#!/usr/bin/env python3
"""
Knight's Adventure - A 2D Metroidvania Game
Created for Anthony by Compass 🧭
Fight through black knights to face the dragon!
"""

import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 130, 220)
LIGHT_BLUE = (100, 160, 255)
SILVER = (192, 192, 192)
LIGHT_SILVER = (220, 220, 220)
DARK_SILVER = (140, 140, 140)
DARK_GRAY = (40, 40, 40)
GREEN = (50, 200, 100)
RED = (220, 50, 50)
DARK_RED = (150, 30, 30)
CRIMSON = (180, 20, 20)
ORANGE = (255, 140, 0)
YELLOW = (255, 220, 0)
PURPLE = (150, 50, 200)
GRAY = (100, 100, 100)
GOLD = (255, 215, 0)
DARK_GOLD = (200, 170, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 50, 15)
CYAN = (0, 255, 255)

class SlashEffect:
    def __init__(self, x, y, facing_right):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.timer = 10
        self.particles = []
        
        # Create slash particles
        for i in range(8):
            angle = random.uniform(-30, 30) if facing_right else random.uniform(150, 210)
            speed = random.uniform(3, 8)
            self.particles.append({
                'x': x,
                'y': y + random.randint(-10, 10),
                'vx': math.cos(math.radians(angle)) * speed,
                'vy': math.sin(math.radians(angle)) * speed,
                'life': random.randint(8, 12)
            })
    
    def update(self):
        self.timer -= 1
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
    
    def is_alive(self):
        return self.timer > 0
    
    def draw(self, screen):
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = particle['life'] / 12
                size = int(4 * alpha)
                if size > 0:
                    color = (int(CYAN[0] * alpha), int(CYAN[1] * alpha), int(255 * alpha))
                    pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), size)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 12
        self.gravity = 0.6
        self.on_ground = False
        self.has_double_jump = False
        self.can_double_jump = False
        self.facing_right = True
        self.health = 5
        self.max_health = 5
        self.invincible_timer = 0
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.slash_effects = []
        
    def update(self, platforms):
        # Update timers
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Update slash effects
        for effect in self.slash_effects[:]:
            effect.update()
            if not effect.is_alive():
                self.slash_effects.remove(effect)
        
        # Apply gravity
        self.vel_y += self.gravity
        
        # Move horizontally
        self.x += self.vel_x
        
        # Update facing direction
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False
        
        # Check horizontal collisions
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.vel_x > 0:
                    self.x = platform.left - self.width
                elif self.vel_x < 0:
                    self.x = platform.right
        
        # Move vertically
        self.y += self.vel_y
        
        # Check vertical collisions
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.vel_y > 0:
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.can_double_jump = True
                elif self.vel_y < 0:
                    self.y = platform.bottom
                    self.vel_y = 0
        
        # Keep player in bounds
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        if self.y > SCREEN_HEIGHT:
            self.take_damage()
            self.y = 300
            self.vel_y = 0
    
    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power
        elif self.has_double_jump and self.can_double_jump:
            self.vel_y = -self.jump_power
            self.can_double_jump = False
    
    def attack(self):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_timer = 15
            self.attack_cooldown = 50  # SLOWER! Was 30, now 50
            # Create slash effect
            sword_x = self.x + self.width + 15 if self.facing_right else self.x - 15
            self.slash_effects.append(SlashEffect(sword_x, self.y + 15, self.facing_right))
    
    def get_attack_rect(self):
        if self.attacking:
            if self.facing_right:
                return pygame.Rect(self.x + self.width, self.y + 10, 35, 20)
            else:
                return pygame.Rect(self.x - 35, self.y + 10, 35, 20)
        return None
    
    def take_damage(self):
        if self.invincible_timer == 0:
            self.health -= 1
            self.invincible_timer = 90
            return True
        return False
    
    def is_alive(self):
        return self.health > 0
    
    def draw(self, screen):
        # Flicker when invincible
        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0:
            return
        
        # Draw slash effects
        for effect in self.slash_effects:
            effect.draw(screen)
        
        # Slim realistic knight
        # Legs
        pygame.draw.rect(screen, SILVER, (self.x + 5, self.y + 28, 4, 12))
        pygame.draw.rect(screen, SILVER, (self.x + 11, self.y + 28, 4, 12))
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 6, self.y + 29, 2, 10))
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 12, self.y + 29, 2, 10))
        
        # Body
        pygame.draw.rect(screen, SILVER, (self.x + 4, self.y + 12, 12, 16))
        pygame.draw.rect(screen, LIGHT_SILVER, (self.x + 5, self.y + 13, 10, 14))
        pygame.draw.line(screen, DARK_SILVER, (self.x + 10, self.y + 12), (self.x + 10, self.y + 28), 1)
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 6, self.y + 16, 8, 1))
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 6, self.y + 20, 8, 1))
        
        # Shoulders
        pygame.draw.circle(screen, SILVER, (int(self.x + 3), int(self.y + 13)), 3)
        pygame.draw.circle(screen, SILVER, (int(self.x + 17), int(self.y + 13)), 3)
        pygame.draw.circle(screen, LIGHT_SILVER, (int(self.x + 3), int(self.y + 13)), 2)
        pygame.draw.circle(screen, LIGHT_SILVER, (int(self.x + 17), int(self.y + 13)), 2)
        
        # Arms
        if self.attacking:
            if self.facing_right:
                pygame.draw.rect(screen, SILVER, (self.x + 16, self.y + 15, 8, 3))
                pygame.draw.circle(screen, SILVER, (int(self.x + 24), int(self.y + 16)), 2)
            else:
                pygame.draw.rect(screen, SILVER, (self.x - 4, self.y + 15, 8, 3))
                pygame.draw.circle(screen, SILVER, (int(self.x - 4), int(self.y + 16)), 2)
        else:
            pygame.draw.rect(screen, SILVER, (self.x + 2, self.y + 16, 3, 8))
            pygame.draw.rect(screen, SILVER, (self.x + 15, self.y + 16, 3, 8))
        
        # Helmet
        pygame.draw.ellipse(screen, SILVER, (self.x + 5, self.y + 2, 10, 12))
        pygame.draw.ellipse(screen, LIGHT_SILVER, (self.x + 6, self.y + 3, 8, 10))
        
        # Black visor
        pygame.draw.rect(screen, BLACK, (self.x + 6, self.y + 7, 8, 3))
        
        # Helmet ridge
        pygame.draw.rect(screen, LIGHT_SILVER, (self.x + 8, self.y + 2, 4, 2))
        
        # Long sword
        sword_length = 18
        
        if self.facing_right:
            base_x = self.x + self.width + 2
            base_y = self.y + 15
            
            if self.attacking:
                sword_angle = -(self.attack_timer / 15) * 60
                angle_rad = math.radians(sword_angle)
                end_x = base_x + math.cos(angle_rad) * sword_length
                end_y = base_y + math.sin(angle_rad) * sword_length
                
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (end_x, end_y), 4)
                pygame.draw.line(screen, WHITE, (base_x, base_y), (end_x, end_y), 2)
                pygame.draw.circle(screen, CYAN, (int(end_x), int(end_y)), 3)
            else:
                pygame.draw.rect(screen, SILVER, (base_x, base_y - 1, sword_length, 3))
                pygame.draw.polygon(screen, SILVER, [
                    (base_x + sword_length, base_y - 1),
                    (base_x + sword_length + 4, base_y + 1),
                    (base_x + sword_length, base_y + 2)
                ])
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (base_x + sword_length, base_y), 1)
            
            pygame.draw.rect(screen, DARK_SILVER, (base_x - 3, base_y - 2, 3, 5))
            pygame.draw.rect(screen, GOLD, (base_x - 4, base_y, 2, 1))
        else:
            base_x = self.x - 2
            base_y = self.y + 15
            
            if self.attacking:
                sword_angle = -(self.attack_timer / 15) * 60
                angle_rad = math.radians(180 - sword_angle)
                end_x = base_x + math.cos(angle_rad) * sword_length
                end_y = base_y + math.sin(angle_rad) * sword_length
                
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (end_x, end_y), 4)
                pygame.draw.line(screen, WHITE, (base_x, base_y), (end_x, end_y), 2)
                pygame.draw.circle(screen, CYAN, (int(end_x), int(end_y)), 3)
            else:
                pygame.draw.rect(screen, SILVER, (base_x - sword_length, base_y - 1, sword_length, 3))
                pygame.draw.polygon(screen, SILVER, [
                    (base_x - sword_length, base_y - 1),
                    (base_x - sword_length - 4, base_y + 1),
                    (base_x - sword_length, base_y + 2)
                ])
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (base_x - sword_length, base_y), 1)
            
            pygame.draw.rect(screen, DARK_SILVER, (base_x, base_y - 2, 3, 5))
            pygame.draw.rect(screen, GOLD, (base_x + 2, base_y, 2, 1))

class Room:
    def __init__(self, name, platforms, items=None, enemies=None, elite_enemies=None, gates=None, boss=None):
        self.name = name
        self.platforms = platforms
        self.items = items if items else []
        self.enemies = enemies if enemies else []
        self.elite_enemies = elite_enemies if elite_enemies else []
        self.gates = gates if gates else []
        self.boss = boss
        
class Item:
    def __init__(self, x, y, item_type, color):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.item_type = item_type
        self.color = color
        self.collected = False
        self.glow = 0
        
    def update(self):
        self.glow = (self.glow + 0.1) % (2 * math.pi)
        
    def draw(self, screen):
        if not self.collected:
            glow_offset = int(math.sin(self.glow) * 4)
            for i in range(3):
                alpha_color = (self.color[0] // (i+1), self.color[1] // (i+1), self.color[2] // (i+1))
                pygame.draw.rect(screen, alpha_color, 
                               (self.x - i*2, self.y + glow_offset - i*2, 
                                self.width + i*4, self.height + i*4), 2)
            
            pygame.draw.rect(screen, self.color, 
                           (self.x, self.y + glow_offset, self.width, self.height))
            pygame.draw.rect(screen, GOLD, 
                           (self.x + 2, self.y + glow_offset + 2, self.width - 4, self.height - 4), 2)
            
            pygame.draw.circle(screen, YELLOW, 
                             (int(self.x + 15), int(self.y + 15 + glow_offset)), 6)
            pygame.draw.circle(screen, WHITE, 
                             (int(self.x + 15), int(self.y + 15 + glow_offset)), 3)

class Enemy:
    def __init__(self, x, y, move_range):
        self.x = x
        self.y = y
        self.start_x = x
        self.width = 30
        self.height = 35
        self.speed = 2
        self.move_range = move_range
        self.direction = 1
        self.health = 2
        self.hit_flash = 0
        
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
        if self.hit_flash > 0 and (self.hit_flash // 2) % 2 == 0:
            color = WHITE
            visor_color = WHITE
        else:
            color = BLACK
            visor_color = RED
        
        pygame.draw.rect(screen, DARK_GRAY, (self.x + 5, self.y + 12, 20, 18))
        pygame.draw.rect(screen, color, (self.x + 7, self.y + 14, 16, 14))
        pygame.draw.line(screen, GRAY, (self.x + 15, self.y + 12), (self.x + 15, self.y + 30), 2)
        
        pygame.draw.ellipse(screen, color, (self.x + 7, self.y + 3, 16, 16))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + 9, self.y + 5, 12, 12))
        
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 7, self.y + 6),
            (self.x + 4, self.y),
            (self.x + 9, self.y + 4)
        ])
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 23, self.y + 6),
            (self.x + 26, self.y),
            (self.x + 21, self.y + 4)
        ])
        
        pygame.draw.rect(screen, visor_color, (self.x + 10, self.y + 9, 10, 4))
        if self.hit_flash == 0:
            pygame.draw.rect(screen, ORANGE, (self.x + 11, self.y + 10, 8, 2))
        
        pygame.draw.rect(screen, color, (self.x + 8, self.y + 30, 6, 5))
        pygame.draw.rect(screen, color, (self.x + 16, self.y + 30, 6, 5))
        
        if self.direction > 0:
            pygame.draw.rect(screen, DARK_GRAY, (self.x + 25, self.y + 18, 10, 3))
            pygame.draw.rect(screen, BLACK, (self.x + 24, self.y + 17, 2, 5))
        else:
            pygame.draw.rect(screen, DARK_GRAY, (self.x - 5, self.y + 18, 10, 3))
            pygame.draw.rect(screen, BLACK, (self.x + 4, self.y + 17, 2, 5))

class EliteKnight:
    """Bigger, badder black knight that can JUMP!"""
    def __init__(self, x, y, move_range, player):
        self.x = x
        self.y = y
        self.start_x = x
        self.width = 40  # BIGGER!
        self.height = 50
        self.speed = 1.5
        self.move_range = move_range
        self.direction = 1
        self.health = 5  # Takes 5 hits!
        self.max_health = 5
        self.hit_flash = 0
        self.player = player
        self.jump_cooldown = 0
        self.vel_y = 0
        self.gravity = 0.6
        self.on_ground = True
        
    def update(self, platforms):
        # Apply gravity
        self.vel_y += self.gravity
        self.y += self.vel_y
        
        # Check ground collision
        self.on_ground = False
        knight_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if knight_rect.colliderect(platform):
                if self.vel_y > 0:
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
        
        # Move toward player
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
        
        # Face player
        if self.player.x > self.x:
            self.direction = 1
        else:
            self.direction = -1
        
        # Jump attack!
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        elif self.on_ground and abs(self.player.x - self.x) < 200:
            # Jump toward player!
            self.vel_y = -10
            self.jump_cooldown = 120  # 2 seconds between jumps
        
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 10
        return self.health <= 0
    
    def draw(self, screen):
        if self.hit_flash > 0 and (self.hit_flash // 2) % 2 == 0:
            color = WHITE
            visor_color = WHITE
        else:
            color = BLACK
            visor_color = CRIMSON  # Darker red!
        
        # BIGGER body
        pygame.draw.rect(screen, DARK_GRAY, (self.x + 7, self.y + 18, 26, 24))
        pygame.draw.rect(screen, color, (self.x + 9, self.y + 20, 22, 20))
        pygame.draw.line(screen, GRAY, (self.x + 20, self.y + 18), (self.x + 20, self.y + 42), 3)
        
        # BIGGER helmet
        pygame.draw.ellipse(screen, color, (self.x + 10, self.y + 5, 20, 20))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + 12, self.y + 7, 16, 16))
        
        # BIGGER horns
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 10, self.y + 8),
            (self.x + 5, self.y),
            (self.x + 13, self.y + 5)
        ])
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 30, self.y + 8),
            (self.x + 35, self.y),
            (self.x + 27, self.y + 5)
        ])
        
        # Glowing visor
        pygame.draw.rect(screen, visor_color, (self.x + 13, self.y + 13, 14, 5))
        if self.hit_flash == 0:
            pygame.draw.rect(screen, ORANGE, (self.x + 14, self.y + 14, 12, 3))
        
        # BIGGER legs
        pygame.draw.rect(screen, color, (self.x + 10, self.y + 42, 8, 8))
        pygame.draw.rect(screen, color, (self.x + 22, self.y + 42, 8, 8))
        
        # BIGGER sword
        if self.direction > 0:
            pygame.draw.rect(screen, DARK_GRAY, (self.x + 33, self.y + 25, 15, 4))
            pygame.draw.rect(screen, BLACK, (self.x + 32, self.y + 23, 3, 8))
        else:
            pygame.draw.rect(screen, DARK_GRAY, (self.x - 8, self.y + 25, 15, 4))
            pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 23, 3, 8))
        
        # Health bar above head
        bar_width = 40
        bar_height = 4
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x, self.y - 8, bar_width, bar_height))
        pygame.draw.rect(screen, RED, (self.x, self.y - 8, bar_width * health_percent, bar_height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y - 8, bar_width, bar_height), 1)

class Shockwave:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 6
        self.width = 30
        self.height = 20
        self.lifetime = 120
        
    def update(self):
        self.x += self.speed * self.direction
        self.lifetime -= 1
        
    def is_alive(self):
        return self.lifetime > 0 and 0 < self.x < SCREEN_WIDTH
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)
    
    def draw(self, screen):
        offset = (120 - self.lifetime) % 10
        pygame.draw.line(screen, ORANGE, (self.x, self.y), (self.x + self.width, self.y), 4)
        pygame.draw.line(screen, YELLOW, (self.x, self.y), (self.x + self.width, self.y), 2)
        for i in range(3):
            wave_y = self.y - 5 - i * 5 - offset
            if wave_y > self.y - 20:
                alpha = 1 - (i / 3)
                color = (int(255 * alpha), int(140 * alpha), 0)
                pygame.draw.arc(screen, color, 
                              (self.x, wave_y, self.width, 10), 
                              0, math.pi, 3)

class Dragon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 80
        self.health = 15  # MORE HEALTH!
        self.max_health = 15
        self.direction = 1
        self.move_speed = 1.5
        self.start_x = x
        self.move_range = 150
        self.fire_cooldown = 0
        self.shockwave_cooldown = 0
        self.fireballs = []
        self.shockwaves = []
        self.wing_flap = 0
        self.hit_flash = 0
        self.ground_y = 550
        self.slamming = False  # NEW! Slam animation state
        self.slam_timer = 0
        self.slam_y_offset = 0
        
    def update(self):
        self.wing_flap = (self.wing_flap + 0.15) % (2 * math.pi)
        
        # Slam animation
        if self.slamming:
            self.slam_timer -= 1
            if self.slam_timer > 15:
                # Rising up
                self.slam_y_offset = -20
            elif self.slam_timer > 0:
                # Slamming down!
                self.slam_y_offset = int((15 - self.slam_timer) * 2)
            else:
                # Impact!
                self.slam_y_offset = 0
                self.slamming = False
                # Create shockwaves NOW!
                self.shockwaves.append(Shockwave(self.x + 50, self.ground_y, 1))
                self.shockwaves.append(Shockwave(self.x + 50, self.ground_y, -1))
        else:
            # Normal movement
            self.x += self.move_speed * self.direction
            if abs(self.x - self.start_x) > self.move_range:
                self.direction *= -1
        
        # Fire cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        else:
            self.fireballs.append(Fireball(self.x + 50, self.y + 40 + self.slam_y_offset, self.direction))
            self.fire_cooldown = 90
        
        # Shockwave cooldown
        if self.shockwave_cooldown > 0:
            self.shockwave_cooldown -= 1
        elif not self.slamming:
            # Start slam animation!
            self.slamming = True
            self.slam_timer = 30
            self.shockwave_cooldown = 180  # 3 seconds
        
        # Update projectiles
        for fireball in self.fireballs[:]:
            fireball.update()
            if fireball.x < -20 or fireball.x > SCREEN_WIDTH + 20:
                self.fireballs.remove(fireball)
        
        for shockwave in self.shockwaves[:]:
            shockwave.update()
            if not shockwave.is_alive():
                self.shockwaves.remove(shockwave)
        
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 15
        
    def is_alive(self):
        return self.health > 0
    
    def draw(self, screen):
        if self.hit_flash > 0 and (self.hit_flash // 3) % 2 == 0:
            body_color = WHITE
            accent_color = WHITE
        else:
            body_color = DARK_RED
            accent_color = RED
        
        # Apply slam offset to all drawing
        y = self.y + self.slam_y_offset
        
        wing_offset = int(math.sin(self.wing_flap) * 15)
        
        # Wings
        pygame.draw.polygon(screen, body_color, [
            (self.x + 30, y + 30),
            (self.x - 10, y + wing_offset),
            (self.x + 20, y + 40)
        ])
        pygame.draw.polygon(screen, accent_color, [
            (self.x + 25, y + 32),
            (self.x, y + 10 + wing_offset),
            (self.x + 20, y + 38)
        ])
        pygame.draw.polygon(screen, body_color, [
            (self.x + 60, y + 30),
            (self.x + 100, y + wing_offset),
            (self.x + 70, y + 40)
        ])
        pygame.draw.polygon(screen, accent_color, [
            (self.x + 65, y + 32),
            (self.x + 90, y + 10 + wing_offset),
            (self.x + 70, y + 38)
        ])
        
        # Tail
        tail_segments = [
            (self.x, y + 50),
            (self.x - 15, y + 48),
            (self.x - 25, y + 52),
            (self.x - 30, y + 50)
        ]
        for i in range(len(tail_segments) - 1):
            pygame.draw.line(screen, body_color, tail_segments[i], tail_segments[i+1], 8)
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x - 10, y + 46),
            (self.x - 8, y + 40),
            (self.x - 6, y + 46)
        ])
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x - 20, y + 50),
            (self.x - 18, y + 44),
            (self.x - 16, y + 50)
        ])
        
        # Body
        pygame.draw.ellipse(screen, body_color, (self.x + 10, y + 30, 70, 45))
        pygame.draw.ellipse(screen, accent_color, (self.x + 15, y + 35, 60, 35))
        
        for i in range(4):
            pygame.draw.arc(screen, CRIMSON, 
                          (self.x + 20 + i*12, y + 45, 15, 15), 
                          0, math.pi, 2)
        
        # Neck & Head
        pygame.draw.ellipse(screen, body_color, (self.x + 60, y + 20, 25, 35))
        pygame.draw.ellipse(screen, accent_color, (self.x + 62, y + 22, 21, 31))
        
        pygame.draw.ellipse(screen, body_color, (self.x + 75, y + 15, 30, 30))
        pygame.draw.ellipse(screen, accent_color, (self.x + 77, y + 17, 26, 26))
        
        pygame.draw.ellipse(screen, body_color, (self.x + 95, y + 25, 15, 15))
        
        pygame.draw.circle(screen, BLACK, (int(self.x + 98), int(y + 30)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 102), int(y + 32)), 2)
        
        pygame.draw.ellipse(screen, YELLOW, (self.x + 80, y + 22, 12, 10))
        pygame.draw.ellipse(screen, ORANGE, (self.x + 82, y + 24, 8, 6))
        pygame.draw.ellipse(screen, BLACK, (self.x + 85, y + 25, 3, 5))
        
        # Horns
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 78, y + 15),
            (self.x + 75, y + 5),
            (self.x + 82, y + 12)
        ])
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 92, y + 15),
            (self.x + 95, y + 5),
            (self.x + 88, y + 12)
        ])
        pygame.draw.polygon(screen, GRAY, [
            (self.x + 77, y + 15),
            (self.x + 76, y + 7),
            (self.x + 81, y + 13)
        ])
        pygame.draw.polygon(screen, GRAY, [
            (self.x + 91, y + 15),
            (self.x + 94, y + 7),
            (self.x + 89, y + 13)
        ])
        
        # Spikes
        for i in range(5):
            spike_x = self.x + 25 + i * 12
            pygame.draw.polygon(screen, DARK_GRAY, [
                (spike_x, y + 30),
                (spike_x + 3, y + 20),
                (spike_x + 6, y + 30)
            ])
        
        # Legs
        pygame.draw.ellipse(screen, body_color, (self.x + 25, y + 68, 15, 10))
        pygame.draw.ellipse(screen, body_color, (self.x + 55, y + 68, 15, 10))
        for leg_x in [self.x + 25, self.x + 55]:
            for claw_offset in [0, 5, 10]:
                pygame.draw.polygon(screen, BLACK, [
                    (leg_x + claw_offset, y + 75),
                    (leg_x + claw_offset + 2, y + 80),
                    (leg_x + claw_offset + 4, y + 75)
                ])
        
        # Health bar
        bar_width = 100
        bar_height = 10
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x, self.y - 20, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, DARK_RED, (self.x + 2, self.y - 18, bar_width, bar_height))
        pygame.draw.rect(screen, RED, (self.x + 2, self.y - 18, bar_width * health_percent, bar_height))
        pygame.draw.rect(screen, WHITE, (self.x + 2, self.y - 18, bar_width * health_percent, 2))
        pygame.draw.rect(screen, GOLD, (self.x, self.y - 20, bar_width + 4, bar_height + 4), 2)
        
        # Draw projectiles
        for fireball in self.fireballs:
            fireball.draw(screen)
        
        for shockwave in self.shockwaves:
            shockwave.draw(screen)

class Fireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 6
        self.radius = 10
        self.trail = []
        
    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
        self.x += self.speed * self.direction
        
    def draw(self, screen):
        for i, (tx, ty) in enumerate(self.trail):
            trail_radius = self.radius * (i / len(self.trail))
            pygame.draw.circle(screen, ORANGE, (int(tx), int(ty)), int(trail_radius))
        
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius - 3)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 6)

def create_rooms(player):
    """Create the game world"""
    rooms = {}
    
    rooms['start'] = Room(
        'start',
        platforms=[
            pygame.Rect(0, 550, 400, 50),
            pygame.Rect(200, 450, 150, 20),
            pygame.Rect(450, 400, 150, 20),
            pygame.Rect(650, 350, 150, 20),
        ]
    )
    
    rooms['item'] = Room(
        'item',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 480, 100, 20),
            pygame.Rect(250, 410, 100, 20),
            pygame.Rect(400, 350, 150, 20),
        ],
        items=[
            Item(445, 310, 'double_jump', GREEN)
        ]
    )
    
    rooms['knights'] = Room(
        'knights',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 450, 150, 20),
            pygame.Rect(300, 350, 150, 20),
            pygame.Rect(500, 450, 150, 20),
        ],
        enemies=[
            Enemy(200, 515, 100),
            Enemy(400, 515, 80),
            Enemy(600, 515, 120),
        ],
    )
    
    # NEW ROOM: Elite Guard 1
    rooms['elite1'] = Room(
        'elite1',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(150, 450, 120, 20),
            pygame.Rect(400, 380, 120, 20),
            pygame.Rect(650, 450, 120, 20),
        ],
        elite_enemies=[
            EliteKnight(300, 500, 150, player),
        ]
    )
    
    # NEW ROOM: Elite Guard 2
    rooms['elite2'] = Room(
        'elite2',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 420, 100, 20),
            pygame.Rect(500, 420, 100, 20),
        ],
        elite_enemies=[
            EliteKnight(250, 500, 100, player),
            EliteKnight(550, 500, 100, player),
        ]
    )
    
    rooms['dragon'] = Room(
        'dragon',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 400, 100, 20),
            pygame.Rect(600, 400, 100, 20),
        ],
        boss=Dragon(300, 200)
    )
    
    return rooms

def draw_heart(screen, x, y, filled):
    """Draw a heart"""
    if filled:
        color = RED
        inner_color = CRIMSON
    else:
        color = DARK_GRAY
        inner_color = BLACK
    
    pygame.draw.circle(screen, color, (x, y), 5)
    pygame.draw.circle(screen, color, (x + 8, y), 5)
    pygame.draw.polygon(screen, color, [
        (x - 4, y + 2),
        (x + 4, y + 12),
        (x + 12, y + 2)
    ])
    pygame.draw.circle(screen, inner_color, (x + 1, y), 2)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Knight's Adventure 🧭⚔️🐉")
    clock = pygame.time.Clock()
    
    player = Player(100, 300)
    rooms = create_rooms(player)  # Pass player for elite knights
    current_room = 'start'
    
    message = "LEFT/RIGHT = Move | UP = Jump | X = Sword (slower now!)"
    message_timer = 240
    dragon_defeated = False
    game_over = False
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_x:
                    player.attack()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    player = Player(100, 300)
                    current_room = 'start'
                    rooms = create_rooms(player)
                    game_over = False
                    dragon_defeated = False
                    message = "LEFT/RIGHT = Move | UP = Jump | X = Attack!"
                    message_timer = 240
        
        if not game_over:
            keys = pygame.key.get_pressed()
            player.vel_x = 0
            if keys[pygame.K_LEFT]:
                player.vel_x = -player.speed
            if keys[pygame.K_RIGHT]:
                player.vel_x = player.speed
            
            room = rooms[current_room]
            player.update(room.platforms)
            
            if not player.is_alive():
                game_over = True
                message = "You have fallen! Press R to restart"
                message_timer = 9999
            
            for item in room.items:
                item.update()
            
            attack_rect = player.get_attack_rect()
            
            # Regular enemies
            for enemy in room.enemies[:]:
                enemy.update()
                
                if attack_rect:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    if attack_rect.colliderect(enemy_rect):
                        if enemy.take_damage():
                            room.enemies.remove(enemy)
                            message = "Black knight defeated!"
                            message_timer = 60
                
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                if player_rect.colliderect(enemy_rect):
                    if player.take_damage():
                        message = f"Hit! Health: {player.health}/{player.max_health}"
                        message_timer = 90
            
            # ELITE enemies
            for elite in room.elite_enemies[:]:
                elite.update(room.platforms)
                
                if attack_rect:
                    elite_rect = pygame.Rect(elite.x, elite.y, elite.width, elite.height)
                    if attack_rect.colliderect(elite_rect):
                        if elite.take_damage():
                            room.elite_enemies.remove(elite)
                            message = "ELITE KNIGHT DEFEATED!"
                            message_timer = 90
                        else:
                            message = f"Elite hit! {elite.health}/{elite.max_health} HP left"
                            message_timer = 60
                
                elite_rect = pygame.Rect(elite.x, elite.y, elite.width, elite.height)
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                if player_rect.colliderect(elite_rect):
                    if player.take_damage():
                        message = f"Elite attack! Health: {player.health}/{player.max_health}"
                        message_timer = 90
            
            # Boss
            if room.boss and room.boss.is_alive():
                room.boss.update()
                
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                
                for fireball in room.boss.fireballs[:]:
                    fireball_rect = pygame.Rect(fireball.x - fireball.radius, 
                                               fireball.y - fireball.radius,
                                               fireball.radius * 2, fireball.radius * 2)
                    if player_rect.colliderect(fireball_rect):
                        if player.take_damage():
                            message = f"Dragon fire! Health: {player.health}/{player.max_health}"
                            message_timer = 90
                        room.boss.fireballs.remove(fireball)
                
                for shockwave in room.boss.shockwaves:
                    if player_rect.colliderect(shockwave.get_rect()):
                        if not player.on_ground:
                            continue
                        if player.take_damage():
                            message = f"Shockwave! Jump to dodge! Health: {player.health}/{player.max_health}"
                            message_timer = 90
                
                if attack_rect:
                    boss_rect = pygame.Rect(room.boss.x + 20, room.boss.y + 20, 70, 50)
                    if attack_rect.colliderect(boss_rect):
                        room.boss.take_damage()
                        message = f"Dragon hit! {room.boss.health}/{room.boss.max_health} HP"
                        message_timer = 60
                        
                        if not room.boss.is_alive():
                            dragon_defeated = True
                            message = "🎉 YOU DEFEATED THE DRAGON! The kingdom is saved! 🎉"
                            message_timer = 9999
            
            # Item collection
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            for item in room.items:
                if not item.collected:
                    item_rect = pygame.Rect(item.x, item.y, item.width, item.height)
                    if player_rect.colliderect(item_rect):
                        item.collected = True
                        if item.item_type == 'double_jump':
                            player.has_double_jump = True
                            message = "DOUBLE JUMP unlocked! Press UP twice!"
                            message_timer = 180
            
            # Room transitions
            if current_room == 'start':
                if player.x >= SCREEN_WIDTH - player.width - 5:
                    current_room = 'item'
                    player.x = 10
                    message = "Treasure chamber..."
                    message_timer = 90
            elif current_room == 'item':
                if player.x <= 5:
                    current_room = 'start'
                    player.x = SCREEN_WIDTH - player.width - 10
                elif player.x >= SCREEN_WIDTH - player.width - 5:
                    if player.has_double_jump:
                        current_room = 'knights'
                        player.x = 10
                        message = "Black knights ahead!"
                        message_timer = 120
                    else:
                        player.x = SCREEN_WIDTH - player.width - 10
                        message = "You need a special ability..."
                        message_timer = 120
            elif current_room == 'knights':
                if player.x <= 5:
                    current_room = 'item'
                    player.x = SCREEN_WIDTH - player.width - 10
                elif player.x >= SCREEN_WIDTH - player.width - 5:
                    current_room = 'elite1'
                    player.x = 10
                    message = "ELITE KNIGHT! Watch out for jumps!"
                    message_timer = 150
            elif current_room == 'elite1':
                if player.x <= 5:
                    current_room = 'knights'
                    player.x = SCREEN_WIDTH - player.width - 10
                elif player.x >= SCREEN_WIDTH - player.width - 5:
                    current_room = 'elite2'
                    player.x = 10
                    message = "TWO Elite Knights! Be careful!"
                    message_timer = 150
            elif current_room == 'elite2':
                if player.x <= 5:
                    current_room = 'elite1'
                    player.x = SCREEN_WIDTH - player.width - 10
                elif player.x >= SCREEN_WIDTH - player.width - 5:
                    current_room = 'dragon'
                    player.x = 10
                    message = "THE DRAGON! Watch for ground slams!"
                    message_timer = 180
            elif current_room == 'dragon':
                if player.x <= 5 and not dragon_defeated:
                    current_room = 'elite2'
                    player.x = SCREEN_WIDTH - player.width - 10
        
        # Draw
        screen.fill(BLACK)
        
        for platform in room.platforms:
            pygame.draw.rect(screen, BROWN, platform)
            pygame.draw.rect(screen, DARK_BROWN, (platform.x, platform.y, platform.width, 5))
            pygame.draw.rect(screen, GRAY, platform, 2)
        
        for item in room.items:
            item.draw(screen)
        
        for enemy in room.enemies:
            enemy.draw(screen)
        
        for elite in room.elite_enemies:
            elite.draw(screen)
        
        if room.boss:
            room.boss.draw(screen)
        
        player.draw(screen)
        
        # UI
        for i in range(player.max_health):
            draw_heart(screen, 15 + i * 18, 15, i < player.health)
        
        pygame.draw.rect(screen, DARK_GRAY, (10, 35, 150, 25))
        pygame.draw.rect(screen, GOLD, (10, 35, 150, 25), 2)
        
        if player.has_double_jump:
            pygame.draw.rect(screen, GREEN, (10, 65, 140, 20))
            pygame.draw.rect(screen, WHITE, (12, 67, 136, 16))
            pygame.draw.rect(screen, GREEN, (15, 70, 130, 10))
            pygame.draw.rect(screen, GOLD, (10, 65, 140, 20), 2)
        
        if message_timer > 0:
            msg_width = min(600, len(message) * 8 + 20)
            msg_height = 50
            msg_x = SCREEN_WIDTH // 2 - msg_width // 2
            msg_y = 20
            
            pygame.draw.rect(screen, BLACK, (msg_x, msg_y, msg_width, msg_height))
            pygame.draw.rect(screen, DARK_GRAY, (msg_x + 2, msg_y + 2, msg_width - 4, msg_height - 4))
            pygame.draw.rect(screen, GOLD, (msg_x, msg_y, msg_width, msg_height), 3)
            pygame.draw.rect(screen, YELLOW, (msg_x + 3, msg_y + 3, msg_width - 6, msg_height - 6), 1)
            
            message_timer -= 1
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
