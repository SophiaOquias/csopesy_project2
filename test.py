from threading import Thread, Lock, BoundedSemaphore, Semaphore, current_thread
from time import sleep

def blue_process():
    global blue_lock, green_lock, fitting_slots, blue_limit, green_limit
    global total_slots, blue_count, green_count
    
    blue_limit.acquire()

    while green_lock.locked():
        pass

    if not blue_lock.locked() and not green_lock.locked():
        blue_lock.acquire()
        print("Blue only.")

    fitting_slots.acquire()
    print(current_thread().name)

    sleep(1)

    global completed_blue_processes
    completed_blue_processes += 1

    fitting_slots.release()

    global completed_green_processes

    if completed_blue_processes == blue_count or (completed_blue_processes % total_slots == 0 and completed_green_processes != green_count):
        print("Empty fitting room.")
        
        if completed_green_processes != green_count:
            for _ in range(total_slots):
                green_limit.release()
            
            # Ensure the lock is acquired before releasing
            if blue_lock.locked():
                blue_lock.release()

    elif completed_green_processes == green_count:
        # Ensure the lock is acquired before releasing
        if blue_lock.locked():
            blue_lock.release()

def green_process():
    global blue_lock, green_lock, fitting_slots, green_limit, blue_limit
    global total_slots, blue_count, green_count
    
    green_limit.acquire()

    while blue_lock.locked():
        pass
    
    if not green_lock.locked() and not blue_lock.locked():
        green_lock.acquire()
        print("Green only.")
    
    fitting_slots.acquire()
    print(current_thread().name)

    sleep(1)

    global completed_green_processes
    completed_green_processes += 1

    fitting_slots.release()

    global completed_blue_processes

    if completed_green_processes == green_count or (completed_green_processes % total_slots == 0 and completed_blue_processes != blue_count):
        print("Empty fitting room.")
        
        if completed_blue_processes != blue_count:
            for _ in range(total_slots):
                blue_limit.release()
            
            green_lock.release()

    elif completed_blue_processes == blue_count:
        green_limit.release()

def main():
    global blue_lock, green_lock, fitting_slots, blue_limit, green_limit
    global total_slots, blue_count, green_count, completed_blue_processes, completed_green_processes

    total_slots, blue_count, green_count = map(int, input("Input values: ").split())
    fitting_slots = BoundedSemaphore(total_slots)
    blue_lock, green_lock = Lock(), Lock()
    completed_blue_processes, completed_green_processes = 0, 0
    limit_value = total_slots + 5

    if blue_count <= 0:
        green_limit, blue_limit = Semaphore(limit_value), Semaphore(0)
    else:
        blue_limit, green_limit = Semaphore(limit_value), Semaphore(0)

    for i in range(1, blue_count+1):
        Thread(target=blue_process, name=f"{i} Blue").start()

    for i in range(1, green_count+1):
        Thread(target=green_process, name=f"{i} Green").start()

if __name__ == "__main__":
    main()
