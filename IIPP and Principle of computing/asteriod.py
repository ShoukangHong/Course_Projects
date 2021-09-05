# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
ANGLE_VEL = 0.06
FONT_SIZE = 36
SIZE =[800, 600]
score = 0
lives = 3
time = 0
started = False
rocks = []
missiles = set()
explosions = set()
message = ''

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 30) # original radius 35
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
titlesound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
soundtrack.set_volume(0.5)
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group,canvas):
    for obj in list(group):  
        obj.draw(canvas)
        obj.update()
        if obj.lifespan <= 0:
            group.remove(obj)
            
def group_collide(group, other):
    for obj in list(group):
        if obj.collide(other):
            explosions.add(Sprite(other.pos, other.vel,
                other.angle, 0, explosion_image, explosion_info))
            group.remove(obj)
            return True
        
def group_group_collide(group1, group2):
    for obj in list(group2):
        if group_collide(group1, obj):
            group2.remove(obj)
            return True
    return False

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.keep_shoot = False
        self.timer = 0
    def shoot(self):
        global missiles
        vector = angle_to_vector(self.angle)
        pos = [self.pos[0] + vector[0] * self.radius, self.pos[1] + vector[1] * self.radius]
        vel = [vector[0]*4 + self.vel[0],vector[1]*4 + self.vel[1]]
        missiles.add( Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound))
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    def update(self):
        vector = angle_to_vector(self.angle)
        if self.keep_shoot:
            self.timer = (self.timer+1) % 15
            if self.timer == 0:
                self.shoot()
        for i in range(len(self.vel)):
            if self.thrust:
                self.vel[i] = (self.vel[i] + vector[i]*0.16)
            self.vel[i] *= 0.98
            self.pos[i] = (self.pos[i] + self.vel[i]) % SIZE[i]
        self.angle += self.angle_vel
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            self.age += 1 
            center = [self.image_center[0] + self.age*self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    def collide(self, obj):
        return self.radius + obj.radius > dist(self.pos, obj.pos)
    def update(self):
        for i in range(len(self.vel)):
            self.pos[i] = (self.pos[i] + self.vel[i]) % SIZE[i]
        self.angle += self.angle_vel
        self.lifespan -= 0.4

def end_game():
    global time, lives, score, started, rocks, missiles, my_ship, message
    message = 'Your Score: ' + str(score)
    started = False
    ship_thrust_sound.rewind()
    rocks = []
    my_ship.thrust = False
    my_ship.keep_shoot = False
    my_ship.image_center[0] = abs(my_ship.image_center[0] - my_ship.image_size[0])
    
def start_game():
    global time, lives, score, started, rocks, missiles, my_ship, message
    message = ''
    started = True
    time = 0
    lives = 3
    score = 0
    rocks = []
    missiles = set()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    ship_thrust_sound.rewind()
    soundtrack.rewind()
    soundtrack.play()
    titlesound.rewind()
    
def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw ship and sprites
    my_ship.draw(canvas)
    if group_collide(rocks, my_ship):
        lives -= 1
        explosion_sound.rewind()
        explosion_sound.play()
        if lives <= 0:
            end_game()
    if group_group_collide(missiles, rocks):
        score += 1
        explosion_sound.rewind()
        explosion_sound.play()
    process_sprite_group(rocks, canvas)
    process_sprite_group(missiles,canvas)
    process_sprite_group(explosions, canvas)
    canvas.draw_text('Score: ' + str(score), [WIDTH -180, FONT_SIZE], FONT_SIZE, 'green')
    canvas.draw_text('Lives: ' + str(lives), [20, FONT_SIZE], FONT_SIZE, 'red')
    my_ship.update()
    # update ship and sprites
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        canvas.draw_text(message, (WIDTH/2 - 10*len(message), HEIGHT - 48), 48, 'Red')

def rock_spawner():
    global rocks
    i= min(10, 2+ (time//600))
    if not started:
        return None
    pos = [random.random()*WIDTH, random.random()*HEIGHT]
    if dist(pos, my_ship.pos) > 2*asteroid_info.get_radius() + my_ship.radius:
        rocks.append(Sprite(pos, [i*random.random()-i/2, i*random.random()-i/2],
                3*random.random(), random.choice([-1,1])*ANGLE_VEL, asteroid_image, asteroid_info))
    if len(rocks) > 12:
        rocks.pop(0)       
def key_down(key):
    if not started:
        return
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        ship_thrust_sound.play()
        my_ship.image_center[0]+= my_ship.image_size[0]
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel += ANGLE_VEL
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel -= ANGLE_VEL
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        my_ship.keep_shoot = True
        my_ship.timer = 0
def key_up(key):
    if not started:
        return
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        ship_thrust_sound.rewind()
        my_ship.image_center[0]-= my_ship.image_size[0]
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel -= ANGLE_VEL
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel += ANGLE_VEL
    elif key == simplegui.KEY_MAP['space']:
        my_ship.keep_shoot = False     
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        start_game()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)
rock_spawner()

# get things rolling
timer.start()
frame.start()
titlesound.play()