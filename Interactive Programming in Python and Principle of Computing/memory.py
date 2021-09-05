# implementation of card game - Memory

import random
import simplegui
# helper function to initialize globals
def new_game():
    global upList, cards, turns, end
    upList, turns, end = [-1, -1], 0, False
    cards = range(8)+range(8)
    random.shuffle(cards)

# define event handlers
def pos_to_idx(pos):
    idx = pos[0]//50 + 8*(pos[1]//100)
    if cards[idx] < 0:
        return -1
    return idx

def mouseclick(pos):
    global upList, turns, end
    idx = pos[0]//50 + 8*(pos[1]//100)
    state = sum([1 for n in upList if n>=0])
    if pos[1]>200 or cards[idx]<0 or (idx in upList and state < 2):
        return
    if state == 2:
        state, upList = 0, [-1, -1]
    elif state == 1:
        turns += 1
        label.set_text("Turns = " + str(turns))
    upList[state] = idx
    if not (-1 in upList) and cards[upList[0]] == cards[upList[1]]:
        cards[upList[0]],cards[upList[1]] = -cards[upList[0]]-1, -cards[upList[0]]-1
        upList = [-1, -1]
    if len([n for n in cards if n >=0]) == 0:
        end = True

# cards are logically 50x100 pixels in size    
def draw(canvas):
    canvas.draw_text('turn: '+str(turns), [300, 290], 30, 'white')
    if end:
        canvas.draw_text('You Win!', [116, 260], 50, 'red')
    for i, card in enumerate(cards):
        y = 100*(i//8)
        x = 50* (i%8)
        if card >= 0 and not(i in upList):
            canvas.draw_polygon([[3+x,3+y], [3+x, 97+y], [47+x, 97+y], [47+x, 3+y]], 4, 'Yellow', 'Orange')
        elif card < 0:
            canvas.draw_polygon([[3+x,3+y], [3+x, 97+y], [47+x, 97+y], [47+x, 3+y]], 4, 'white', 'white')
            canvas. draw_text(str(abs(card+1)), [16+x, 64+y], 36, 'black')
        else:
            canvas.draw_polygon([[3+x,3+y], [3+x, 97+y], [47+x, 97+y], [47+x, 3+y]], 4, 'white', 'white')
            canvas. draw_text(str(abs(card)), [16+x, 64+y], 36, 'red')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 400, 300)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric