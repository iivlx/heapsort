import tkinter as tk
import math

# Global flag to control step progression
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

def add_to_heap(heap, value, heap_canvas, sequence, sequence_canvas, heap_draw_params, sequence_draw_params):
    heap.append(value)  # Add value to the heap
    sequence.remove(value)  # Remove value from sequence
    draw_heap(heap_canvas, heap, *heap_draw_params)
    draw_sequence(sequence_canvas, sequence, *sequence_draw_params)
    wait_for_space_press(root)
    heapify_up(heap, len(heap) - 1, heap_canvas, heap_draw_params)

def heapify_up(heap, index, canvas, heap_draw_params):
    while index != 0:
        parent = (index - 1) // 2
        if heap[index] < heap[parent]:
            heap[index], heap[parent] = heap[parent], heap[index]
            draw_heap(canvas, heap, *heap_draw_params)
            wait_for_space_press(root)
        index = parent

def heapify_down(heap, index, canvas, heap_draw_params):
    n = len(heap)
    while index < n:
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right
        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            draw_heap(canvas, heap, *heap_draw_params)
            wait_for_space_press(root)  # Now visualizing each swap
            index = smallest
        else:
            break

def remove_min_from_heap(heap, heap_canvas, sequence_canvas, heap_draw_params, sequence_draw_params, sorted_sequence):
    if not heap: return
    # Swap the first and last element, then pop min (last) element
    heap[0], heap[-1] = heap[-1], heap[0]
    min_value = heap.pop()
    # Before adjusting the heap, let's draw this intermediate state
    draw_heap(heap_canvas, heap, *heap_draw_params)
    wait_for_space_press(root)  # Visualize the swap
    heapify_down(heap, 0, heap_canvas, heap_draw_params)
    # Now add the removed min value to the sorted sequence
    sorted_sequence.append(min_value)
    # Ensure we draw the updated sequence AFTER the heap is adjusted and displayed
    x_start, y_start, box_width, box_height = sequence_draw_params
    y_start += 50  # Positioning for the sorted sequence visualization
    draw_sequence(sequence_canvas, [], x_start, y_start, box_width, box_height)  # Clear previous visualization
    draw_sequence(sequence_canvas, sorted_sequence, x_start, y_start, box_width, box_height)

def main():
    global root
    root = tk.Tk()
    root.title("Heap Sort Visualization with Continuous Updates")
    width = 800
    height = 600

    root.bind('<space>', on_space_press)

    # Set up frames for sequence and heap visualization
    sequence_frame = tk.Frame(root, height=height // 3)
    heap_frame = tk.Frame(root, height=2 * height // 3)
    sequence_frame.pack(fill=tk.X)
    heap_frame.pack(fill=tk.X)

    sequence_canvas = tk.Canvas(sequence_frame, bg='white', height=height // 3)
    heap_canvas = tk.Canvas(heap_frame, bg='white', height=2 * height // 3)
    sequence_canvas.pack(fill=tk.X)
    heap_canvas.pack(fill=tk.X)

    sequence = [5, 3, 17, 10, 84, 19, 6, 22, 9, 4]
    heap = []
    sorted_sequence = []
    heap_draw_params = (width // 2, 20, width - 100, height // 3)
    sequence_draw_params = (20, 10, 50, 20)

    # Display the initial sequence
    draw_sequence(sequence_canvas, sequence, *sequence_draw_params)

    # Move elements from the sequence to the heap
    for value in sequence[:]:
        add_to_heap(heap, value, heap_canvas, sequence, sequence_canvas, heap_draw_params, sequence_draw_params)

    # Sorting and displaying sorted elements
    while heap:
        remove_min_from_heap(heap, heap_canvas, sequence_canvas, heap_draw_params, sequence_draw_params, sorted_sequence)

    root.mainloop()

if __name__ == "__main__":
    main()
