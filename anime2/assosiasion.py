import tkinter as tk
import time
from PIL import Image, ImageTk

# Constants
NUM_CACHE_LINES = 8  # Total cache lines
SET_SIZE = 2  # Number of lines per set (2-way set associative)
NUM_SETS = NUM_CACHE_LINES // SET_SIZE  # Number of sets
NUM_MEMORY_BLOCKS = 8
CACHE_LINE_HEIGHT = 50
MEMORY_BLOCK_HEIGHT = 40  # Height for main memory blocks

# Initialize cache tags and data for each set
cache_tags = [[-1] * SET_SIZE for _ in range(NUM_SETS)]
cache_data = [[''] * SET_SIZE for _ in range(NUM_SETS)]

# Function to calculate set index
def set_index(block_address):
    return block_address % NUM_SETS

# Function to update cache (Set-Associative Mapping)
def update_cache(block_address):
    set_idx = set_index(block_address)
    
    # Check if the block is already in the set (cache hit)
    if block_address in cache_tags[set_idx]:
        return False  # Cache hit
    
    # Cache miss - find an empty line in the set or replace the oldest (FIFO for simplicity)
    for i in range(SET_SIZE):
        if cache_tags[set_idx][i] == -1:  # Empty line found
            cache_tags[set_idx][i] = block_address
            cache_data[set_idx][i] = f"Block {block_address}"
            return True  # Cache miss, but space was available
    
    # If no empty line, replace the first one (FIFO)
    cache_tags[set_idx].pop(0)
    cache_data[set_idx].pop(0)
    cache_tags[set_idx].append(block_address)
    cache_data[set_idx].append(f"Block {block_address}")
    return True  # Cache miss

# Create the main application window
root = tk.Tk()
root.title("Set-Associative Mapping Cache Animation")

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Load CPU image
cpu_image = Image.open("cpu.png")
cpu_image = cpu_image.resize((80, 80), Image.Resampling.LANCZOS)
cpu_photo = ImageTk.PhotoImage(cpu_image)

# Function to draw arrows
def draw_arrow(canvas, x1, y1, x2, y2, color="black"):
    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color, width=2)

# Function to draw the animation
def animate():
    for block_address in range(NUM_MEMORY_BLOCKS * 2):  # Loop to show the animation multiple times
        set_idx = set_index(block_address % NUM_MEMORY_BLOCKS)
        
        # Clear the canvas
        canvas.delete("all")

        # Draw CPU image
        canvas.create_image(40, 50, image=cpu_photo)
        canvas.create_text(40, 100, text="CPU", font=("Arial", 12, "bold"))

        # Draw main memory blocks with addresses and block numbers
        for i in range(NUM_MEMORY_BLOCKS):
            color = 'grey' if i != block_address % NUM_MEMORY_BLOCKS else 'blue'
            canvas.create_rectangle(550, 100 + i * MEMORY_BLOCK_HEIGHT, 700, 100 + (i + 1) * MEMORY_BLOCK_HEIGHT, fill=color)
            canvas.create_text(625, 100 + (i + 0.5) * MEMORY_BLOCK_HEIGHT, text=f"Block {i}\nAddr {i*4:02X}", font=("Arial", 10))

        # Update cache
        is_cache_miss = update_cache(block_address % NUM_MEMORY_BLOCKS)

        # Draw cache lines with data
        for set_idx in range(NUM_SETS):
            for line_idx in range(SET_SIZE):
                color = 'lightblue' if cache_tags[set_idx][line_idx] != -1 else 'white'
                canvas.create_rectangle(250, 100 + (set_idx * SET_SIZE + line_idx) * CACHE_LINE_HEIGHT, 400, 100 + (set_idx * SET_SIZE + line_idx + 1) * CACHE_LINE_HEIGHT, fill=color, outline='black')
                if cache_tags[set_idx][line_idx] != -1:
                    canvas.create_text(325, 100 + (set_idx * SET_SIZE + line_idx + 0.5) * CACHE_LINE_HEIGHT, text=f"Block {cache_tags[set_idx][line_idx]} (Addr {cache_tags[set_idx][line_idx]*4:02X})", font=("Arial", 10))

        # Draw arrows
        if is_cache_miss:
            # Draw arrow for cache miss (to the relevant set)
            draw_arrow(canvas, 80, 100, 250, 100 + set_idx * SET_SIZE * CACHE_LINE_HEIGHT + CACHE_LINE_HEIGHT // 2, color="red")
            canvas.create_text(165, 80, text="Cache Miss", fill="red", font=("Arial", 10, "bold"))
        else:
            # Only find the hit line index if the block is in the set
            if block_address % NUM_MEMORY_BLOCKS in cache_tags[set_idx]:
                hit_line_idx = cache_tags[set_idx].index(block_address % NUM_MEMORY_BLOCKS)
                draw_arrow(canvas, 80, 100, 250, 100 + (set_idx * SET_SIZE + hit_line_idx) * CACHE_LINE_HEIGHT + CACHE_LINE_HEIGHT // 2, color="green")
                canvas.create_text(165, 80, text="Cache Hit", fill="green", font=("Arial", 10, "bold"))

        # Draw calculation steps
        canvas.create_text(125, 300, text=f"Calculation:", font=("Arial", 12, "bold"))
        canvas.create_text(125, 330, text=f"Block Address: {block_address % NUM_MEMORY_BLOCKS}", font=("Arial", 12))
        canvas.create_text(125, 360, text=f"Set Index = {block_address % NUM_MEMORY_BLOCKS} % {NUM_SETS} = {set_idx}", font=("Arial", 12, "bold"))

        # Draw labels
        canvas.create_text(625, 70, text="Main Memory", font=("Arial", 12, "bold"))
        canvas.create_text(325, 70, text="Cache Lines", font=("Arial", 12, "bold"))

        # Update the canvas
        root.update()
        time.sleep(1)

# Function to start animation
def start_animation():
    animate()

# Add Start button
start_button = tk.Button(root, text="Start Animation", command=start_animation)
start_button.pack()

# Start the Tkinter event loop
root.mainloop()