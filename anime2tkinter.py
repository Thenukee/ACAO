import tkinter as tk
import time
from PIL import Image, ImageTk

# Constants
NUM_CACHE_LINES = 4
NUM_MEMORY_BLOCKS = 16
CACHE_LINE_HEIGHT = 50
MEMORY_BLOCK_HEIGHT = 20

# Initialize cache tags and data
cache = [-1] * NUM_CACHE_LINES
cache_data = [''] * NUM_CACHE_LINES

# Function to calculate cache line index
def cache_line_index(block_address):
    return block_address % NUM_CACHE_LINES

# Function to update cache
def update_cache(block_address):
    index = cache_line_index(block_address)
    cache[index] = block_address
    cache_data[index] = f"Block {block_address}"

# Create the main application window
root = tk.Tk()
root.title("Direct Mapping Cache Animation")

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
        index = cache_line_index(block_address % NUM_MEMORY_BLOCKS)
        
        # Clear the canvas
        canvas.delete("all")

        # Draw CPU image
        canvas.create_image(40, 50, image=cpu_photo)
        canvas.create_text(40, 100, text="CPU", font=("Arial", 12, "bold"))

        # Draw main memory blocks with addresses
        for i in range(NUM_MEMORY_BLOCKS):
            color = 'grey' if i != block_address % NUM_MEMORY_BLOCKS else 'blue'
            canvas.create_rectangle(550, 100 + i * MEMORY_BLOCK_HEIGHT, 700, 100 + (i + 1) * MEMORY_BLOCK_HEIGHT, fill=color)
            canvas.create_text(625, 100 + (i + 0.5) * MEMORY_BLOCK_HEIGHT, text=f"Addr {i*4:02X}")

        # Update cache
        is_cache_miss = cache[index] != block_address % NUM_MEMORY_BLOCKS
        update_cache(block_address % NUM_MEMORY_BLOCKS)

        # Draw cache lines with data
        for i in range(NUM_CACHE_LINES):
            color = 'lightblue' if cache[i] != -1 else 'white'
            canvas.create_rectangle(250, 100 + i * CACHE_LINE_HEIGHT, 400, 100 + (i + 1) * CACHE_LINE_HEIGHT, fill=color, outline='black')
            if cache[i] != -1:
                canvas.create_text(325, 100 + (i + 0.5) * CACHE_LINE_HEIGHT, text=f"Block {cache[i]} (Addr {cache[i]*4:02X})")
        
        # Draw arrows
        if is_cache_miss:
            # Draw arrow for cache miss
            draw_arrow(canvas, 80, 100, 250, 100 + index * CACHE_LINE_HEIGHT + CACHE_LINE_HEIGHT // 2, color="red")
            canvas.create_text(165, 80, text="Cache Miss", fill="red", font=("Arial", 10, "bold"))
        else:
            # Draw arrow for cache hit
            draw_arrow(canvas, 80, 100, 250, 100 + index * CACHE_LINE_HEIGHT + CACHE_LINE_HEIGHT // 2, color="green")
            canvas.create_text(165, 80, text="Cache Hit", fill="green", font=("Arial", 10, "bold"))

        # Draw labels
        canvas.create_text(625, 70, text="Main Memory", font=("Arial", 12, "bold"))
        canvas.create_text(325, 70, text="Cache Lines", font=("Arial", 12, "bold"))

        # Update the canvas
        root.update()
        time.sleep(1)

# Run the animation
animate()

# Start the Tkinter event loop
root.mainloop()
