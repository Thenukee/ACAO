import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
NUM_CACHE_LINES = 4
NUM_MEMORY_BLOCKS = 16

# Cache line colors
cache_colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']
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

# Animation function
def animate(frame):
    block_address = frame % NUM_MEMORY_BLOCKS
    index = cache_line_index(block_address)

    # Clear the plot
    plt.clf()

    # Plot main memory blocks
    plt.subplot(2, 1, 1)
    for i in range(NUM_MEMORY_BLOCKS):
        plt.bar(i, 1, color='grey' if i != block_address else 'blue')
    plt.title(f"Accessing Main Memory Block {block_address}")
    plt.xlabel("Memory Blocks")
    plt.ylabel("Access")

    # Update cache
    update_cache(block_address)

    # Plot cache lines
    plt.subplot(2, 1, 2)
    for i in range(NUM_CACHE_LINES):
        plt.bar(i, 1, color=cache_colors[i] if cache[i] != -1 else 'white', edgecolor='black')
        plt.text(i, 0.5, cache_data[i], ha='center', va='center')
    plt.title(f"Cache Lines (Block {block_address} -> Cache Line {index})")
    plt.xlabel("Cache Lines")
    plt.ylabel("Storage")

# Create the animation
fig = plt.figure(figsize=(10, 6))
anim = FuncAnimation(fig, animate, frames=range(32), interval=1000, repeat=True)

plt.show()
