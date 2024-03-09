def heapify_up(heap, index, callback=None):
    while index != 0:
        parent = (index - 1) // 2
        if heap[index] < heap[parent]:
            heap[index], heap[parent] = heap[parent], heap[index]
            if callback: callback()
        index = parent

def heapify_down(heap, index, callback=None):
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
            if callback: callback()
            index = smallest
        else:
            break

def add_to_heap(heap, value, callback=None):
    heap.append(value)
    if callback: callback()
    heapify_up(heap, len(heap) - 1, callback)

def remove_min_from_heap(heap, callback=None):
    if not heap:
        return None
    heap[0], heap[-1] = heap[-1], heap[0]
    if callback: callback()
    min_value = heap.pop()
    if callback: callback(min_value)
    heapify_down(heap, 0, callback)
    return min_value