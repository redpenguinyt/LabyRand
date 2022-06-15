import turtle, random, time

labyrinth_cords = []
finish = []
SPEED = 5
GAME_DELAY = 1

def create_player():
	player = turtle.Turtle("classic")
	player.color("blue")
	player.penup()
	player.speed(0)
	reset(player)
	return player

def laby_move(pen, distance, penUp=False):
	if penUp:
		pen.up()
	for _ in range(int(distance/SPEED)):
		pen.forward(SPEED)
		if not penUp: labyrinth_cords.append(pen.position())
	pen.down()

def laby_go(pen, distance, direction, across=False):
	directions = {"up": 90, "left": 180, "down": -90, "right": 0}
	pen.seth(directions[direction])
	for _ in range(int(distance/50)):
		skip = False
		pos = [pen.pos()[0],pen.pos()[1]]
		if random.randint(0,5) == 5:
			skip = True
		if direction == "down" and across:
			pos[0] -= 50
			if tuple(pos) in labyrinth_cords:
				skip = True
		if direction == "right" and across:
			pos[1] += 50
			if tuple(pos) in labyrinth_cords:
				skip = True

		laby_move(pen, 50, skip)

def set_finish(pos):
	finish_range = round(10/SPEED)
	for i in range(-finish_range, finish_range+1):
		for j in range(-finish_range, finish_range+1):
			new_pos = (
				pos[0]+i*SPEED,
				pos[1]+j*SPEED
			)
			finish.append(new_pos)

def draw_labyrinth(screen=None):
	if screen:
		finish[:] = []
		labyrinth_cords[:] = []
		screen.clear()
		screen.reset()

	screen = turtle.Screen()
	screen.setup(500, 500)
	screen.title("LabyRand")
	screen.bgcolor("black")
	screen.tracer(6, 75)

	labypen = turtle.Turtle("square")
	labypen.color("red")
	labypen.speed("fastest")
	labypen.up()
	labypen.goto(0 - screen.window_width()/2-25,screen.window_height()/2+25)
	labypen.down()

	for i in range(0, int(screen.window_width()/50+1)):
		laby_go(labypen, (i)*50, "right")
		laby_go(labypen, screen.window_height(), "down", True)
		labypen.up()
		labypen.goto(0 - screen.window_width()/2-25,screen.window_height()/2+25)
		labypen.down()

	for i in range(0, int(screen.window_height()/50+1)):
		laby_go(labypen, (i)*50, "down")
		laby_go(labypen, screen.window_width(), "right", True)
		labypen.up()
		labypen.goto(0 - screen.window_width()/2-25,screen.window_height()/2+25)
		labypen.down()

	labypen.up()
	def randcords():
		return 5*round( random.randint(0-screen.window_width()/2, screen.window_width()/2) /5)
	labypen.goto(randcords(), randcords())
	labypen.down()

	set_finish(labypen.position())
	labypen.color("lime")
	def restart():
		global player
		player = restart_game(screen)
	screen.onkey(up, "w")
	screen.onkey(lt, "a")
	screen.onkey(dn, "s")
	screen.onkey(rt, "d")
	screen.onkey(restart, "r")
	screen.listen()

	screen.tracer(1,1)

	return screen

def movePlayer():
	global moveVec
	global direction
	player.goto(player.position() + moveVec)
	player.seth(direction)

def outsideBorders(pos):
	if pos[0] > screen.window_width()/2 or pos[0] < 0 - screen.window_width()/2:
		return True
	if pos[1] > screen.window_height()/2 or pos[1] < 0 - screen.window_height()/2 + 10:
		return True

def reset(r_turtle):
	global moveVec
	global direction
	moveVec = (0,0)
	direction = 90
	r_turtle.goto(0,0)

def up():
	global moveVec
	global direction
	if moveVec == (0,-SPEED): return
	moveVec = (0,SPEED)
	direction = 90
def lt():
	global moveVec
	global direction
	if moveVec == (SPEED,0): return
	moveVec = (-SPEED,0)
	direction = 180
def rt():
	global moveVec
	global direction
	if moveVec == (-SPEED,0): return
	moveVec = (SPEED,0)
	direction = 0
def dn():
	global moveVec
	global direction
	if moveVec == (0,SPEED): return
	moveVec = (0,-SPEED)
	direction = 270

def restart_game(screen):
	"""Example:
>>> screen = draw_labyrinth()
>>> player = restart_game(screen)"""
	draw_labyrinth(screen)
	return create_player()

start_screen = turtle.Screen()
start_screen.bgcolor("black")
title = turtle.Turtle("square")
title.color("red")
title.back(110)
title.up()
title.write("LabyRand", font=("Cascadia Code", 32, "normal"))
title.right(90)
title.forward(100)
title.write("WASD to move\nPress R to regenerate a level\nThe game will start in 3 seconds\nYou don't have a choice", font=("Cascadia Code", 20, "normal"))
title.forward(20)

time.sleep(3)

start_screen.clear()

global direction
global moveVec
direction = 90
moveVec = (0,0)

screen = draw_labyrinth()
global player
player = create_player()

while True:
	if player.position() in labyrinth_cords or outsideBorders(player.position()):
		reset(player)
	if player.position() in finish:
		player.write("You win!", align="center", font=("Cascadia Code", 20, "normal"))
		time.sleep(2)
		player = restart_game(screen)
		continue
	movePlayer()
	time.sleep(GAME_DELAY / 100)