"""
# Global variables
int n_slots = 0
int n_blue_waiting = 0
int n_green_waiting = 0
Semaphore mutex = 1
Semaphore blue_turnstile = 0
Semaphore green_turnstile = 0

# Function for entering fitting room
function enter_fitting_room(color):
    wait(mutex)
    if color == "blue" and n_green_waiting > 0:
        n_blue_waiting++
        signal(mutex)
        wait(blue_turnstile)
    else if color == "green" and n_blue_waiting > 0:
        n_green_waiting++
        signal(mutex)
        wait(green_turnstile)
    else:
        n_slots++
        if n_slots == 1:
            # First thread to enter
            if color == "blue":
                print("Blue only.")
            elif color == "green":
                print("Green only.")
        signal(mutex)
    
    # Inside the fitting room
    print(color, " thread with ID ", get_thread_ID(), " entered.")

# Function for exiting fitting room
function exit_fitting_room(color):
    wait(mutex)
    n_slots--
    if color == "blue" and n_slots == 0:
        while n_green_waiting > 0:
            signal(green_turnstile)
            n_green_waiting--
    else if color == "green" and n_slots == 0:
        while n_blue_waiting > 0:
            signal(blue_turnstile)
            n_blue_waiting--
    if n_slots == 0:
        print("Empty fitting room.")
    signal(mutex)
    
    # Exiting the fitting room
    print(color, " thread with ID ", get_thread_ID(), " exited.")

# Main program
function main():
    input n, b, g from user
    
    # Create b blue threads and g green threads
    for i = 1 to b:
        create_thread("blue", i)
    
    for j = 1 to g:
        create_thread("green", j)
    
    # Wait for all threads to finish
    join_all_threads()
"""