import pyglet
from pyglet.window import key
from pyglet import shapes
import random

# Create a window
window = pyglet.window.Window(width=800, height=600, caption="Endless Runner Game")

# Define gravity, jump speed, and player speed
gravity = -900
jump_speed = 500
player_speed = 300

# Create a batch for better performance
batch = pyglet.graphics.Batch()

# Create player using shapes
player = shapes.Rectangle(50, 100, 50, 50, color=(50, 225, 30), batch=batch)

# Create ground using shapes
ground = shapes.Rectangle(0, 50, 800, 20, color=(0, 0, 255), batch=batch)

# Variables to track player movement and state
keys = key.KeyStateHandler()
window.push_handlers(keys)
player_velocity_y = 0
is_jumping = False

# List to hold obstacles
obstacles = []

# Function to create obstacles
def create_obstacle():
    x = window.width
    y = ground.y + ground.height
    width = 20
    height = random.randint(20, 50)
    obstacle = shapes.Rectangle(x, y, width, height, color=(255, 0, 0), batch=batch)
    obstacles.append(obstacle)

# Function to update obstacles
def update_obstacles(dt):
    for obstacle in obstacles:
        obstacle.x -= player_speed * dt
    # Remove obstacles that are off-screen
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle.x + obstacle.width > 0]

# Update function to handle movement and gravity
def update(dt):
    global player_velocity_y, is_jumping

    # Apply gravity
    player_velocity_y += gravity * dt

    # Move player vertically
    player.y += player_velocity_y * dt

    # Check for collisions with the ground
    if player.y <= ground.y + ground.height:
        player.y = ground.y + ground.height
        player_velocity_y = 0
        is_jumping = False

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if (player.x + player.width > obstacle.x and player.x < obstacle.x + obstacle.width and
                player.y < obstacle.y + obstacle.height):
            print("Game Over!")
            pyglet.app.exit()

    # Update obstacles
    update_obstacles(dt)

@window.event
def on_key_press(symbol, modifiers):
    global player_velocity_y, is_jumping

    # Handle jump
    if symbol == key.SPACE and not is_jumping:
        player_velocity_y = jump_speed
        is_jumping = True

@window.event
def on_draw():
    window.clear()
    batch.draw()

# Schedule the update function
pyglet.clock.schedule_interval(update, 1/60.0)
# Schedule obstacle creation
pyglet.clock.schedule_interval(lambda dt: create_obstacle(), 1.5)

# Start the game
pyglet.app.run()

# Credits to Proxlight - Subscribe for more Python game tutorials!
print("Thanks for playing! Check out Proxlight on YouTube for more tutorials.")