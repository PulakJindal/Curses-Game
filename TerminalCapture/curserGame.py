import curses
from curses import wrapper
import time
import random

def gameOver(win, score):
    win.nodelay(False)
    win.clear()
    win.addstr( win.getmaxyx()[0]//2, win.getmaxyx()[1]//2 - 5, "GAME OVER")
    win.addstr( win.getmaxyx()[0]//2 + 1, win.getmaxyx()[1]//2 - 7, f"Final Score: {score}")
    win.getch()
    win.refresh()
    print("Game Over. Final Score:", score)

def main(stdscr):
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
    ey = 1

    win.nodelay(True)

    while True:        
        
        try:
            key = -1
            while True:                # Drain the input buffer
                ch = win.getch()
                if ch == -1:
                    break
                key = ch
            if key == curses.KEY_RIGHT and x < winWidth - 2:
                x += 1
            elif key == curses.KEY_LEFT and x > 1:
                x -= 1
            elif key == curses.KEY_DOWN and y < winHeight - 2:
                y += 1
            elif key == curses.KEY_UP and y > 3:
                y -= 1
            elif key == ord('q'):
                print("Exit...")
                break
        except:
            pass
        
        if x == ex and y == ey+5:
            score += 1
            ey = 1
            ex = random.randint(max(x-10, 1), min(x+10, winWidth-2))
        elif ey < winHeight-6:
            ey += 1
        elif ey == winHeight-6:
            lives -= 1
            if lives == 0:
                gameOver(win, score)
                break
            ey = 1
            ex = random.randint(max(x-15, 1), min(x+15, winWidth-2))        #object appear only near player
        
        
        win.clear()
        win.addstr(1, 1, "Use arrow keys to move 'U'. Press 'q' to quit.")       #instructions
        # win.addstr(2, 1, f"Window Size: {winHeight}x{winWidth}")                 #window size
        # win.addstr(3, 1, f"Position: ({x-1}, {y-5})")                            #current position
        # win.addstr(4, 1, f"E Position: ({ex-1}, {ey})")                          #enemy position
        win.hline(2, 1, curses.ACS_HLINE, winWidth-2)                            #horizontal line below info
        win.addstr(2, winWidth-12, f"Score: {score}")                            #score display
        win.addstr(2, 2, f"Lives: {lives}")                                      #lives display
        win.addstr(y, x, "U")
        win.addstr(5+ey, ex, "O")
        win.border()
        win.refresh()
        
        time.sleep(max(0.02, 0.2-(score*0.005)))  #increase speed as score increases
        
wrapper(main)
    