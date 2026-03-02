// Knight's Quest - JavaScript Metroidvania
// Controls: Arrow keys to move, UP to jump, X to attack, D to dash, R to restart

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game constants
const GRAVITY = 0.8;
const JUMP_POWER = -15;
const MOVE_SPEED = 5;
const RUN_SPEED = 8;
const DASH_SPEED = 20;
const DASH_DURATION = 15;

// Game state
const game = {
    player: null,
    keys: {},
    sprites: {},
    spritesLoaded: false,
    currentRoom: 'start',
    coins: 0,
    abilities: {
        doubleJump: false,
        dash: false
    },
    camera: { x: 0, y: 0 }
};

// Sprite configuration
const spriteConfig = {
    idle: { frames: 4, frameWidth: 50 },
    walk: { frames: 8, frameWidth: 50 },
    run: { frames: 7, frameWidth: 50 },
    run_attack: { frames: 6, frameWidth: 60 },
    attack1: { frames: 5, frameWidth: 60 },
    attack2: { frames: 4, frameWidth: 60 },
    attack3: { frames: 4, frameWidth: 60 },
    protect: { frames: 1, frameWidth: 50 },
    hurt: { frames: 2, frameWidth: 50 },
    jump: { frames: 6, frameWidth: 50 },
    dead: { frames: 6, frameWidth: 60 },
    defend: { frames: 5, frameWidth: 50 },
    pickup: { frames: 5, frameWidth: 50 }
};

// Load all sprites
function loadSprites() {
    const spriteNames = Object.keys(spriteConfig);
    let loaded = 0;
    
    spriteNames.forEach(name => {
        const img = new Image();
        img.onload = () => {
            loaded++;
            if (loaded === spriteNames.length) {
                game.spritesLoaded = true;
                init();
            }
        };
        img.src = `sprites/${name}.jpg`;
        game.sprites[name] = img;
    });
}

