import pyautogui
import time
import os
import random
from pynput.keyboard import Listener
import platform
import threading
plat = platform.system()
if plat != "Darwin":
    import winsound



boss_colour = [116,255,255]
cave_colour = [255,0,255]
 # set to 20 for PC

max_hours = 10
max_time = 60*60* max_hours
delay = random.randint(10,20)

skill_info = []
skill_loc = 0

crop_info = []


def play_sound(type):
    os.system(f"afplay /System/Library/Sounds/{type}.aiff")

def make_sound(freq=500,duration=100,type='Ping'):
    # types: Ping,Hero,Glass,Funk,Bottle
    if plat == "Darwin":
        t = threading.Thread(target=play_sound,args=(type,)).start()
        
    else:
        winsound.Beep(freq,duration)



def find(colour,region):
    tolerance = 20
    img = pyautogui.screenshot(region=region)
    width, height = img.size
    pixels = img.load()

    matches = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]

            if (abs(r - colour[0]) <= tolerance and
                abs(g - colour[1]) <= tolerance and
                abs(b - colour[2]) <= tolerance):

                matches.append((x, y))

    return matches 


def click(pos,matches,region,miss_click=False):
    # y, x = match[0][0], match[1][0]

    # screen_x = x + region[0]
    # screen_y = y + region[1]
    # split x and y
    xs = [p[0] for p in matches]
    ys = [p[1] for p in matches]

    # bounding box
    left   = min(xs)
    right  = max(xs)
    top    = min(ys)
    bottom = max(ys)

    # midpoint
    mid_x = (left + right) / 2
    mid_y = (top + bottom) / 2

    # convert to screen coords
    screen_x = mid_x + region[0]
    screen_y = mid_y + region[1]

    # optional miss click
    if miss_click:
        screen_y += mid_y / 8

    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.click()

    make_sound(500, 100)

    pyautogui.moveTo(pos, duration=0.2)

def press_to_start(key):
    global skill_info
    global skill_loc
    global main_region
    try:
        if key.char == 'g':
            x,y = skill_info[-2][0], skill_info[-2][1]
            x_size = skill_info[-1][0] - x
            y_size = skill_info[-1][1] - y
            skill_loc = (x, y, x_size, y_size)

            screen_res_x, screen_res_y = pyautogui.size()
            x_diff = screen_res_x - skill_info[-3][0]
            y_diff = screen_res_y - skill_info[-4][1]

            main_region = (0, 0, screen_res_x - x_diff, screen_res_y - y_diff)

            print(screen_res_x,': ',screen_res_y)
            print(f"\nMain game region: {main_region}")
            print(f"Skill XP display: {skill_loc}\n")
            
            return False
        

        elif key.char == 'l':
            skill_info.append(pyautogui.position())
            make_sound(1000,100)


        else:
            print("wait")
            pass
    except:
        pass

def get_turn_off_time():

    while True:
        length = input("Enter run time in hours (e.g. 3.1 or 4): ")
        try:
            length = float(length)
            length = length * 3600
            return length
        except:
            print("Enter Numbers only (e.g. 3.1 or 4)")
            



