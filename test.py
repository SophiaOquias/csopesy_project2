import threading
import time

class FittingRoom:
    def __init__(self, n):
        self.n = n
        self.blue_slots = threading.Semaphore(n)
        self.green_slots = threading.Semaphore(n)
        self.room_lock = threading.Lock()
        self.blue_counter = 0
        self.green_counter = 0
        self.is_room_empty = True

    def enter_room(self, thread_id, color):
        with self.room_lock:
            if self.is_room_empty:
                if color == 'blue':
                    print("Blue only.")
                elif color == 'green':
                    print("Green only.")
                self.is_room_empty = False

            if color == 'blue':
                while self.green_counter > 0:
                    self.room_lock.release()
                    time.sleep(0.1)  # Add a small delay to reduce busy waiting
                    self.room_lock.acquire()
                self.blue_counter += 1
            else:
                while self.blue_counter > 0:
                    self.room_lock.release()
                    time.sleep(0.1)  # Add a small delay to reduce busy waiting
                    self.room_lock.acquire()
                self.green_counter += 1

        if color == 'blue':
            self.blue_slots.acquire()
        else:
            self.green_slots.acquire()

        timestamp_ms = int(time.time() * 1000)
        print(f"{timestamp_ms} - {thread_id} ({color}) entered the fitting room.")

    def exit_room(self, thread_id, color):
        with self.room_lock:
            timestamp_ms = int(time.time() * 1000)
            print(f"{timestamp_ms} - {thread_id} ({color}) exited the fitting room.")
            if color == 'blue':
                self.blue_counter -= 1
                if self.blue_counter == 0:
                    self.is_room_empty = True
                self.blue_slots.release()
            else:
                self.green_counter -= 1
                if self.green_counter == 0:
                    self.is_room_empty = True
                self.green_slots.release()

def simulate_fitting_room(n, b, g):
    fitting_room = FittingRoom(n)

    def blue_thread(thread_id):
        fitting_room.enter_room(thread_id, 'blue')
        time.sleep(1)  # Simulate some work inside the fitting room
        fitting_room.exit_room(thread_id, 'blue')

    def green_thread(thread_id):
        fitting_room.enter_room(thread_id, 'green')
        time.sleep(1)  # Simulate some work inside the fitting room
        fitting_room.exit_room(thread_id, 'green')

    threads = []

    for i in range(b):
        thread = threading.Thread(target=blue_thread, args=(f"Blue-{i}",))
        threads.append(thread)

    for i in range(g):
        thread = threading.Thread(target=green_thread, args=(f"Green-{i}",))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    n = int(input("Enter the number of slots inside the fitting room: "))
    b = int(input("Enter the number of blue threads: "))
    g = int(input("Enter the number of green threads: "))

    simulate_fitting_room(n, b, g)