// Player class
class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 40;
        this.height = 60;
        this.velocityX = 0;
        this.velocityY = 0;
        this.onGround = false;
        this.facingRight = true;
        this.health = 5;
        this.maxHealth = 5;
        this.jumpsLeft = 1;
        this.attacking = false;
        this.attackFrame = 0;
        this.attackType = 1;
        this.dashing = false;
        this.dashTimer = 0;
        this.invincible = false;
        this.invincibleTimer = 0;
        this.hurt = false;
        this.hurtTimer = 0;
        this.defending = false;
        this.pickingUp = false;
        this.pickupTimer = 0;
        this.dying = false;
        this.deathTimer = 0;
        
        // Animation
        this.currentAnimation = 'idle';
        this.frame = 0;
        this.frameTimer = 0;
        this.frameDelay = 5;
    }
    
    update() {
        // Handle death animation
        if (this.dying) {
            this.deathTimer--;
            if (this.deathTimer <= 0) {
                this.respawn();
            }
            return; // Skip other updates while dying
        }
        
        // Handle pickup animation
        if (this.pickingUp) {
            this.pickupTimer--;
            if (this.pickupTimer <= 0) {
                this.pickingUp = false;
            }
            return; // Skip other updates while picking up
        }
        
        // Handle invincibility
        if (this.invincible) {
            this.invincibleTimer--;
            if (this.invincibleTimer <= 0) {
                this.invincible = false;
            }
        }
        
        // Handle hurt animation
        if (this.hurt) {
            this.hurtTimer--;
            if (this.hurtTimer <= 0) {
                this.hurt = false;
            }
        }
        
        // Handle defending (hold S key)
        this.defending = game.keys['s'] && this.onGround;
        
        // Handle dashing
        if (this.dashing) {
            this.dashTimer--;
            if (this.dashTimer <= 0) {
                this.dashing = false;
                this.velocityX = 0;
            }
            return; // Skip other updates while dashing
        }
        
        // Handle attacking
        if (this.attacking) {
            this.attackFrame++;
            const config = spriteConfig[`attack${this.attackType}`];
            if (this.attackFrame >= config.frames * this.frameDelay) {
                this.attacking = false;
                this.attackFrame = 0;
            }
            this.velocityX *= 0.8; // Slow down while attacking
        }
        
        // Horizontal movement
        if (!this.attacking && !this.dashing && !this.defending) {
            if (game.keys['ArrowLeft']) {
                this.velocityX = game.keys['ShiftLeft'] ? -RUN_SPEED : -MOVE_SPEED;
                this.facingRight = false;
            } else if (game.keys['ArrowRight']) {
                this.velocityX = game.keys['ShiftLeft'] ? RUN_SPEED : MOVE_SPEED;
                this.facingRight = true;
            } else {
                this.velocityX *= 0.8;
                if (Math.abs(this.velocityX) < 0.1) this.velocityX = 0;
            }
        } else if (this.defending) {
            this.velocityX *= 0.9; // Slow down while defending
        }
        
        // Jumping
        if (game.keys['ArrowUp'] && !game.keys['ArrowUp_pressed']) {
            if (this.onGround) {
                this.velocityY = JUMP_POWER;
                this.jumpsLeft = game.abilities.doubleJump ? 1 : 0;
                game.keys['ArrowUp_pressed'] = true;
            } else if (this.jumpsLeft > 0) {
                this.velocityY = JUMP_POWER;
                this.jumpsLeft--;
                game.keys['ArrowUp_pressed'] = true;
            }
        }
        
        // Attacking
        if (game.keys['x'] && !game.keys['x_pressed'] && !this.attacking) {
            this.attacking = true;
            this.attackFrame = 0;
            this.attackType = Math.floor(Math.random() * 3) + 1; // Random attack 1-3
            game.keys['x_pressed'] = true;
            this.checkAttackHit();
        }
        
        // Dashing
        if (game.keys['d'] && !game.keys['d_pressed'] && game.abilities.dash && !this.dashing) {
            this.dashing = true;
            this.dashTimer = DASH_DURATION;
            this.velocityX = this.facingRight ? DASH_SPEED : -DASH_SPEED;
            this.velocityY = 0;
            game.keys['d_pressed'] = true;
        }
        
        // Apply gravity
        this.velocityY += GRAVITY;
        
        // Update position
        this.x += this.velocityX;
        this.y += this.velocityY;
        
        // Check collisions
        this.checkCollisions();
        
        // Update animation
        this.updateAnimation();
    }
    
    updateAnimation() {
        let newAnimation = 'idle';
        
        if (this.dying) {
            newAnimation = 'dead';
        } else if (this.pickingUp) {
            newAnimation = 'pickup';
        } else if (this.defending) {
            newAnimation = 'defend';
        } else if (this.hurt) {
            newAnimation = 'hurt';
        } else if (this.dashing) {
            newAnimation = 'run';
        } else if (this.attacking) {
            newAnimation = `attack${this.attackType}`;
        } else if (!this.onGround) {
            newAnimation = 'jump';
        } else if (Math.abs(this.velocityX) > 6) {
            newAnimation = 'run';
        } else if (Math.abs(this.velocityX) > 0.5) {
            newAnimation = 'walk';
        }
        
        if (newAnimation !== this.currentAnimation) {
            this.currentAnimation = newAnimation;
            this.frame = 0;
            this.frameTimer = 0;
        }
        
        // Update frame
        this.frameTimer++;
        if (this.frameTimer >= this.frameDelay) {
            this.frameTimer = 0;
            this.frame++;
            const config = spriteConfig[this.currentAnimation];
            if (this.frame >= config.frames) {
                this.frame = 0;
            }
        }
    }
    
    checkCollisions() {
        const room = rooms[game.currentRoom];
        this.onGround = false;
        
        // Floor collision
        if (this.y + this.height >= canvas.height) {
            this.y = canvas.height - this.height;
            this.velocityY = 0;
            this.onGround = true;
            this.jumpsLeft = game.abilities.doubleJump ? 2 : 1;
        }
        
        // Platform collisions
        room.platforms.forEach(platform => {
            if (this.velocityY >= 0 &&
                this.x + this.width > platform.x &&
                this.x < platform.x + platform.width &&
                this.y + this.height >= platform.y &&
                this.y + this.height <= platform.y + 20) {
                this.y = platform.y - this.height;
                this.velocityY = 0;
                this.onGround = true;
                this.jumpsLeft = game.abilities.doubleJump ? 2 : 1;
            }
        });
        
        // Wall collisions
        if (this.x < 0) this.x = 0;
        if (this.x + this.width > canvas.width) this.x = canvas.width - this.width;
        if (this.y < 0) this.y = 0;
    }
    
    checkAttackHit() {
        const room = rooms[game.currentRoom];
        const attackRange = 80;
        const attackX = this.facingRight ? this.x + this.width : this.x - attackRange;
        
        room.enemies.forEach(enemy => {
            if (!enemy.dead &&
                enemy.x < attackX + attackRange &&
                enemy.x + enemy.width > attackX &&
                enemy.y < this.y + this.height &&
                enemy.y + enemy.height > this.y) {
                enemy.takeDamage(1);
            }
        });
    }
    
    takeDamage(amount) {
        if (this.invincible || this.dying) return;
        
        // Defend blocks 50% damage
        if (this.defending) {
            amount = Math.ceil(amount / 2);
            showMessage('Blocked!');
        }
        
        this.health -= amount;
        this.invincible = true;
        this.invincibleTimer = 60;
        this.hurt = true;
        this.hurtTimer = 20;
        
        if (this.health <= 0) {
            this.die();
        }
        
        updateUI();
    }
    
    die() {
        this.dying = true;
        this.deathTimer = 90; // 1.5 seconds for death animation
        this.velocityX = 0;
        this.velocityY = 0;
    }
    
    respawn() {
        this.dying = false;
        this.health = this.maxHealth;
        this.x = 100;
        this.y = 100;
        this.velocityX = 0;
        this.velocityY = 0;
        game.currentRoom = 'start';
        game.coins = 0;
        updateUI();
    }
    
    draw() {
        ctx.save();
        
        // Flicker when invincible
        if (this.invincible && Math.floor(this.invincibleTimer / 5) % 2 === 0) {
            ctx.globalAlpha = 0.5;
        }
        
        // Flip sprite if facing left
        if (!this.facingRight) {
            ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
            ctx.scale(-1, 1);
            ctx.translate(-(this.x + this.width / 2), -(this.y + this.height / 2));
        }
        
        // Draw current animation frame
        const config = spriteConfig[this.currentAnimation];
        const sprite = game.sprites[this.currentAnimation];
        
        if (sprite && sprite.complete) {
            const frameWidth = config.frameWidth;
            const frameHeight = sprite.height;
            const sourceX = this.frame * frameWidth;
            
            ctx.drawImage(
                sprite,
                sourceX, 0,
                frameWidth, frameHeight,
                this.x - 10, this.y - 10,
                this.width + 20, this.height + 20
            );
        }
        
        ctx.restore();
        
        // Debug hitbox
        // ctx.strokeStyle = 'red';
        // ctx.strokeRect(this.x, this.y, this.width, this.height);
    }
}

