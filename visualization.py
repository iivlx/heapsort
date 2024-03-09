import tkinter as tk
from heapsort import add_to_heap, remove_min_from_heap
import math

# Global variables for GUI elements and data structures
root = tk.Tk()
heap = []
sequence = [5, 3, 17, 10, 84, 19, 6, 22, 9, 4]
sorted_sequence = []

# Initialize canvas dimensions and other parameters
width = 800
height = 600
heap_canvas = tk.Canvas(root, width=width, height=height // 2, bg='white')
sequence_canvas = tk.Canvas(root, width=width, height=height // 2, bg='white')
heap_draw_params = (width // 2, 20, width - 100, height // 3)
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
def draw_sequence(canvas, sequence, x_start, y_start, box_width, box_height):
    canvas.delete("all")  # Clear the canvas for redrawing the sequence
    x = x_start
    for value in sequence:
        canvas.create_rectangle(x, y_start, x + box_width, y_start + box_height, outline="black")
        canvas.create_text(x + box_width / 2, y_start + box_height / 2, text=str(value))
        x += box_width

def draw_heap(canvas, heap, start_x, start_y, max_width, height, node_radius=20):
    canvas.delete("all")  # Clear the canvas for redrawing the heap
    n = len(heap)
    if n == 0:
        return
    max_level = math.floor(math.log2(n + 1))
    x_spacing = max_width // (2 ** max_level)
    y_spacing = height // (max_level + 1)

    def draw_node(x, y, level, index):
        if index < n:
            child_x_spacing = max(x_spacing // (2 ** level), 2 * node_radius)
            child_level = level + 1
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2

            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="skyblue")
            canvas.create_text(x, y, text=str(heap[index]))

            if left_child_index < n:
                canvas.create_line(x, y, x - child_x_spacing, y + y_spacing)
                draw_node(x - child_x_spacing, y + y_spacing, child_level, left_child_index)
            if right_child_index < n:
                canvas.create_line(x, y, x + child_x_spacing, y + y_spacing)
                draw_node(x + child_x_spacing, y + y_spacing, child_level, right_child_index)

    draw_node(start_x, start_y, 0, 0)

#def draw_sequence(canvas, sequence, x_start, y_start, box_width, box_height):
#    canvas.delete("all")  # Clear the canvas for redrawing the sequence
#    # Drawing logic for sequence and sorted_sequence##


#def draw_heap(canvas, heap, start_x, start_y, max_width, height, node_radius=20):
#    canvas.delete("all")  # Clear the canvas for redrawing the heap
#    # Drawing logic for heap

def update_visualization(value=None):
    if value: sorted_sequence.append(value)
    draw_heap(heap_canvas, heap, *heap_draw_params)
    draw_sequence(sequence_canvas, sequence + sorted_sequence, *sequence_draw_params)
    wait_for_space_press(root)

def main():
    global heap, sequence, sorted_sequence
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

if __name__ == "__main__":
    main()