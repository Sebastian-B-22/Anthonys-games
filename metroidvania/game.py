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
        self.width = 20  # Slimmer!
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
        self.has_dash = False
        self.has_map = False
        self.coins = 0
        self.sword_level = 1
        self.dashing = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_speed = 15
        self.dash_duration = 10
        
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
        
        # Update timers
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.dash_timer > 0:
            self.dash_timer -= 1
        else:
            self.dashing = False
        
        # Update slash effects
        for effect in self.slash_effects[:]:
            effect.update()
            if not effect.is_alive():
                self.slash_effects.remove(effect)
        
        # Apply gravity (not while dashing)
        if not self.dashing:
            self.vel_y += self.gravity
        
        # Move horizontally
        if self.dashing:
            # Dash movement
            dash_vel = self.dash_speed if self.facing_right else -self.dash_speed
            self.x += dash_vel
        else:
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
                if self.vel_x > 0:  # Moving right
                    self.x = platform.left - self.width
                elif self.vel_x < 0:  # Moving left
                    self.x = platform.right
        
        # Move vertically
        self.y += self.vel_y
        
        # Check vertical collisions
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.can_double_jump = True
                elif self.vel_y < 0:  # Jumping up
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
            self.attack_cooldown = 30
            # Create slash effect
            sword_x = self.x + self.width + 15 if self.facing_right else self.x - 15
            self.slash_effects.append(SlashEffect(sword_x, self.y + 15, self.facing_right))
    

    def dash(self):
        if self.has_dash and self.dash_cooldown == 0 and not self.dashing:
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = 60  # 1 second cooldown
            self.invincible_timer = self.dash_duration  # Invincible while dashing!

    def get_attack_rect(self):
        if self.attacking:
            if self.facing_right:
                return pygame.Rect(self.x + self.width, self.y + 10, 35, 20)  # Longer reach!
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
        
        # Draw slash effects first (behind knight)
        for effect in self.slash_effects:
            effect.draw(screen)
        
        # Slim realistic knight - all silver with black visor
        
        # Legs (slim, realistic)
        pygame.draw.rect(screen, SILVER, (self.x + 5, self.y + 28, 4, 12))
        pygame.draw.rect(screen, SILVER, (self.x + 11, self.y + 28, 4, 12))
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 6, self.y + 29, 2, 10))
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 12, self.y + 29, 2, 10))
        
        # Body (slim torso)
        pygame.draw.rect(screen, SILVER, (self.x + 4, self.y + 12, 12, 16))
        pygame.draw.rect(screen, LIGHT_SILVER, (self.x + 5, self.y + 13, 10, 14))
        
        # Chest plate detail
        pygame.draw.line(screen, DARK_SILVER, (self.x + 10, self.y + 12), (self.x + 10, self.y + 28), 1)
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 6, self.y + 16, 8, 1))
        pygame.draw.rect(screen, DARK_SILVER, (self.x + 6, self.y + 20, 8, 1))
        
        # Shoulders
        pygame.draw.circle(screen, SILVER, (int(self.x + 3), int(self.y + 13)), 3)
        pygame.draw.circle(screen, SILVER, (int(self.x + 17), int(self.y + 13)), 3)
        pygame.draw.circle(screen, LIGHT_SILVER, (int(self.x + 3), int(self.y + 13)), 2)
        pygame.draw.circle(screen, LIGHT_SILVER, (int(self.x + 17), int(self.y + 13)), 2)
        
        # Arms (slim)
        if self.attacking:
            # Extended arm when attacking
            if self.facing_right:
                pygame.draw.rect(screen, SILVER, (self.x + 16, self.y + 15, 8, 3))
                pygame.draw.circle(screen, SILVER, (int(self.x + 24), int(self.y + 16)), 2)
            else:
                pygame.draw.rect(screen, SILVER, (self.x - 4, self.y + 15, 8, 3))
                pygame.draw.circle(screen, SILVER, (int(self.x - 4), int(self.y + 16)), 2)
        else:
            pygame.draw.rect(screen, SILVER, (self.x + 2, self.y + 16, 3, 8))
            pygame.draw.rect(screen, SILVER, (self.x + 15, self.y + 16, 3, 8))
        
        # Helmet (realistic proportions)
        pygame.draw.ellipse(screen, SILVER, (self.x + 5, self.y + 2, 10, 12))
        pygame.draw.ellipse(screen, LIGHT_SILVER, (self.x + 6, self.y + 3, 8, 10))
        
        # Black visor (horizontal slit - mysterious!)
        pygame.draw.rect(screen, BLACK, (self.x + 6, self.y + 7, 8, 3))
        
        # Helmet top ridge
        pygame.draw.rect(screen, LIGHT_SILVER, (self.x + 8, self.y + 2, 4, 2))
        
        # Long sword with swing animation
        sword_angle = 0
        sword_length = 18  # LONGER SWORD!
        
        if self.attacking:
            sword_angle = -(self.attack_timer / 15) * 60  # Swing animation
        
        if self.facing_right:
            # Sword position
            base_x = self.x + self.width + 2
            base_y = self.y + 15
            
            if self.attacking:
                # Animated swing
                angle_rad = math.radians(sword_angle)
                end_x = base_x + math.cos(angle_rad) * sword_length
                end_y = base_y + math.sin(angle_rad) * sword_length
                
                # Blade (glowing when swinging)
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (end_x, end_y), 4)
                pygame.draw.line(screen, WHITE, (base_x, base_y), (end_x, end_y), 2)
                
                # Sword tip
                pygame.draw.circle(screen, CYAN, (int(end_x), int(end_y)), 3)
            else:
                # Blade at rest
                pygame.draw.rect(screen, SILVER, (base_x, base_y - 1, sword_length, 3))
                pygame.draw.polygon(screen, SILVER, [
                    (base_x + sword_length, base_y - 1),
                    (base_x + sword_length + 4, base_y + 1),
                    (base_x + sword_length, base_y + 2)
                ])
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (base_x + sword_length, base_y), 1)
            
            # Hilt
            pygame.draw.rect(screen, DARK_SILVER, (base_x - 3, base_y - 2, 3, 5))
            pygame.draw.rect(screen, GOLD, (base_x - 4, base_y, 2, 1))
        else:
            # Left-facing sword
            base_x = self.x - 2
            base_y = self.y + 15
            
            if self.attacking:
                # Animated swing
                angle_rad = math.radians(180 - sword_angle)
                end_x = base_x + math.cos(angle_rad) * sword_length
                end_y = base_y + math.sin(angle_rad) * sword_length
                
                # Blade (glowing when swinging)
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (end_x, end_y), 4)
                pygame.draw.line(screen, WHITE, (base_x, base_y), (end_x, end_y), 2)
                
                # Sword tip
                pygame.draw.circle(screen, CYAN, (int(end_x), int(end_y)), 3)
            else:
                # Blade at rest
                pygame.draw.rect(screen, SILVER, (base_x - sword_length, base_y - 1, sword_length, 3))
                pygame.draw.polygon(screen, SILVER, [
                    (base_x - sword_length, base_y - 1),
                    (base_x - sword_length - 4, base_y + 1),
                    (base_x - sword_length, base_y + 2)
                ])
                pygame.draw.line(screen, LIGHT_SILVER, (base_x, base_y), (base_x - sword_length, base_y), 1)
            
            # Hilt
            pygame.draw.rect(screen, DARK_SILVER, (base_x, base_y - 2, 3, 5))
            pygame.draw.rect(screen, GOLD, (base_x + 2, base_y, 2, 1))