// Enemy class
class Enemy {
    constructor(x, y, type = 'knight') {
        this.x = x;
        this.y = y;
        this.width = 40;
        this.height = 60;
        this.type = type;
        this.health = type === 'knight' ? 3 : 2;
        this.speed = 2;
        this.direction = 1;
        this.dead = false;
        this.patrolRange = 200;
        this.startX = x;
    }
    
    update() {
        if (this.dead) return;
        
        // Simple patrol AI
        this.x += this.speed * this.direction;
        
        if (this.x < this.startX - this.patrolRange || this.x > this.startX + this.patrolRange) {
            this.direction *= -1;
        }
        
        // Check collision with player
        if (!game.player.invincible &&
            this.x < game.player.x + game.player.width &&
            this.x + this.width > game.player.x &&
            this.y < game.player.y + game.player.height &&
            this.y + this.height > game.player.y) {
            game.player.takeDamage(1);
        }
    }
    
    takeDamage(amount) {
        this.health -= amount;
        if (this.health <= 0) {
            this.dead = true;
            game.coins += 10;
            updateUI();
        }
    }
    
    draw() {
        if (this.dead) return;
        
        ctx.fillStyle = this.type === 'knight' ? '#333' : '#555';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        // Draw health bar
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x, this.y - 10, this.width, 5);
        ctx.fillStyle = 'green';
        ctx.fillRect(this.x, this.y - 10, this.width * (this.health / 3), 5);
    }
}

