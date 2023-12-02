import threading
from time import sleep
import random 

class FittingRoom:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.color = None
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def enter_room(self, thread_id, color):
        with self.lock:
            while self.count >= self.n or (self.color and self.color != color):
                self.condition.wait()

            if self.count == 0:
                self.color = color
                print(f"{color} only.")

            self.count += 1
            print(f"{thread_id} {color}")

    def exit_room(self, thread_id, color):
        with self.lock:
            self.count -= 1

            if self.count == 0:
                self.color = None
                print("Empty fitting room.")

            self.condition.notify_all()

def simulate(thread_id, color, fitting_room):
    fitting_room.enter_room(thread_id, color)
    sleep(1)
    fitting_room.exit_room(thread_id, color)

if __name__ == "__main__":
    input_values = input("Input: ")
    n, b, g = map(int, input_values.split())

    fitting_room = FittingRoom(n)
    threads = []

    for i in range(b):
        thread = threading.Thread(target=simulate, args=(i, 'Blue', fitting_room))
        threads.append(thread)

    for i in range(g):
        thread = threading.Thread(target=simulate, args=(i, 'Green', fitting_room))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