class Room:
    def __init__(self, name, platforms, items=None, enemies=None, elite_enemies=None, gates=None, boss=None, bench=None, skeletons=None, skeleton_boss=None, npc=None, treasure=None, shopkeeper=None, flying_enemies=None, rolling_enemies=None, crystals=None):
        self.name = name
        self.platforms = platforms
        self.items = items if items else []
        self.enemies = enemies if enemies else []
        self.elite_enemies = elite_enemies if elite_enemies else []
        self.gates = gates if gates else []
        self.boss = boss
        self.bench = bench
        self.skeletons = skeletons if skeletons else []
        self.skeleton_boss = skeleton_boss
        self.npc = npc
        self.treasure = treasure
        self.shopkeeper = shopkeeper
        self.flying_enemies = flying_enemies if flying_enemies else []
        self.rolling_enemies = rolling_enemies if rolling_enemies else []
        self.crystals = crystals if crystals else []
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
            # Glowing aura
            for i in range(3):
                alpha_color = (self.color[0] // (i+1), self.color[1] // (i+1), self.color[2] // (i+1))
                pygame.draw.rect(screen, alpha_color, 
                               (self.x - i*2, self.y + glow_offset - i*2, 
                                self.width + i*4, self.height + i*4), 2)
            
            # Item box
            pygame.draw.rect(screen, self.color, 
                           (self.x, self.y + glow_offset, self.width, self.height))
            pygame.draw.rect(screen, GOLD, 
                           (self.x + 2, self.y + glow_offset + 2, self.width - 4, self.height - 4), 2)
            
            # Star effect
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
        # Flash white when hit
        if self.hit_flash > 0 and (self.hit_flash // 2) % 2 == 0:
            color = WHITE
            visor_color = WHITE
        else:
            color = BLACK
            visor_color = RED
        
        # Black knight body
        pygame.draw.rect(screen, DARK_GRAY, (self.x + 5, self.y + 12, 20, 18))
        pygame.draw.rect(screen, color, (self.x + 7, self.y + 14, 16, 14))
        
        # Armor plates
        pygame.draw.line(screen, GRAY, (self.x + 15, self.y + 12), (self.x + 15, self.y + 30), 2)
        
        # Helmet
        pygame.draw.ellipse(screen, color, (self.x + 7, self.y + 3, 16, 16))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + 9, self.y + 5, 12, 12))
        
        # Horns
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
        
        # Visor
        pygame.draw.rect(screen, visor_color, (self.x + 10, self.y + 9, 10, 4))
        if self.hit_flash == 0:
            pygame.draw.rect(screen, ORANGE, (self.x + 11, self.y + 10, 8, 2))
        
        # Legs
        pygame.draw.rect(screen, color, (self.x + 8, self.y + 30, 6, 5))
        pygame.draw.rect(screen, color, (self.x + 16, self.y + 30, 6, 5))
        
        # Sword
        if self.direction > 0:
            pygame.draw.rect(screen, DARK_GRAY, (self.x + 25, self.y + 18, 10, 3))
            pygame.draw.rect(screen, BLACK, (self.x + 24, self.y + 17, 2, 5))
        else:
            pygame.draw.rect(screen, DARK_GRAY, (self.x - 5, self.y + 18, 10, 3))
            pygame.draw.rect(screen, BLACK, (self.x + 4, self.y + 17, 2, 5))