// Item class
class Item {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.width = 30;
        this.height = 30;
        this.type = type;
        this.collected = false;
    }
    
    update() {
        if (this.collected) return;
        
        // Check collision with player
        if (game.player.x < this.x + this.width &&
            game.player.x + game.player.width > this.x &&
            game.player.y < this.y + this.height &&
            game.player.y + game.player.height > this.y) {
            this.collect();
        }
    }
    
    collect() {
        this.collected = true;
        
        // Trigger pickup animation
        game.player.pickingUp = true;
        game.player.pickupTimer = 30; // 0.5 seconds
        game.player.velocityX = 0;
        
        if (this.type === 'doubleJump') {
            game.abilities.doubleJump = true;
            showMessage('Double Jump unlocked!');
        } else if (this.type === 'dash') {
            game.abilities.dash = true;
            showMessage('Dash unlocked! Press D');
        } else if (this.type === 'coin') {
            game.coins += 50;
            updateUI();
        }
    }
    
    draw() {
        if (this.collected) return;
        
        if (this.type === 'doubleJump') {
            ctx.fillStyle = '#4fc3f7';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            ctx.fillStyle = 'white';
            ctx.font = '20px Arial';
            ctx.fillText('⬆️⬆️', this.x + 5, this.y + 22);
        } else if (this.type === 'dash') {
            ctx.fillStyle = '#ff9800';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            ctx.fillStyle = 'white';
            ctx.font = '20px Arial';
            ctx.fillText('💨', this.x + 5, this.y + 22);
        } else if (this.type === 'coin') {
            ctx.fillStyle = '#ffd700';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            ctx.fillStyle = 'white';
            ctx.font = '20px Arial';
            ctx.fillText('💰', this.x + 5, this.y + 22);
        }
    }
}

