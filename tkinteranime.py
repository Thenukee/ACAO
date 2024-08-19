import tkinter as tk
import time

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

# Function to draw the animation
def animate():
    for block_address in range(NUM_MEMORY_BLOCKS * 2):  # Loop to show the animation multiple times
        index = cache_line_index(block_address % NUM_MEMORY_BLOCKS)
        
        # Clear the canvas
        canvas.delete("all")

        # Draw main memory blocks
        for i in range(NUM_MEMORY_BLOCKS):
            color = 'grey' if i != block_address % NUM_MEMORY_BLOCKS else 'blue'
            canvas.create_rectangle(50, 50 + i * MEMORY_BLOCK_HEIGHT, 200, 50 + (i + 1) * MEMORY_BLOCK_HEIGHT, fill=color)
            canvas.create_text(125, 50 + (i + 0.5) * MEMORY_BLOCK_HEIGHT, text=f"Block {i}")

        # Update cache
        update_cache(block_address % NUM_MEMORY_BLOCKS)

        # Draw cache lines
        for i in range(NUM_CACHE_LINES):
            color = 'lightblue' if cache[i] != -1 else 'white'
            canvas.create_rectangle(300, 50 + i * CACHE_LINE_HEIGHT, 450, 50 + (i + 1) * CACHE_LINE_HEIGHT, fill=color, outline='black')
            if cache[i] != -1:
                canvas.create_text(375, 50 + (i + 0.5) * CACHE_LINE_HEIGHT, text=cache_data[i])
        
        # Draw labels
        canvas.create_text(125, 30, text="Main Memory")
        canvas.create_text(375, 30, text="Cache Lines")

        # Update the canvas
        root.update()
        time.sleep(1)

# Run the animation
animate()

# Start the Tkinter event loop
root.mainloop()