class Shockwave:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.speed = 6
        self.width = 30
        self.height = 20
        self.lifetime = 120  # 2 seconds
        
    def update(self):
        self.x += self.speed * self.direction
        self.lifetime -= 1
        
    def is_alive(self):
        return self.lifetime > 0 and 0 < self.x < SCREEN_WIDTH
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)
    
    def draw(self, screen):
        # Animated shockwave effect
        offset = (120 - self.lifetime) % 10
        # Ground crack effect
        pygame.draw.line(screen, ORANGE, (self.x, self.y), (self.x + self.width, self.y), 4)
        pygame.draw.line(screen, YELLOW, (self.x, self.y), (self.x + self.width, self.y), 2)
        # Energy waves
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
        self.health = 10
        self.max_health = 10
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
        self.ground_y = 550  # Ground level for shockwave
        
    def update(self):
        # Wing animation
        self.wing_flap = (self.wing_flap + 0.15) % (2 * math.pi)
        
        # Move back and forth
        self.x += self.move_speed * self.direction
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
        
        # Fire cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        else:
            # Shoot fireball
            self.fireballs.append(Fireball(self.x + 50, self.y + 40, self.direction))
            self.fire_cooldown = 90
        
        # Shockwave cooldown
        if self.shockwave_cooldown > 0:
            self.shockwave_cooldown -= 1
        else:
            # Create shockwaves in both directions!
            self.shockwaves.append(Shockwave(self.x + 50, self.ground_y, 1))
            self.shockwaves.append(Shockwave(self.x + 50, self.ground_y, -1))
            self.shockwave_cooldown = 150  # 2.5 seconds
        
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
        # Flash when hit
        if self.hit_flash > 0 and (self.hit_flash // 3) % 2 == 0:
            body_color = WHITE
            accent_color = WHITE
        else:
            body_color = DARK_RED
            accent_color = RED
        
        # Wing flap offset
        wing_offset = int(math.sin(self.wing_flap) * 15)
        
        # Wings
        pygame.draw.polygon(screen, body_color, [
            (self.x + 30, self.y + 30),
            (self.x - 10, self.y + wing_offset),
            (self.x + 20, self.y + 40)
        ])
        pygame.draw.polygon(screen, accent_color, [
            (self.x + 25, self.y + 32),
            (self.x, self.y + 10 + wing_offset),
            (self.x + 20, self.y + 38)
        ])
        pygame.draw.polygon(screen, body_color, [
            (self.x + 60, self.y + 30),
            (self.x + 100, self.y + wing_offset),
            (self.x + 70, self.y + 40)
        ])
        pygame.draw.polygon(screen, accent_color, [
            (self.x + 65, self.y + 32),
            (self.x + 90, self.y + 10 + wing_offset),
            (self.x + 70, self.y + 38)
        ])
        
        # Tail
        tail_segments = [
            (self.x, self.y + 50),
            (self.x - 15, self.y + 48),
            (self.x - 25, self.y + 52),
            (self.x - 30, self.y + 50)
        ]
        for i in range(len(tail_segments) - 1):
            pygame.draw.line(screen, body_color, tail_segments[i], tail_segments[i+1], 8)
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x - 10, self.y + 46),
            (self.x - 8, self.y + 40),
            (self.x - 6, self.y + 46)
        ])
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x - 20, self.y + 50),
            (self.x - 18, self.y + 44),
            (self.x - 16, self.y + 50)
        ])
        
        # Body
        pygame.draw.ellipse(screen, body_color, (self.x + 10, self.y + 30, 70, 45))
        pygame.draw.ellipse(screen, accent_color, (self.x + 15, self.y + 35, 60, 35))
        
        # Belly scales
        for i in range(4):
            pygame.draw.arc(screen, CRIMSON, 
                          (self.x + 20 + i*12, self.y + 45, 15, 15), 
                          0, math.pi, 2)
        
        # Neck
        pygame.draw.ellipse(screen, body_color, (self.x + 60, self.y + 20, 25, 35))
        pygame.draw.ellipse(screen, accent_color, (self.x + 62, self.y + 22, 21, 31))
        
        # Head
        pygame.draw.ellipse(screen, body_color, (self.x + 75, self.y + 15, 30, 30))
        pygame.draw.ellipse(screen, accent_color, (self.x + 77, self.y + 17, 26, 26))
        
        # Snout
        pygame.draw.ellipse(screen, body_color, (self.x + 95, self.y + 25, 15, 15))
        
        # Nostrils
        pygame.draw.circle(screen, BLACK, (int(self.x + 98), int(self.y + 30)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 102), int(self.y + 32)), 2)
        
        # Eye
        pygame.draw.ellipse(screen, YELLOW, (self.x + 80, self.y + 22, 12, 10))
        pygame.draw.ellipse(screen, ORANGE, (self.x + 82, self.y + 24, 8, 6))
        pygame.draw.ellipse(screen, BLACK, (self.x + 85, self.y + 25, 3, 5))
        
        # Horns
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 78, self.y + 15),
            (self.x + 75, self.y + 5),
            (self.x + 82, self.y + 12)
        ])
        pygame.draw.polygon(screen, DARK_GRAY, [
            (self.x + 92, self.y + 15),
            (self.x + 95, self.y + 5),
            (self.x + 88, self.y + 12)
        ])
        pygame.draw.polygon(screen, GRAY, [
            (self.x + 77, self.y + 15),
            (self.x + 76, self.y + 7),
            (self.x + 81, self.y + 13)
        ])
        pygame.draw.polygon(screen, GRAY, [
            (self.x + 91, self.y + 15),
            (self.x + 94, self.y + 7),
            (self.x + 89, self.y + 13)
        ])
        
        # Spikes
        for i in range(5):
            spike_x = self.x + 25 + i * 12
            pygame.draw.polygon(screen, DARK_GRAY, [
                (spike_x, self.y + 30),
                (spike_x + 3, self.y + 20),
                (spike_x + 6, self.y + 30)
            ])
        
        # Legs/claws
        pygame.draw.ellipse(screen, body_color, (self.x + 25, self.y + 68, 15, 10))
        pygame.draw.ellipse(screen, body_color, (self.x + 55, self.y + 68, 15, 10))
        for leg_x in [self.x + 25, self.x + 55]:
            for claw_offset in [0, 5, 10]:
                pygame.draw.polygon(screen, BLACK, [
                    (leg_x + claw_offset, self.y + 75),
                    (leg_x + claw_offset + 2, self.y + 80),
                    (leg_x + claw_offset + 4, self.y + 75)
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
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            trail_radius = self.radius * (i / len(self.trail))
            pygame.draw.circle(screen, ORANGE, (int(tx), int(ty)), int(trail_radius))
        
        # Draw fireball
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius - 3)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 6)



