import heapq

class PriorityQueue:
   def __init__(self):
       self.data = []

   def __len__(self):
       return len(self.data)

   def __bool__(self):
       return bool(self.data)

   """ Insert item into queue with given priority."""
   def append(self, item, priority):
       heapq.heappush(self.data, (priority, item))

   """ Pops item with lowest priority."""
   def pop(self):
       return heapq.heappop(self.data)[1]
