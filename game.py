import turtle
import random
import time
import winsound

from sympy import Q


#sets screen size variables
width = 800
height = 400
cursor_size = 20

#turns off animation speed, creates blue background
turtle.tracer(0,0)
screen = turtle.Screen()
screen.title('Cross Country Slopes')
screen.setup(width, height)
screen.bgcolor('#2E5984')

#creates snow ground
background = turtle.Turtle('square', visible=False)
background.shapesize(height/2 / cursor_size, width / cursor_size)
background.penup()
background.sety(-height/4)
background.color('#D3D3D3')
background.stamp()


#creates player, starting with custom shapes
snowboarder = ((-5, 5), (-5, 30), (-10, 30), (-10, 50), (10, 50), (10, 30), (5, 30), (5, 5), (30, 5), (30, 0), (-20, 0), (-20, 5))
turtle.register_shape('snowboarder', snowboarder)
snowboarder = ((-5, 5), (10, 20), (5, 25), (20, 40), (35, 25), (20, 10), (15, 15), (5, 5), (30, 5), (30, 0), (-20, 0), (-20, 5))
turtle.register_shape('ducking_snowboarder', snowboarder)

player = turtle.Turtle()
player.color("black")
player.shape("snowboarder")
player.tilt(90)
player.penup()
player.speed(0)
player.setposition(-250, 15)

#creates rock list for rocks to be placed when generated, adds ability to create rocks
rocks = []
class Rock_Generator():
    def create_rock():
        rock = turtle.Turtle()
        rock.color("grey")
        rock.shape("circle")
        rock.penup()
        rock.speed(0)
        rock.setposition(400, 5)
        rocks.append(rock)
        return rocks

#creates treetops
treetops = []
class Treetop_Generator():
    #turtle object
    shape = ((0, 100), (25, 75), (10, 75), (25, 60), (10, 60), (25, 45), 
            (-25, 45), (-10, 60), (-25, 60), (-10, 75), (-25, 75))
    #registering the new shape
    turtle.register_shape('treetop', shape)
    def create_tree():
        treetop = turtle.Turtle()
        treetop.color("green")
        treetop.shape('treetop')
        treetop.tilt(90)
        treetop.penup()
        treetop.speed(0)
        treetop.setposition(400, -5)
        treetops.append(treetop)
        return treetops

# creates treetrunks
treetrunks = []
class Treetrunk_Generator():
    #turtle object
    shape = ((-8, 40), (8, 40), (8, 0), (-8, 0))
    #registering the new shape
    turtle.register_shape('treetrunk', shape)
    def create_trunk():
        treetrunk = turtle.Turtle()
        treetrunk.color("#775d42")
        treetrunk.shape('treetrunk')
        treetrunk.tilt(90)
        treetrunk.penup()
        treetrunk.speed(0)
        treetrunk.setposition(400, 0)
        treetrunks.append(treetrunk)
        return treetrunks

#set health percent
global health
health = 100

#draw health percent
health_pen = turtle.Turtle()
health_pen.speed(0)
health_pen.color("white")
health_pen.penup()
health_pen.setposition(-390, 180)
health_pen.write(f'Health: {health}%', False, align = "left", font = ("Arial", 10, "normal"))
health_pen.hideturtle()

#set score
score = 0

#draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(330, 180)
score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))
score_pen.hideturtle()

#placeholder jump height, and obstacle speed, called player speed since it is as if the player is moving
#don't change these
vertical_speed = 0
generator_reset_number = 0
damage = 0
high_scores = [0]
#change these
player_speed = 8
obstacle_delay = 25
speedup_rate = 0.5


#function for playing music
def play_background_music(sound_file, time = 0):
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    if time > 0:
        turtle.ontimer(lambda: play_background_music(sound_file, time), t = int(time * 1000))
#duration of the music selected
length_of_wav_file = 58

#playing music
play_background_music("Snowboarder-Game/RockInstrumental.wav", length_of_wav_file)

# jump function sets the vertical velocity
def jump():
    if player.ycor() == 0:
        global vertical_speed
        vertical_speed = 60

def duck():
    if player.shape() == 'snowboarder':
        player.shape('ducking_snowboarder')

def stand():
    if player.shape() == 'ducking_snowboarder':
        player.shape('snowboarder')

def restore():
    global player_speed
    player_speed = 8
    global score
    score = 0
    score_pen.clear()
    score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))
    global health
    health = 100
    health_pen.clear()
    health_pen.write(f'Health: {health}%', False, align = "left", font = ("Arial", 10, "normal")) 
    global generator_reset_number
    generator_reset_number = obstacle_delay

#listens for the space key to be pressed
screen.onkeypress(jump, 'space')
screen.onkeypress(duck, 'z')
screen.onkeyrelease(stand, 'z')
screen.onkeypress(restore, 'r')
screen.listen()

