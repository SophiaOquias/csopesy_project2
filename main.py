from threading import Thread, BoundedSemaphore, Lock
from time import sleep

n, b, g = map(int, input("Enter n, b, g values: ").split())
room = BoundedSemaphore(value=n)
blue_done, green_done = 0, 0
id = 1
switch = n
mtx = Lock()

def fit_room(color):
    global id, blue_done, green_done
    print(f"ID: {id} Color: {color}")
    if color == 'Green':
        green_done += 1
    else:
        blue_done += 1

    id += 1
    sleep(1)
    room.release()

    if room._value == n:
        print("\nEmpty fitting room")

def color_func(color):
    global id, mtx, room, blue_done, green_done, switch
    ctr = 0

    while (green_done != g and color == 'Green') or (blue_done != b and color == 'Blue'):
        mtx.acquire()
        print(f"\n{color} Only")

        temp = 1
        while temp == 1:
            room.acquire()
            Thread(target=lambda: fit_room(color)).start()
            sleep(1)

            if (green_done != g and color == 'Green') or (blue_done != b and color == 'Blue'):
                if ctr == switch - 1:
                    other_color_done = green_done if color == 'Blue' else blue_done
                    if other_color_done != (g if color == 'Green' else b):
                        while room._value != n:
                            pass
                        mtx.release()
                        sleep(1)
                        temp = 0
                        ctr = 0
                else:
                    ctr += 1
            elif (green_done == g and color == 'Green') or (blue_done == b and color == 'Blue'):
                ctr = 0
                while room._value != n:
                    pass
                mtx.release()
                sleep(1)
                temp = 0

def main():
    global n, b, g
    green_thread = Thread(target=lambda: color_func('Green'))
    blue_thread = Thread(target=lambda: color_func('Blue'))

    green_thread.start()
    sleep(1)
    blue_thread.start()

if __name__ == "__main__":
    main()