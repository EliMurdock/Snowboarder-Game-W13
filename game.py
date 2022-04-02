import turtle
import random
import time


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


#creates player
player = turtle.Turtle()
player.color("black")
player.shape("square")
player.penup()
player.speed(0)
player.setposition(-210, 25)

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

#placeholder jump height, and obstacle speed, called player speed since it is as if the player is moving
#don't change these
vertical_speed = 0
reset_number = 0
#change these
player_speed = 8
obstacle_delay = 20
speedup_rate = 0.5


# jump function sets the vertical velocity
def jump():
    if player.ycor() == 10:
        global vertical_speed
        vertical_speed = 60

#listens for the space key to be pressed
screen.onkeypress(jump, 'space')
screen.listen()

#runs the game
while True:
    time.sleep(0.02)
    #changes player position based on vertical velocity and gravity
    player_y = player.ycor()
    if vertical_speed > 0 or player_y > 10:
        player.sety(player_y + vertical_speed/5)
        vertical_speed += -5

    #randomly generated rocks and trees, wih delay between obstacles
    randnum = random.randint(1, 10)
    if reset_number > 0:
        reset_number += -1
    else:
        if randnum == 1:
            Treetrunk_Generator.create_trunk()
            Treetop_Generator.create_tree()
            reset_number = obstacle_delay
        elif randnum == 2:
            Rock_Generator.create_rock()
            reset_number = obstacle_delay

    #changes all rock positions, removes rocks at the end
    for rock in rocks:
        rock_x = rock.xcor()
        rock.setx(rock_x - player_speed)
        if rock_x <= -400:
            rocks.remove(rock)

    #changes all tree & trunk positions, removes trees at the end
    for trunk in treetrunks:
        trunk_x = trunk.xcor()
        trunk.setx(trunk_x - player_speed)
        if trunk_x <= -400:
            treetrunks.remove(trunk)
    for treetop in treetops:
        treetop_x = treetop.xcor()
        treetop.setx(treetop_x - player_speed)
        if treetop_x <= -400:
            treetops.remove(treetop)
        
    #updates the screen to show new turtle positions
    turtle.update()
    player_speed += speedup_rate/100


