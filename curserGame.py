import curses
from curses import wrapper
import time
import random
import argparse


#================Game Over Function================
def gameOver(win, score):
    win.nodelay(False)
    win.clear()
    win.addstr( win.getmaxyx()[0]//2, win.getmaxyx()[1]//2 - 5, "GAME OVER")
    win.addstr( win.getmaxyx()[0]//2 + 1, win.getmaxyx()[1]//2 - 7, f"Final Score: {score}")
    win.addstr( win.getmaxyx()[0]//2 + 3, win.getmaxyx()[1]//2 - 9, "Press Enter to exit")
    key = win.getch()
    while key not in [10, 13, curses.KEY_ENTER]:
        key = win.getch()
        win.refresh()
    print("Game Over. Final Score:", score)


#================Catch the Fruit Game================
def catchTheFruit(stdscr):
    score = 0
    lives = 3
    
    stdscr.clear()
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()
    
    winWidth = int(width * 0.4)
    winHeight = height
    
    win = curses.newwin(winHeight, winWidth, 0, int(width*0.3))
    
    win.keypad(True)        #allows to get keys like arrows
    win.border()            #draw border around window
    
    x, y = winWidth//2, winHeight//2
    win.addstr(y, x, "X")
    
    ex = int(width*0.3)+1
    ey = 2

    win.nodelay(True)
    
    drop = []
    ex = random.randint(1, winWidth-2)
    drop.append({"x" : ex, "y" : ey})   #new drop at random position
    spawnTimer = 0
    
    PLAYER_INTERVAL = 0.03                            #player movement speed
    ENEMY_INTERVAL = max(0.05, 0.15 - score * 0.005)     #enemy movement speed

    last_player_update = time.time()                    #last player update time
    last_enemy_update = time.time()                     #last enemy update time

    while True:        
        now = time.time()
        
        if now - last_player_update > PLAYER_INTERVAL:      #player movement update
            key = -1
            while True:                # Drain the input buffer
                ch = win.getch()
                if ch == -1:
                    break
                key = ch
            if (key == curses.KEY_RIGHT or key == ord('6')) and x < winWidth - 2:
                x += 1
            elif (key == curses.KEY_LEFT or key == ord('4')) and x > 1:
                x -= 1
            elif (key == curses.KEY_DOWN or key == ord('2')) and y < winHeight - 2:
                y += 1
            elif (key == curses.KEY_UP or key == ord('8')) and y > 3:
                y -= 1
            elif key == ord('q'):
                print("Exit...")
                break
            last_player_update = now                         #update last player movement time
        
        if now - last_enemy_update > ENEMY_INTERVAL:         #enemy movement update
            spawnTimer += 1
            if spawnTimer >= max(0, 20-(0.1*score)):
                spawnTimer = 0
                distanceFromPlayer = 5+(score*0.1)
                ex = random.randint(int(max(x-distanceFromPlayer, 1)), int(min(x+distanceFromPlayer, winWidth-2)))
                drop.append({"x" : ex, "y" : ey})   #new drop at random position
                
            new_drop = []
            for d in drop:
                d["y"] += 1
                
                if d["x"] == x and d["y"] == y:
                    score += 1
                    continue
                
                if d["y"] >= winHeight - 1:
                    lives -= 1
                    if lives == 0:
                        gameOver(win, score)
                        return
                    else:
                        continue
                new_drop.append(d)
            drop = new_drop
            last_enemy_update = now                           #update last enemy movement time
        
        win.clear()
        win.addstr(1, 1, "Use arrow keys to move 'U'. Press 'q' to quit.")       #instructions
        # win.addstr(2, 1, f"Window Size: {winHeight}x{winWidth}")                 #window size
        # win.addstr(3, 1, f"Position: ({x-1}, {y-5})")                            #current position
        # win.addstr(4, 1, f"E Position: ({ex-1}, {ey})")                          #enemy position
        win.hline(2, 1, curses.ACS_HLINE, winWidth-2)                            #horizontal line below info
        win.addstr(2, winWidth-12, f"Score: {score}")                            #score display
        win.addstr(2, 2, f"Lives: {lives}")                                      #lives display
        win.addstr(y, x, "U")
        for d in drop:
            win.addstr(d["y"], d["x"], "O")
        win.border()
        win.refresh()
        
        # time.sleep(0.01)


#================Dodge the Enemy Game================
def spaceFight(stdscr):
    score = 0
    lives = 3
    
    stdscr.clear()
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()
    
    winWidth = int(width * 0.3)
    winHeight = height
    
    win = curses.newwin(winHeight, winWidth, 0, int(width*0.35))
    
    win.keypad(True)        #allows to get keys like arrows
    win.border()            #draw border around window
    
    x, y = winWidth//2, winHeight//2
    
    ex = int(width*0.3)+1
    ey = 2

    win.nodelay(True)
    
    drop = []
    ex = random.randint(1, winWidth-2)  #new drop at random position
    drop.append({"x" : ex, "y" : ey})   
    spawnTimer = 0

    PLAYER_INTERVAL = 0.03
    ENEMY_INTERVAL = max(0.00, 0.15 - score * 0.01)

    last_player_update = time.time()
    last_enemy_update = time.time()
    
    while True:        
        
        now = time.time()
        
        if now - last_player_update > PLAYER_INTERVAL:
            key = -1
            while True:                # Drain the input buffer
                ch = win.getch()
                if ch == -1:
                    break
                key = ch
            if (key == curses.KEY_RIGHT or key == ord('6')) and x < winWidth - 2:
                x += 1
            elif (key == curses.KEY_LEFT or key == ord('4')) and x > 1:
                x -= 1
            elif (key == curses.KEY_DOWN or key == ord('2')) and y < winHeight - 2:
                y += 1
            elif (key == curses.KEY_UP or key == ord('8')) and y > 3:
                y -= 1
            elif key == ord('q'):
                print("Exit...")
                break
            last_player_update = now
        
        if now - last_enemy_update > ENEMY_INTERVAL:
            spawnTimer += 1
            if spawnTimer >= max(0, 20-(0.1*score)):
                spawnTimer = 0
                ex = random.randint(int(max(x-15, 2)), int(min(x+15, winWidth-3)))
                drop.append({"x" : ex, "y" : ey})   #new drop at random position
                    
            new_drop = []
            for d in drop:
                d["y"] += 1
                
                xv = d["x"]
                if (xv == x or x == xv+2 or x == xv+1) and d["y"] == y:
                    lives -= 1
                    if lives == 0:
                        gameOver(win, score)
                        return
                    continue
                
                if d["y"] >= winHeight - 1:
                    score += 1
                    continue
                    
                new_drop.append(d)
            drop = new_drop
            last_enemy_update = now
        
        win.clear()
        win.addstr(1, 1, "Use arrow keys to move 'A'. Press 'q' to quit.")       #instructions
        # win.addstr(2, 1, f"Window Size: {winHeight}x{winWidth}")                 #window size
        # win.addstr(3, 1, f"Position: ({x-1}, {y-5})")                            #current position
        # win.addstr(4, 1, f"E Position: ({ex-1}, {ey})")                          #enemy position
        win.hline(2, 1, curses.ACS_HLINE, winWidth-2)                            #horizontal line below info
        win.addstr(2, winWidth-12, f"Score: {score}")                            #score display
        win.addstr(2, 2, f"Lives: {lives}")                                      #lives display
        win.addstr(y, x, "A")
        for d in drop:
            win.addstr(d["y"], d["x"], "OOO")
        win.border()
        win.refresh()
        
def main(stdscr):
    
    parser = argparse.ArgumentParser(
        prog = "curserGame.py",
        description="Terminal Games"
        )
    
    parser.add_argument(
        "-g", "--gameNumber",
        default=1,
        help="Select the game to play: 1 for Catch the Fruit, 2 for Space Fight",
        type=int,
        choices=[1, 2]
        )
    
    if parser.parse_args().gameNumber == 2:
        spaceFight(stdscr)
    else:
        catchTheFruit(stdscr)
        
wrapper(main)
    