class NPC:
    """A friendly NPC character"""
    def __init__(self, x, y, dialogue):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.dialogue = dialogue
        self.dialogue_shown = False
    
    def draw(self, screen):
        # Draw a simple hooded figure (like Cornifer!)
        # Body (brown cloak)
        pygame.draw.ellipse(screen, BROWN, (self.x+5, self.y+15, 20, 25))
        
        # Hood
        pygame.draw.ellipse(screen, DARK_BROWN, (self.x+7, self.y+5, 16, 18))
        pygame.draw.circle(screen, DARK_BROWN, (int(self.x+15), int(self.y+8)), 9)
        
        # Face (friendly!)
        pygame.draw.circle(screen, (255, 220, 180), (int(self.x+15), int(self.y+15)), 6)
        
        # Eyes
        pygame.draw.circle(screen, BLACK, (int(self.x+12), int(self.y+14)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x+18), int(self.y+14)), 2)
        
        # Smile
        pygame.draw.arc(screen, BLACK, (self.x+10, self.y+15, 10, 6), 0, 3.14, 2)
        
        # Scroll/map in hand
        pygame.draw.rect(screen, (240, 230, 200), (self.x+20, self.y+20, 8, 10))
        pygame.draw.line(screen, BLACK, (self.x+21, self.y+22), (self.x+27, self.y+22), 1)
        pygame.draw.line(screen, BLACK, (self.x+21, self.y+25), (self.x+27, self.y+25), 1)