// Room definitions
const rooms = {
    start: {
        name: 'Starting Hall',
        platforms: [
            { x: 200, y: 600, width: 400, height: 20 }
        ],
        enemies: [],
        items: [
            new Item(500, 550, 'coin')
        ],
        exits: [
            { x: canvas.width - 50, y: 0, width: 50, height: canvas.height, to: 'combat1' }
        ]
    },
    combat1: {
        name: 'Knight Chamber',
        platforms: [
            { x: 100, y: 500, width: 300, height: 20 },
            { x: 600, y: 400, width: 300, height: 20 },
            { x: 300, y: 300, width: 200, height: 20 }
        ],
        enemies: [
            new Enemy(150, 440, 'knight'),
            new Enemy(650, 340, 'knight')
        ],
        items: [],
        exits: [
            { x: 0, y: 0, width: 50, height: canvas.height, to: 'start' },
            { x: canvas.width - 50, y: 0, width: 50, height: canvas.height, to: 'powerup1' }
        ]
    },
    powerup1: {
        name: 'Ancient Shrine',
        platforms: [
            { x: 400, y: 500, width: 400, height: 20 }
        ],
        enemies: [],
        items: [
            new Item(565, 450, 'doubleJump')
        ],
        exits: [
            { x: 0, y: 0, width: 50, height: canvas.height, to: 'combat1' },
            { x: canvas.width - 50, y: 0, width: 50, height: canvas.height, to: 'combat2' }
        ]
    },
    combat2: {
        name: 'Guardian Hall',
        platforms: [
            { x: 200, y: 600, width: 200, height: 20 },
            { x: 600, y: 500, width: 200, height: 20 },
            { x: 400, y: 350, width: 200, height: 20 }
        ],
        enemies: [
            new Enemy(250, 540, 'knight'),
            new Enemy(650, 440, 'knight'),
            new Enemy(450, 290, 'knight')
        ],
        items: [],
        exits: [
            { x: 0, y: 0, width: 50, height: canvas.height, to: 'powerup1' },
            { x: canvas.width - 50, y: 0, width: 50, height: canvas.height, to: 'powerup2' }
        ]
    },
    powerup2: {
        name: 'Windswept Peak',
        platforms: [
            { x: 400, y: 450, width: 400, height: 20 }
        ],
        enemies: [],
        items: [
            new Item(565, 400, 'dash')
        ],
        exits: [
            { x: 0, y: 0, width: 50, height: canvas.height, to: 'combat2' }
        ]
    }
};

// Show message
function showMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.textContent = text;
    msgDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 20px 40px;
        border-radius: 10px;
        font-size: 24px;
        z-index: 1000;
    `;
    document.body.appendChild(msgDiv);
    setTimeout(() => msgDiv.remove(), 2000);
}

// Update UI
function updateUI() {
    document.getElementById('health').textContent = `❤️ Health: ${game.player.health}/${game.player.maxHealth}`;
    document.getElementById('coins').textContent = `💰 Coins: ${game.coins}`;
    document.getElementById('room').textContent = `📍 ${rooms[game.currentRoom].name}`;
}

// Input handling
window.addEventListener('keydown', (e) => {
    game.keys[e.key] = true;
    
    // Restart
    if (e.key === 'r') {
        game.player.die();
    }
});

window.addEventListener('keyup', (e) => {
    game.keys[e.key] = false;
    game.keys[e.key + '_pressed'] = false;
});

// Initialize game
function init() {
    game.player = new Player(100, 100);
    updateUI();
    gameLoop();
}

// Check room transitions
function checkRoomTransitions() {
    const room = rooms[game.currentRoom];
    
    room.exits.forEach(exit => {
        if (game.player.x < exit.x + exit.width &&
            game.player.x + game.player.width > exit.x &&
            game.player.y < exit.y + exit.height &&
            game.player.y + game.player.height > exit.y) {
            
            // Change room
            game.currentRoom = exit.to;
            
            // Position player at opposite side
            if (exit.x < canvas.width / 2) {
                game.player.x = canvas.width - 100;
            } else {
                game.player.x = 100;
            }
            game.player.y = 100;
            
            updateUI();
        }
    });
}

// Game loop
function gameLoop() {
    // Clear canvas
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Get current room
    const room = rooms[game.currentRoom];
    
    // Draw platforms
    ctx.fillStyle = '#999';
    room.platforms.forEach(platform => {
        ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
    });
    
    // Draw exits
    ctx.fillStyle = 'rgba(0, 255, 0, 0.3)';
    room.exits.forEach(exit => {
        ctx.fillRect(exit.x, exit.y, exit.width, exit.height);
    });
    
    // Update and draw items
    room.items.forEach(item => {
        item.update();
        item.draw();
    });
    
    // Update and draw enemies
    room.enemies.forEach(enemy => {
        enemy.update();
        enemy.draw();
    });
    
    // Update and draw player
    game.player.update();
    game.player.draw();
    
    // Check room transitions
    checkRoomTransitions();
    
    requestAnimationFrame(gameLoop);
}

// Start loading sprites
loadSprites();
