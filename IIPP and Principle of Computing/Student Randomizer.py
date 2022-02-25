import random
import simplegui
students = '''
A, A
B, B
C, C
D, D
E, E
F, F
G, G
H, H
I, I
J, J
K, K
L, L
M, M
N, N
O, O
P, P
Q, Q
R, R
S, S
T, T
U, U
V, V
W, W
X, X
Y, Y
Z, Z'''

students = students.strip().split('\n')
for i in range(len(students)):
    students[i] = students[i].strip()
    
groupSize = 4
largerGroup = False
gList = []
font = 30
width = 1280
height = 800

def randomize():
    global gList, groupSize, largerGroup
    gList = []
    random.shuffle(students)
    num = (len(students)//groupSize)
    if len(students)%groupSize > 0 and not largerGroup:
        num += 1
    average = len(students)/num
    idx = 0
    for i, student in enumerate(students):
        if i + 1 > idx * average:
            idx += 1
            gList.append([])
            gList[-1].append('Group ' + str(idx))
        gList[-1].append(student)
    for group in gList:
        for text in group:
            print(text)

def fontSizeUp():
    global font
    font += 2
    
def fontSizeDown():
    global font
    if font > 10:
        font -= 2

def groupSizeUp():
    global groupSize
    if groupSize < len(students):
        groupSize += 1
    
def groupSizeDown():
    global groupSize
    if groupSize > 2:
        groupSize -= 1
        
def changeAdjustMode():
    global largerGroup
    largerGroup = not largerGroup
# Handler to draw on canvas
def draw(canvas):
    txt = "Group Size: " + str(groupSize) + "    "
    txt += "Allow Larger Group" if largerGroup else "Allow Smaller Group"
    canvas.draw_text(txt, [font,font*(1)*1.2], font*3//4, "Green")
    if not gList:
        row1 = [''] + students[:len(students)//2]
        row2 = [''] + students[len(students)//2:]
    else:
        row1 = []
        row2 = []
        for group in gList[:len(gList)//2]:
            row1 += group + ['']
        for group in gList[len(gList)//2:]:	
            row2 += group + ['']
    drawRow(canvas, row1, 0)
    drawRow(canvas, row2, 1)
    
def drawRow(canvas, texts, i):
    for j, text in enumerate(texts):
        color = "Yellow" if "Group" in text else "White"
        canvas.draw_text(text, [i * width//2 + font,font*(j+2)*1.2], font, color)
        
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", width, height)
frame.add_button("Randomize", randomize)
frame.add_label("Group Control:")
frame.add_button("Group Size Up", groupSizeUp)
frame.add_button("Group Size Down", groupSizeDown)
frame.add_button("Change Adjust Mode", changeAdjustMode)
frame.add_label("Display Control:")
frame.add_button("Font Size Up", fontSizeUp)
frame.add_button("Font Size Down", fontSizeDown)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
