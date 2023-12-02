import threading 
import time

capacity = 0
blue_waiting = 0
green_waiting = 0
mutex = threading.Semaphore(1)
blue_gate = threading.Semaphore(0)
green_gate = threading.Semaphore(0)

def enter_fitting_room(color, thread_id):

    global capacity, blue_waiting, green_waiting
    mutex.acquire()

    if color == "blue" and green_waiting > 0:
        blue_waiting += 1
        mutex.release()
        blue_gate.acquire()
    elif color == "green" and blue_waiting > 0:
        green_waiting += 1
        mutex.release()
        green_gate.acquire()
    else:
        capacity += 1
        if capacity == 1:
            if color == "blue":
                print("Blue only.")
            elif color == "green":
                print("Green only.")
        mutex.release()
    
    print(f"time: {time.time()} {color} thread with ID {thread_id} entered fitting room.")
    # time.sleep(1)

def exit_fitting_room(color, thread_id):

    global capacity, blue_waiting, green_waiting
    mutex.acquire()
    capacity -= 1
    
    if color == "blue" and capacity == 0:
        while green_waiting > 0:
            green_gate.release()
            green_waiting -= 1
    elif color == "green" and capacity == 0:
        while blue_waiting > 0:
            blue_gate.release()
            blue_waiting -= 1
    
    if capacity == 0:
        print("Empty fitting room.")
    
    print(f"time: {time.time()} {color} thread with ID {thread_id} exited fitting room.")
    # time.sleep(1)
    
    mutex.release()

# get input 

def create_blue_thread(thread_id): 
    enter_fitting_room("blue", thread_id)
    exit_fitting_room("blue", thread_id)

def create_green_thread(thread_id): 
    enter_fitting_room("green", thread_id)
    exit_fitting_room("green", thread_id)

capacity = int(input())
b = int(input())
g = int(input())

threads = []

# Set manual IDs for blue threads
for i in range(b):
    thread = threading.Thread(target=create_blue_thread, args=(f"Blue_{i}",))
    threads.append(thread)
    thread.start()

# Set manual IDs for green threads
for i in range(g):
    thread = threading.Thread(target=create_green_thread, args=(f"Green_{i}",))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
