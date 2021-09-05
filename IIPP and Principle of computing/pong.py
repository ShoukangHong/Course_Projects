# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
rand = 1.8+ 2 *random.random()
ball_vel = [rand, math.sqrt(4.1**2 - rand**2)*random.choice([-1, 1])]
PAD_MV = 4.0
paddle1_vel, paddle2_vel = 0, 0
AI = [False, False]
AIPOS = [HEIGHT/2-HALF_PAD_HEIGHT, HEIGHT/2-HALF_PAD_HEIGHT]
AILv = PAD_MV
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global ball_pos, ball_vel, rand # these are vectors stored as lists
    ball_pos = [WIDTH/2 - BALL_RADIUS, HEIGHT/2 - BALL_RADIUS]
    rand = 1.8+ 2 *random.random()
    ball_vel = [direction * rand, math.sqrt(4.1**2 - rand**2)*random.choice([-1, 1])]
    paddle1_pos, paddle2_pos = ([HALF_PAD_WIDTH,HEIGHT/2 - HALF_PAD_HEIGHT], 
                                [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT])
# define event handlers
def new_game():  # these are numbers
    global score1, score2  # these are ints
    global ball_pos, ball_vel
    score1, score2 = 0, 0
    spawn_ball(random.choice([-1, 1]))
def end_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_pos, ball_vel
    score1, score2 = 0, 0
    paddle1_pos, paddle2_pos = [HALF_PAD_WIDTH,HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle1_vel, paddle2_vel = 0, 0
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0,0]
    AI[0], AI[1] = False, False
def AI1_handler():
    AI[0] = not AI[0]
def AI2_handler():
    AI[1] = not AI[1]
def AI_paddle_vel():
    global paddle1_vel, paddle2_vel
    AI_pos()
    if AI[0]:
        if abs(paddle1_pos[1] - AIPOS[0]) <= AILv:
            paddle1_vel = 0
        elif paddle1_pos[1] < AIPOS[0]:
            paddle1_vel = AILv
        else:
            paddle1_vel = -AILv
    if AI[1]:
        if abs(paddle2_pos[1] - AIPOS[1]) <= AILv:
            paddle2_vel = 0
        elif paddle2_pos[1] < AIPOS[1]:
            paddle2_vel = AILv
        else:
            paddle2_vel = -AILv
def AI_pos():
    global AIPOS
    if ball_vel[0]>0:
        AIPOS[1] = ball_pos[1] - HALF_PAD_HEIGHT
        AIPOS[0] = HEIGHT/2-HALF_PAD_HEIGHT
    else:
        AIPOS[0] = ball_pos[1] - HALF_PAD_HEIGHT
        AIPOS[1] = HEIGHT/2-HALF_PAD_HEIGHT
def AILvUp():
    global AILv
    AILv += 1
    AILv = min(10.0, AILv)
    label.set_text('AI Level ' + str(int(AILv)))
def AILvDown():
    global AILv
    AILv -= 1
    AILv = max(1.0, AILv)
    label.set_text('AI Level ' + str(int(AILv)))
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS-5, 5, 'orange', 'Yellow')    
    # update paddle's vertical position, keep paddle on the screen
    AI_paddle_vel()
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    paddle1_pos[1] = max(min(paddle1_pos[1], HEIGHT-PAD_HEIGHT), 0)
    paddle2_pos[1] = max(min(paddle2_pos[1], HEIGHT-PAD_HEIGHT), 0)
    # draw paddles
    canvas.draw_line(paddle1_pos,[paddle1_pos[0],paddle1_pos[1]+ PAD_HEIGHT], PAD_WIDTH, "Yellow")
    canvas.draw_line(paddle2_pos,[paddle2_pos[0],paddle2_pos[1]+ PAD_HEIGHT], PAD_WIDTH, "Yellow")    
    # determine whether paddle and ball collide    
    if ball_pos[0]+20 >= WIDTH - PAD_WIDTH:
        if paddle2_pos[1]<=ball_pos[1]<=paddle2_pos[1]+ PAD_HEIGHT:
            ball_vel[0] *= -(1+ 0.06*random.random())
            ball_vel[1] *= 0.56+ 1*random.random()
        else:
            score1 +=1
            spawn_ball(-1)
    elif ball_pos[0]-20 <= PAD_WIDTH:
        if paddle1_pos[1]<=ball_pos[1]<=paddle1_pos[1]+ PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 +=1
            spawn_ball(1)
    # draw scores
    canvas.draw_text(str(score1) + '    ' + str(score2), [252,60], 48, 'green')
    if AI[0]:
        canvas.draw_text('AI', [40,30], 30, 'green')
    else:
        canvas.draw_text('Player 1', [40,30], 30, 'green')
    if AI[1]:
        canvas.draw_text('        AI', [465,30], 30, 'green')
    else:
        canvas.draw_text('Player 2', [465,30], 30, 'green')
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -PAD_MV
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = PAD_MV
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -PAD_MV
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = PAD_MV
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('new game', new_game)
frame.add_button('end game', end_game)
frame.add_button('Player 1 use AI', AI1_handler)
frame.add_button('Player 2 use AI', AI2_handler)
frame.add_button('AI Level Up', AILvUp)
frame.add_button('AI Level Down', AILvDown)
label = frame.add_label('AI Level ' + str(int(AILv)))

# start frame
new_game()
frame.start()