#use health pen to write intro
health_pen.color('black')
health_pen.setposition(0, 25)
health_pen.write(f'Cross Country Slopes', False, align = "center", font = ("Arial", 40, "italic"))
health_pen.setposition(0, -30)
health_pen.write(f'Game will start shortly', False, align = "center", font = ("Arial", 15, "normal"))
health_pen.setposition(0, -70)
health_pen.write(f'Z = Duck     Space = Jump', False, align = "center", font = ("Arial", 12, "normal"))

# reset to health position
time.sleep(3)
health_pen.color("white")
health_pen.setposition(-390, 180)
health_pen.clear()
health_pen.write(f'Health: {health}%', False, align = "left", font = ("Arial", 10, "normal"))
            

#runs the game
while True:
    time.sleep(0.01)
    #changes player position based on vertical velocity and gravity
    player_y = player.ycor()
    if vertical_speed > 0 or player_y > 0:
        player.sety(player_y + vertical_speed/5)
        vertical_speed += -5

    #randomly generated rocks and trees, wih delay between obstacles
    randnum = random.randint(1, 10)
    if generator_reset_number > 0:
        generator_reset_number += -1
    else:
        if randnum == 1:
            Treetrunk_Generator.create_trunk()
            Treetop_Generator.create_tree()
            generator_reset_number = obstacle_delay
        elif randnum == 2:
            Rock_Generator.create_rock()
            generator_reset_number = obstacle_delay

    #changes all rock positions, removes rocks at the end
    for rock in rocks:
        rock_x = rock.xcor()
        rock_y = rock.ycor()
        rock.setx(rock_x - player_speed)
        if rock_x <= -400:
            score += 1
            score_pen.clear()
            score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))
        #deletes rockturtles at he end
        if rock_x <= -400:
            rocks.remove(rock)
            rock.hideturtle()
        
        #rock collisions
        if (rock_x - 10 < player.xcor() < rock_x + 10 and
            rock_y - 10 < player.ycor() < rock_y + 10 and
            damage == 0):
            player_speed = 3
            damage = 10
            health += -25
            # change health
            health_pen.clear()
            health_pen.write(f'Health: {health}%', False, align = "left", font = ("Arial", 10, "normal"))
            #change score
            score += -1
            # score_pen.clear()
            # score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))


    # slows the player down if they recently took damage
    if damage > 0:
        damage += -0.5
        player_speed += 0.25


    #changes all tree & trunk positions, removes trees at the end
    for trunk in treetrunks:
        trunk_x = trunk.xcor()
        trunk.setx(trunk_x - player_speed)
        #remove trunkturtles at the end
        if trunk_x <= -400:
            treetrunks.remove(trunk)
            trunk.hideturtle()

    for treetop in treetops:
        treetop_x = treetop.xcor()
        treetop_y = treetop.ycor()
        treetop.setx(treetop_x - player_speed)
        #increase score
        if treetop_x <= -400:
            score += 1
            score_pen.clear()
            score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))
        
        #checks for collisions with treetops
        if ((player.shape() == 'snowboarder' and
             treetop_x - 10 < player.xcor() < treetop_x + 10 and
             damage == 0) or 
            (player.shape() =='ducking_snowboarder' and
             treetop_x - 10 < player.xcor() < treetop_x + 10 and
             player.ycor() > 30 and
             damage == 0)):
            player_speed = 3
            damage = 10
            # change health
            health += -25
            health_pen.clear()
            health_pen.write(f'Health: {health}%', False, align = "left", font = ("Arial", 10, "normal"))
            #change score
            score += -1
            score_pen.clear()
            score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))

        #remove treeturtles at the end
        if treetop_x <= -400:
            treetops.remove(treetop)
            treetop.hideturtle()
    
    #writes game over
    if health <= 0 and generator_reset_number < 100:
        health_pen.color('black')
        health_pen.setposition(0, 25)
        health_pen.write(f'GAME OVER', False, align = "center", font = ("Arial", 50, "bold"))
        health_pen.setposition(0, -30)
        health_pen.write(f'Press R to restart', False, align = "center", font = ("Arial", 15, "bold"))

        #removes obstacles, corrects score
        generator_reset_number = 10000
        for i in range(3):
            for rock in rocks:
                if -400 < rock.xcor() < -290:
                    score += 1
                rock.setx(-400)
                rock.hideturtle()
                rocks.remove(rock)
            for trunk in treetrunks:
                trunk.setx(-400)
                trunk.hideturtle()
                treetrunks.remove(trunk)
            for treetop in treetops:
                if -400 < treetop.xcor() < -290:
                    score += 1
                treetop.setx(-400)
                treetop.hideturtle()
                treetops.remove(treetop)
        
        #high score system
        if score < 0:
            score = 0
        score_pen.clear()
        score_pen.write(f'Score: {score}', False, align = 'left', font = ("Arial", 10, "normal"))     
        high_scores.append(score)
        health_pen.setposition(0, -50)
        health_pen.write(f'High Score: {max(high_scores)}', False, align = "center", font = ("Arial", 12, "bold"))
        health_pen.color("white")
        health_pen.setposition(-390, 180)
            


    #updates the screen to show new turtle positions
    turtle.update()
    player_speed += speedup_rate/100


