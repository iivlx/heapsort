import tkinter as tk
from heapsort import add_to_heap, remove_min_from_heap
import math
import sys

# Global variables for GUI elements and data structures
root = tk.Tk()
heap = []
#sequence = [5, 3, 17, 10, 84, 19, 6, 22, 9, 4]
sequence = []
default_sequence = [1, 2, 3, 17, 20 , 20, 48, 12, 23 ,41 ,12 ,141 , 4, 5, 6, 55 ,66, 84, 82, 74,8, 9, 14, 81, 17, 64, 4, 7, 8]
sorted_sequence = []

# Initialize canvas dimensions and other parameters
width = 1200
height = 600
heap_canvas = tk.Canvas(root, width=width, height=height * (3/4), bg='white')
sequence_canvas = tk.Canvas(root, width=width, height=height * (1/4), bg='white')
heap_draw_params = (width // 2, 40, width - 100, height // 3)
sequence_draw_params = (20, 10, 50, 20)

# Callback function to control step progression
step_advance = False

def on_space_press(event):
    global step_advance
    step_advance = True

def wait_for_space_press(root):
    global step_advance
    while not step_advance:
        root.update_idletasks()
        root.update()
    step_advance = False

root.bind_all('<space>', on_space_press)

# Visualization functions
def draw_sequence(canvas, sequence, x_start, y_start, box_width, box_height, highlight_index=-1):
    canvas.delete("all")  # Clear the canvas for redrawing the sequence
    x = x_start
    for value in sequence:
        canvas.create_rectangle(x, y_start, x + box_width, y_start + box_height, outline="black")
        canvas.create_text(x + box_width / 2, y_start + box_height / 2, text=str(value))
        x += box_width

def draw_heap(canvas, heap, start_x, start_y, max_width, height, node_radius=20, highlight_index=-1):
    canvas.delete("all")  # Clear the canvas for redrawing the heap
    n = len(heap)
    if n == 0:
        return
    if highlight_index == -1:
        highlight_index = len(heap)-1
    
    max_level = math.floor(math.log2(n))
    min_spacing_x = max_width // (n)  # Calculate the minimum required spacing
    x_spacing = max(min_spacing_x, (max_width / (max_level + 1)))  # Use the larger of the two spacings
    y_spacing = height // (max_level + 1)

    def draw_node(x, y, level, index):
        if index < n:
            child_x_spacing = max(x_spacing // (2 ** level), 2 * node_radius)
            child_level = level + 1
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            fill_color = "yellow" if index == highlight_index else "skyblue"
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill=fill_color)
            canvas.create_text(x, y, text=str(heap[index]))

            if left_child_index < n:
                canvas.create_line(x, y, x - child_x_spacing, y + y_spacing)
                draw_node(x - child_x_spacing, y + y_spacing, child_level, left_child_index)
            if right_child_index < n:
                canvas.create_line(x, y, x + child_x_spacing, y + y_spacing)
                draw_node(x + child_x_spacing, y + y_spacing, child_level, right_child_index)

    draw_node(start_x, start_y, 0, 0)

def update_visualization(value=None, highlight_index=-1):
    if value: sorted_sequence.append(value)
    draw_heap(heap_canvas, heap, *heap_draw_params, highlight_index=highlight_index)
    draw_sequence(sequence_canvas, sequence + sorted_sequence, *sequence_draw_params, highlight_index=highlight_index)
    wait_for_space_press(root)

def main():
    global heap, sequence, default_sequence, sorted_sequence
    heap_canvas.pack()
    sequence_canvas.pack()
    root.title("Heap Sort Visualization")
    update_visualization()
    # Move elements from the sequence to the heap
    for value in sequence[:]:
        sequence = sequence[1:]  # Update sequence to remove the first element
        add_to_heap(heap, value, update_visualization)

    # Sorting and displaying sorted elements
    while heap:
        remove_min_from_heap(heap, callback=update_visualization)

    root.mainloop()

def read_file(filename):
    global sequence
    try:
        with open(filename, 'r') as file:
            content = file.read()
            sequence = [int(size) for size in content.strip().split(' ')]
    except Exception as e:
        print("Invalid file name...")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        read_file(filename)
    else:
        sequence = default_sequence
    main()