class TreasureChest:
    """A chest full of treasure!"""
    def __init__(self, x, y, coins):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.coins = coins
        self.opened = False
    
    def draw(self, screen):
        if not self.opened:
            # Closed chest
            pygame.draw.rect(screen, BROWN, (self.x, self.y+10, self.width, 20))
            pygame.draw.rect(screen, DARK_BROWN, (self.x+2, self.y+12, self.width-4, 16))
            # Lid
            pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, 12))
            pygame.draw.rect(screen, DARK_BROWN, (self.x+2, self.y+2, self.width-4, 8))
            # Lock
            pygame.draw.circle(screen, GOLD, (int(self.x+self.width//2), int(self.y+15)), 4)
            pygame.draw.circle(screen, BLACK, (int(self.x+self.width//2), int(self.y+15)), 2)
        else:
            # Opened chest
            pygame.draw.rect(screen, BROWN, (self.x, self.y+10, self.width, 20))
            pygame.draw.rect(screen, DARK_BROWN, (self.x+2, self.y+12, self.width-4, 16))
            # Lid (open)
            pygame.draw.rect(screen, BROWN, (self.x, self.y-5, self.width, 12))
            # Empty inside
            pygame.draw.rect(screen, BLACK, (self.x+5, self.y+15, self.width-10, 10))

class Shopkeeper:
    """Friendly merchant NPC"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 45
        self.items_for_sale = {
            'better_sword': {'cost': 50, 'bought': False, 'name': 'Better Sword'},
            'heart_container': {'cost': 100, 'bought': False, 'name': 'Heart Container'}
        }
    
    def draw(self, screen):
        # Merchant body (fancy outfit!)
        pygame.draw.ellipse(screen, PURPLE, (self.x+5, self.y+18, 25, 27))
        # Head
        pygame.draw.circle(screen, (255, 220, 180), (int(self.x+17), int(self.y+12)), 8)
        # Hat (merchant's hat)
        pygame.draw.polygon(screen, DARK_RED, [
            (self.x+10, self.y+5),
            (self.x+24, self.y+5),
            (self.x+17, self.y-3)
        ])
        pygame.draw.ellipse(screen, DARK_RED, (self.x+8, self.y+3, 18, 6))
        # Eyes (friendly)
        pygame.draw.circle(screen, BLACK, (int(self.x+13), int(self.y+11)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x+21), int(self.y+11)), 2)
        # Smile
        pygame.draw.arc(screen, BLACK, (self.x+12, self.y+13, 10, 6), 0, 3.14, 2)
        # Coin purse
        pygame.draw.circle(screen, GOLD, (int(self.x+28), int(self.y+30)), 5)
        pygame.draw.line(screen, BROWN, (self.x+28, self.y+25), (self.x+28, self.y+28), 2)


class Skeleton:
    """Spooky skeleton enemy"""
    def __init__(self, x, y, move_range):
        self.x, self.y, self.start_x = x, y, x
        self.width, self.height = 25, 40
        self.speed, self.move_range, self.direction = 2.5, move_range, 1
        self.health, self.hit_flash = 3, 0
    def update(self):
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) > self.move_range: self.direction *= -1
        if self.hit_flash > 0: self.hit_flash -= 1
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 10
        return self.health <= 0
    def draw(self, screen):
        c = WHITE if (self.hit_flash>0 and (self.hit_flash//2)%2==0) else (240,240,230)
        pygame.draw.circle(screen, c, (int(self.x+12), int(self.y+10)), 10)
        pygame.draw.circle(screen, BLACK, (int(self.x+8), int(self.y+8)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x+16), int(self.y+8)), 3)
        pygame.draw.circle(screen, GREEN, (int(self.x+8), int(self.y+8)), 2)
        pygame.draw.circle(screen, GREEN, (int(self.x+16), int(self.y+8)), 2)
        pygame.draw.polygon(screen, BLACK, [(self.x+11,self.y+12),(self.x+13,self.y+12),(self.x+12,self.y+15)])
        for tx in range(3): pygame.draw.rect(screen, BLACK, (self.x+8+tx*3, self.y+16, 2, 3))
        pygame.draw.rect(screen, c, (self.x+10, self.y+20, 4, 15))
        for ry in [22,26,30]: pygame.draw.line(screen, c, (self.x+7,self.y+ry), (self.x+17,self.y+ry), 2)
        pygame.draw.line(screen, c, (self.x+6,self.y+22), (self.x+2,self.y+30), 3)
        pygame.draw.line(screen, c, (self.x+18,self.y+22), (self.x+22,self.y+30), 3)
        pygame.draw.line(screen, c, (self.x+10,self.y+35), (self.x+8,self.y+40), 3)
        pygame.draw.line(screen, c, (self.x+14,self.y+35), (self.x+16,self.y+40), 3)

class BoneProjectile:
    def __init__(self, x, y, direction):
        self.x, self.y, self.direction, self.speed = x, y, direction, 5
    def update(self):
        self.x += self.speed * self.direction
    def draw(self, screen):
        pygame.draw.rect(screen, (240,240,230), (self.x-4, self.y-2, 8, 4))
        pygame.draw.circle(screen, (240,240,230), (int(self.x-4), int(self.y)), 3)
        pygame.draw.circle(screen, (240,240,230), (int(self.x+4), int(self.y)), 3)

class SkeletonBoss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.health = 20
        self.max_health = 20
        self.direction = 1
        self.move_speed = 2
        self.start_x = x
        self.move_range = 200
        self.attack_cooldown = 0
        self.bones = []
        self.hit_flash = 0
    
    def update(self):
        self.x += self.move_speed * self.direction
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.bones.append(BoneProjectile(self.x+30, self.y+30, self.direction))
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
        c = WHITE if (self.hit_flash>0 and (self.hit_flash//3)%2==0) else (240,240,230)
        pygame.draw.circle(screen, c, (int(self.x+30), int(self.y+20)), 20)
        pygame.draw.circle(screen, BLACK, (int(self.x+20), int(self.y+15)), 6)
        pygame.draw.circle(screen, BLACK, (int(self.x+40), int(self.y+15)), 6)
        pygame.draw.circle(screen, RED, (int(self.x+20), int(self.y+15)), 4)
        pygame.draw.circle(screen, RED, (int(self.x+40), int(self.y+15)), 4)
        pygame.draw.polygon(screen, BLACK, [(self.x+28,self.y+22),(self.x+32,self.y+22),(self.x+30,self.y+28)])
        for tx in range(6):
            pygame.draw.rect(screen, BLACK, (self.x+18+tx*4, self.y+32, 3, 5))
        pygame.draw.rect(screen, c, (self.x+26, self.y+40, 8, 30))
        for ry in [44,50,56,62]:
            pygame.draw.line(screen, c, (self.x+15,self.y+ry), (self.x+45,self.y+ry), 4)
        pygame.draw.line(screen, c, (self.x+12,self.y+45), (self.x,self.y+60), 5)
        pygame.draw.line(screen, c, (self.x+48,self.y+45), (self.x+60,self.y+60), 5)
        pygame.draw.line(screen, c, (self.x+22,self.y+70), (self.x+18,self.y+80), 5)
        pygame.draw.line(screen, c, (self.x+38,self.y+70), (self.x+42,self.y+80), 5)
        bw, bh = 60, 8
        hp = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x, self.y-15, bw, bh))
        pygame.draw.rect(screen, DARK_RED, (self.x, self.y-15, bw*hp, bh))
        pygame.draw.rect(screen, WHITE, (self.x, self.y-15, bw, bh), 1)
        for bone in self.bones:
            bone.draw(screen)


class FlyingEnemy:
    """Flying enemy like vengefly!"""
    def __init__(self, x, y, move_pattern="circle"):
        self.x, self.y = x, y
        self.start_x, self.start_y = x, y
        self.width, self.height = 25, 20
        self.speed, self.health, self.hit_flash = 2, 2, 0
        self.move_pattern, self.angle, self.direction = move_pattern, 0, 1
    
    def update(self):
        if self.move_pattern == "circle":
            self.angle += 0.05
            self.x = self.start_x + math.cos(self.angle) * 80
            self.y = self.start_y + math.sin(self.angle) * 60
        elif self.move_pattern == "hover":
            self.angle += 0.08
            self.y = self.start_y + math.sin(self.angle) * 40
            self.x += self.speed * self.direction
            if abs(self.x - self.start_x) > 100:
                self.direction *= -1
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 10
        return self.health <= 0
    
    def draw(self, screen):
        c = WHITE if (self.hit_flash>0 and (self.hit_flash//2)%2==0) else ORANGE
        pygame.draw.ellipse(screen, c, (int(self.x+5), int(self.y+5), 15, 10))
        pygame.draw.ellipse(screen, DARK_GOLD, (int(self.x+7), int(self.y+7), 11, 6))
        wo = int(abs(math.sin(self.angle * 10)) * 3)
        pygame.draw.ellipse(screen, (200,255,255), (int(self.x-5), int(self.y+3+wo), 12, 8))
        pygame.draw.ellipse(screen, (200,255,255), (int(self.x+18), int(self.y+3+wo), 12, 8))
        pygame.draw.circle(screen, RED, (int(self.x+10), int(self.y+9)), 2)
        pygame.draw.circle(screen, RED, (int(self.x+15), int(self.y+9)), 2)
        pygame.draw.polygon(screen, BLACK, [(int(self.x+12),int(self.y+15)),(int(self.x+10),int(self.y+18)),(int(self.x+14),int(self.y+18))])


class RollingEnemy:
    """Rock enemy that curls and rolls like baldur!"""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.start_x = x
        self.width, self.height = 30, 30
        self.speed = 4
        self.direction = 1
        self.health = 1  # One hit!
        self.rolling = True
        self.hit_flash = 0
    
    def update(self):
        # Roll back and forth
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) > 150:
            self.direction *= -1
        if self.hit_flash > 0:
            self.hit_flash -= 1
    
    def take_damage(self):
        self.health -= 1
        self.hit_flash = 10
        return self.health <= 0
    
    def draw(self, screen):
        c = WHITE if (self.hit_flash>0 and (self.hit_flash//2)%2==0) else GRAY
        # Curled up ball shape
        pygame.draw.circle(screen, c, (int(self.x+15), int(self.y+15)), 15)
        pygame.draw.circle(screen, DARK_GRAY, (int(self.x+15), int(self.y+15)), 12)
        # Segments (armored shell)
        for i in range(4):
            angle = (self.x / 10 + i * 1.57) % 6.28
            seg_x = int(self.x + 15 + math.cos(angle) * 8)
            seg_y = int(self.y + 15 + math.sin(angle) * 8)
            pygame.draw.circle(screen, c, (seg_x, seg_y), 4)

class Crystal:
    """Decorative crystal"""
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color
        self.glow = 0
    
    def update(self):
        self.glow = (self.glow + 0.05) % (2 * math.pi)
    
    def draw(self, screen):
        brightness = int(abs(math.sin(self.glow)) * 50)
        glow_color = tuple(min(255, c + brightness) for c in self.color)
        # Crystal shape
        pygame.draw.polygon(screen, glow_color, [
            (self.x + 10, self.y),
            (self.x + 15, self.y + 12),
            (self.x + 10, self.y + 25),
            (self.x + 5, self.y + 12)
        ])
        pygame.draw.polygon(screen, self.color, [
            (self.x + 10, self.y + 3),
            (self.x + 13, self.y + 12),
            (self.x + 10, self.y + 22),
            (self.x + 7, self.y + 12)
        ])


def create_rooms():
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
    
    rooms['dragon'] = Room(
        'dragon',
        platforms=[
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 400, 100, 20),
            pygame.Rect(600, 400, 100, 20),
        ],
        boss=Dragon(300, 200)
    )
    


    # Dash Ability Room
    rooms['dash_room'] = Room('dash_room',
        platforms=[
            pygame.Rect(0,550,800,50),
            pygame.Rect(300,400,200,20),
        ],
        items=[Item(360,360,'dash',CYAN)])

    # Obby Room
    rooms['obby'] = Room('obby', platforms=[
        pygame.Rect(0,550,150,50), pygame.Rect(200,480,80,20), pygame.Rect(350,420,80,20),
        pygame.Rect(500,360,80,20), pygame.Rect(350,300,80,20), pygame.Rect(200,240,80,20),
        pygame.Rect(400,180,120,20), pygame.Rect(650,180,150,20),
        pygame.Rect(750,300,50,20)])  # Hidden platform on right!
    

    # Cartographer's Room (hidden!)
    rooms['cartographer'] = Room('cartographer',
        platforms=[
            pygame.Rect(0,550,800,50),
            pygame.Rect(350,450,100,20),
        ],
        items=[Item(370,410,'map',PURPLE)],
        npc=NPC(300, 510, "Here's a map for your journey!"))

    # Skeleton Room
    rooms['skeletons'] = Room('skeletons',
        platforms=[pygame.Rect(0,550,800,50), pygame.Rect(150,450,120,20), pygame.Rect(500,450,120,20)],
        skeletons=[Skeleton(250,510,120), Skeleton(550,510,150)])
    
    # Skeleton Boss
    rooms['skeleton_boss'] = Room('skeleton_boss',
        platforms=[pygame.Rect(0,550,800,50), pygame.Rect(150,420,100,20), pygame.Rect(550,420,100,20)],
        skeleton_boss=SkeletonBoss(350,470))


    # Treasure Room
    rooms['treasure'] = Room('treasure',
        platforms=[
            pygame.Rect(0,550,800,50),
            pygame.Rect(350,480,100,20),
        ],
        treasure=TreasureChest(365, 445, 150))
    
    # Shop Room
    rooms['shop'] = Room('shop',
        platforms=[pygame.Rect(0,550,800,50)],
        shopkeeper=Shopkeeper(380, 505))


    # The Cliffs - vertical platforming with flying enemies!
    rooms['cliffs'] = Room('cliffs',
        platforms=[
            pygame.Rect(0,550,150,50),          # Bottom left
            pygame.Rect(200,480,100,20),        # Low platform
            pygame.Rect(100,400,100,20),        # Mid left
            pygame.Rect(300,350,100,20),        # Mid right
            pygame.Rect(150,280,100,20),        # Upper left
            pygame.Rect(400,250,100,20),        # Upper right
            pygame.Rect(250,180,120,20),        # High platform
            pygame.Rect(650,180,150,50),        # Top exit platform
        ],
        flying_enemies=[
            FlyingEnemy(250, 450, 'circle'),
            FlyingEnemy(350, 320, 'hover'),
            FlyingEnemy(300, 220, 'circle'),
        ])


    # Crystal Plains - peaceful area with rolling enemies
    rooms['crystal_plains'] = Room('crystal_plains',
        platforms=[
            pygame.Rect(0,550,800,50),
            pygame.Rect(150,480,120,20),
            pygame.Rect(450,480,120,20),
        ],
        rolling_enemies=[
            RollingEnemy(200, 520),
            RollingEnemy(500, 520),
            RollingEnemy(350, 450),
        ],
        crystals=[
            Crystal(100, 490, CYAN),
            Crystal(250, 520, PURPLE),
            Crystal(400, 520, CYAN),
            Crystal(550, 490, PURPLE),
            Crystal(680, 520, CYAN),
        ])

    return rooms


# Simple minimap
def draw_minimap(screen, rooms, current_room, player):
    """Draw a simple minimap in top right corner"""
    map_x, map_y = 600, 10
    room_size = 25
    
    # Define room positions on minimap
    room_positions = {
        'start': (0, 2),
        'item': (1, 2),
        'knights': (2, 2),
        'elite1': (3, 2),
        'elite2': (4, 2),
        'dragon': (5, 2),
        'heart_upgrade': (6, 2),
        'healing': (7, 2),
        'dash_room': (7, 1),
        'obby': (7, 3),
        'skeletons': (8, 3),
        'skeleton_boss': (9, 3),
    }
    
    # Draw map background
    pygame.draw.rect(screen, BLACK, (map_x-5, map_y-5, 260, 110))
    pygame.draw.rect(screen, GOLD, (map_x-5, map_y-5, 260, 110), 2)
    
    # Draw rooms
    for room_name, (grid_x, grid_y) in room_positions.items():
        rx = map_x + grid_x * room_size
        ry = map_y + grid_y * room_size
        
        if room_name == current_room:
            # Current room (bright)
            pygame.draw.rect(screen, YELLOW, (rx, ry, room_size-2, room_size-2))
        else:
            # Visited room (grey)
            pygame.draw.rect(screen, GRAY, (rx, ry, room_size-2, room_size-2))
        
        pygame.draw.rect(screen, WHITE, (rx, ry, room_size-2, room_size-2), 1)

def draw_heart(screen, x, y, filled):
    """Draw a heart for health"""
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
    rooms = create_rooms()
    current_room = 'start'
    
    message = "LEFT/RIGHT = Move | UP = Jump | X = Sword Attack!"
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
                elif event.key == pygame.K_d:
                    player.dash()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    player = Player(100, 300)
                    current_room = 'start'
                    rooms = create_rooms()
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
            # Obby fall check
            if current_room == 'obby' and player.y > 560:
                player.x, player.y, player.vel_y = 50, 500, 0
                message, message_timer = "Fell! Try again!", 60

            
            if not player.is_alive():
                game_over = True
                message = "You have fallen! Press R to restart"
                message_timer = 9999
            
            for item in room.items:
                item.update()
            # Update crystals
            for crystal in room.crystals:
                crystal.update()

            

            # Shop interaction
            if room.shopkeeper and keys[pygame.K_x]:
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                shop_rect = pygame.Rect(room.shopkeeper.x, room.shopkeeper.y, room.shopkeeper.width, room.shopkeeper.height)
                if player_rect.colliderect(shop_rect):
                    # Try to buy items
                    if not room.shopkeeper.items_for_sale['better_sword']['bought']:
                        cost = room.shopkeeper.items_for_sale['better_sword']['cost']
                        if player.coins >= cost:
                            player.coins -= cost
                            player.sword_level = 2
                            room.shopkeeper.items_for_sale['better_sword']['bought'] = True
                            message = f"Bought Better Sword! (50 coins) Coins: {player.coins}"
                            message_timer = 150
                        else:
                            message = f"Better Sword costs 50 coins. You have {player.coins}"
                            message_timer = 120
                    elif not room.shopkeeper.items_for_sale['heart_container']['bought']:
                        cost = room.shopkeeper.items_for_sale['heart_container']['cost']
                        if player.coins >= cost:
                            player.coins -= cost
                            player.max_health += 1
                            player.health = player.max_health
                            room.shopkeeper.items_for_sale['heart_container']['bought'] = True
                            message = f"Bought Heart Container! (100 coins) Coins: {player.coins}"
                            message_timer = 150
                        else:
                            message = f"Heart Container costs 100 coins. You have {player.coins}"
                            message_timer = 120
                    else:
                        message = "Sold out! Thanks for shopping!"
                        message_timer = 90

            attack_rect = player.get_attack_rect()
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
                        message = f"Hit by black knight! Health: {player.health}/{player.max_health}"
                        message_timer = 90
            
            if room.boss and room.boss.is_alive():
                room.boss.update()
                
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                
                # Check fireballs
                for fireball in room.boss.fireballs[:]:
                    fireball_rect = pygame.Rect(fireball.x - fireball.radius, 
                                               fireball.y - fireball.radius,
                                               fireball.radius * 2, fireball.radius * 2)
                    if player_rect.colliderect(fireball_rect):
                        if player.take_damage():
                            message = f"Dragon fire! Health: {player.health}/{player.max_health}"
                            message_timer = 90
                        room.boss.fireballs.remove(fireball)
                
                # Check shockwaves
                for shockwave in room.boss.shockwaves:
                    if player_rect.colliderect(shockwave.get_rect()):
                        if not player.on_ground:  # You can jump over shockwaves!
                            continue
                        if player.take_damage():
                            message = f"Shockwave! Jump to avoid! Health: {player.health}/{player.max_health}"
                            message_timer = 90
                
                # Player attacks dragon
                if attack_rect:
                    boss_rect = pygame.Rect(room.boss.x + 20, room.boss.y + 20, 70, 50)
                    if attack_rect.colliderect(boss_rect):
                        for _ in range(player.sword_level):
                            room.boss.take_damage()
                        message = f"Dragon hit! Health: {room.boss.health}/{room.boss.max_health}"
                        message_timer = 60
                        
                        if not room.boss.is_alive():
                            dragon_defeated = True
                            message = "🎉 YOU DEFEATED THE DRAGON! The kingdom is saved! 🎉"
                            message_timer = 9999
            
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
                        message = "Black knights ahead! Use X to attack!"
                        message_timer = 120
                    else:
                        player.x = SCREEN_WIDTH - player.width - 10
                        message = "You need a special ability to pass..."
                        message_timer = 120
            elif current_room == 'knights':
                if player.x <= 5:
                    current_room = 'item'
                    player.x = SCREEN_WIDTH - player.width - 10
                elif player.x >= SCREEN_WIDTH - player.width - 5:
                    current_room = 'dragon'
                    player.x = 10
                    message = "THE DRAGON! Attack with X! Jump over shockwaves!"
                    message_timer = 180
            elif current_room == 'dragon':
                if player.x <= 5 and not dragon_defeated:
                    current_room = 'knights'
                    player.x = SCREEN_WIDTH - player.width - 10
        
        # Draw
        screen.fill(WHITE)
        
        for platform in room.platforms:
            pygame.draw.rect(screen, BROWN, platform)
            pygame.draw.rect(screen, DARK_BROWN, (platform.x, platform.y, platform.width, 5))
            pygame.draw.rect(screen, GRAY, platform, 2)
        
        for item in room.items:
            item.draw(screen)
        
        for enemy in room.enemies:
            enemy.draw(screen)
        
        if room.boss:
            room.boss.draw(screen)
        for skeleton in room.skeletons:
            skeleton.draw(screen)
        
        for flyer in room.flying_enemies:
            flyer.draw(screen)
        
        for crystal in room.crystals:
            crystal.draw(screen)
        
        for roller in room.rolling_enemies:
            roller.draw(screen)
        
        if room.skeleton_boss:
            room.skeleton_boss.draw(screen)
        
        if room.npc:
            room.npc.draw(screen)
        
        if room.treasure:
            room.treasure.draw(screen)
        
        if room.shopkeeper:
            room.shopkeeper.draw(screen)

        
        player.draw(screen)
        
        # Minimap (only if you have it!)
        if player.has_map:
            draw_minimap(screen, rooms, current_room, player)
        
        # Coin counter
        pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH-120, 10, 110, 30))
        pygame.draw.rect(screen, GOLD, (SCREEN_WIDTH-120, 10, 110, 30), 2)
        pygame.draw.circle(screen, GOLD, (SCREEN_WIDTH-105, 25), 8)
        
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
        
        if player.has_dash:
            pygame.draw.rect(screen, CYAN, (10, 90, 140, 20))
            pygame.draw.rect(screen, WHITE, (12, 92, 136, 16))
            pygame.draw.rect(screen, CYAN, (15, 95, 130, 10))
            pygame.draw.rect(screen, GOLD, (10, 90, 140, 20), 2)
        
        if message_timer > 0:
            msg_width = min(500, len(message) * 8 + 20)
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