def main():
    if plat == 'Darwin':
        os.system('clear')
    else:
        os.system('cls')
    
    
    run_time = get_turn_off_time()
    

    if plat == 'Darwin':
        os.system('clear')
    else:
        os.system('cls')
    make_sound()

    print("Set NPC tag colour to R = 116, G = 255, B = 255 Op = 255")
    print("Set tile marker to Border = 10, Colour R = 255, G = 0, B = 255, Op = 255")
    print("Tag Crab. Mark each cave tile.\n")
    print("Hover mouse over mouse locations and press 'l' for each of the following locations:\n\n\t1: Top of Windows Taskbar.\n\t2: Left edge of Mini Map (or right most edge of gameplay area).\n\t3: Top left of where skill XP is shown while fighting.\n\t4: Botton right of where skill XP is shown while fighting.\n")
    print("Press 'g' so start once 4 locations are logged.")
    print(f"Run time = {run_time/3600} Hours ({run_time} secs)")
    with Listener(on_press=press_to_start) as l:
        l.join()
    if plat != "Darwin":
        for t in range(3):
            make_sound(500,100)
            
            if plat != "Darwin":
                time.sleep(0.9)

    make_sound(800,100,type='Glass')
    
    pos = pyautogui.position()
    fight_count = 1
    start_bot_timer = time.perf_counter()


    while time.perf_counter() - start_bot_timer < run_time:
        # Find Boss.............................................
        print(f"Start fight {fight_count}")
        print("Looking for Boss")
        for x in range(2):
            while True:
                while True:
                    try:
                        matches = find(boss_colour, main_region)
                        break
                    except:
                        time.sleep(1)
        
                if matches:
                    time.sleep(1.5)
                    print(f"Found Boss: {x+1}",end='\r')
                    break
                time.sleep(1)

        print("\nBoss Confirmed, Pause 2 seconds")    
        time.sleep(2)
            
        # Pause.................................................
        

    
        # Start Fight (click boss)..............................
        while True:
            try:
                matches = find(boss_colour,main_region)
                break
            except:
                pass

        print("Start Combat",end='')
        # click(pos,matches,main_region)
        # Stop Crash if screen changed after finding boss...............
        x = 0
        while True:
            try:
                click(pos,matches,main_region)
                break
            except:
                x += 1
                if x > 2:
                    break
                time.sleep(0.5)

        start_time = time.perf_counter()
        fight_timer = start_time


        # Wait for boss to vanish...............................
       
  
        skill_img = pyautogui.screenshot(region=skill_loc)
        idle_delay = random.randint(200,240)
        idle_delay = 10
        fight_status = 'fight'
        x = 1
        while True:
            time.sleep(1)
            while True:
                try:
                    matches = find(boss_colour, main_region)
                    break
                except:
                    time.sleep(1)

            if not matches: # If Boss has vanished then end pause 1 seconds.....
                time.sleep(1)
                break

            time.sleep(2)

            while True:
                try:
                    matches = find(boss_colour, main_region)
                    break
                except:
                    time.sleep(1)

            if not matches: # If Boss has vanished then end pause 1 seconds.....
                print("Boss Finished")
                time.sleep(1)
                break

            time.sleep(0.1)

            skill_current = pyautogui.screenshot(region=skill_loc)
            if skill_current == skill_img:
                time.sleep(0.1)
                while True:
                    try:
                        matches = find(boss_colour, main_region)
                        break
                    except:
                        time.sleep(1)
                
                
                if matches:
                    if fight_status != 'Out_of_Combat':
                        x = 1
                        print("\nOut of Combat Clicked",end='\r')
                    else:
                        print(f"Out of Combat Clicked {x}",end='\r')
                        x += 1
                    fight_status = 'Out_of_Combat'
                    click(pos, matches, main_region)
                    skill_img = pyautogui.screenshot(region=skill_loc)
                    start_time = time.perf_counter()
                
            elif time.perf_counter() - start_time > idle_delay:
                while True:
                    try:
                        matches = find(boss_colour, main_region)
                        break
                    except:
                        time.sleep(1)
                
                if matches:
                    if fight_status != 'Idle':
                        x = 1
                        print("\nIdle Timer Clicked       ",end='\r')
                    else:
                        print(f"Idle Timer Clicked {x}     ",end='\r')
                        x += 1

                    fight_status = 'Idle'
                    click(pos, matches, main_region)
                    start_time = time.perf_counter()
                    idle_delay = random.randint(200,240)

            else:
                if fight_status != 'Combat':
                    x = 1
                    print(f"\nIn Combat {x}                   ",end='\r')
                else:
                    print(f"In Combat {x}                   ",end='\r')
                    x += 1
                fight_status = 'Combat'
                skill_img = pyautogui.screenshot(region=skill_loc)


            
           


        # Find Cave.............................................
        x = 1
        missclick = random.choice([False, False, False, True])
        
        
        while True:
            print(f"Looking for Cave {x}   ")
            x += 1

            while True:
                try:
                    matches = find(cave_colour, main_region)
                    break
                except:
                    time.sleep(1)

            if matches:
                print("Found Cave")
                if missclick:
                    click(pos, matches, main_region, miss_click=missclick)
                    print("MissClicked")
                    time.sleep(10)
                    missclick = False

                    while True:
                        try:
                            matches = find(cave_colour, main_region)
                            break
                        except:
                            time.sleep(1)
                            
                    click(pos, matches, main_region)
                    time.sleep(10)
                    break

                else:
                    click(pos, matches, main_region)
                    print("Clicked Cave OK")
                    time.sleep(1)
                    break
            else:
                time.sleep(1)

        # click(pos, matches, main_region)
        time_to_kill = time.perf_counter() - fight_timer
        
        print(f"Fight took: {int(time_to_kill)}")
        print(f"Fight {fight_count} finished")
        fight_count += 1
        

        print("Pause for 5 seconds\n")
        time.sleep(5)
    print("Saving Screenshot....")
    time.sleep(1)
    
    time.sleep(1)

if __name__ == "__main__":
    main()



  
