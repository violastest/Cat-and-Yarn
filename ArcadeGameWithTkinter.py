# Viola Dube
# Cat and Yarn Arcade Game


from tkinter import *

import random

#variables
move_direction = 0
yarn_list = [] # list containing all yarn generated, empty at start
yarn_speed = 2 # initial speed of falling yarn
yarn_color_list = ['red', 'yellow', 'blue', 'green', 'purple', 'brown', 'pink']

#functions

# function to generate yarn balls at random places with random color
def generate_yarn():
    # pick a random x position
    xPosition = random.randint(1, 400)

    #pick a random color
    yarn_color = random.choice(yarn_color_list)

    #create a yarn ball of size 30 at random position and color           
    yarn = canvas.create_oval(xPosition, 0, xPosition +30, 30, fill = yarn_color)

    #add yarn to list
    yarn_list.append(yarn)
    
    #schedule this function to generate more yarn
    window.after(1000, generate_yarn)

# function to move yarn downwards, and schedules call to move_yarn
def move_yarn():
    #loop through list of yarn and change y position
    for yarn in yarn_list:
        canvas.move(yarn, 0, yarn_speed)
        # check if end of screen - restart at random position
        if (canvas.coords(yarn)[1] > 400):
            # end game but after user can see score
            window.after(5000, end_game_over)
            #do not check any more yarn, window to be destroyed
            return
    #schedule this function to move yarn down again
    window.after(50, move_yarn)

# function updates score, level yarn speed
def update_score_level():
    #use of global since variables are changed
    global score, level, yarn_speed
    score = score + 1
    score_display.config(text = "Score:" + str(score))
    #determine if level needs to change
    #update level and yarn_speed
    if score > 5 and score <= 10 :
        yarn_speed = yarn_speed +1
        level = 2
        level_display.config(text="Level: " + str(level))
    elif score > 10:
        yarn_speed = yarn_speed +1
        level = 3
        level_display.config(text="Level: " + str(level))

# function to check distance between 2 objects - return true if they touch
def collision(item1, item2, distance):
    xDistance = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    yDistance = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap = xDistance < distance and yDistance < distance
    return overlap

# function checks if character hits yarn, remove from screen, list, update score
def check_hits():
    # check if hit yarn
    for yarn in yarn_list:
        if collision(myCat, yarn, 30):
            canvas.delete(yarn) # remove from canvas
            #find where in list and remove and update score
            yarn_list.remove(yarn)
            update_score_level()
                
    #schedule check hits again
    window.after(100, check_hits)

# function handles when user first pressses arrow keys
def check_input(event):
    global move_direction
    key = event.keysym
    if key == "Right":
        move_direction = "Right"
    elif key == "Left":
        move_direction = "Left"


#function handles when user stops pressing arrow keys
def end_input(event):
    global move_direction
    move_direction = "None"

    
# function checks if not on edge and updates x coordinatesbased on right\left
def move_cat():
    if move_direction == "Right" and canvas.coords(myCat)[0] < 400:
        canvas.move(myCat, 10, 0)
    if move_direction == "Left" and canvas.coords(myCat)[0] > 0:
        canvas.move(myCat, -10, 0)
    window.after(16, move_cat) # move the cat at 60 frames per second

# function called to end game - destroys window
def end_game_over():
    window.destroy()

# function to clear the instructions on the screen
def end_title():
    canvas.delete(title) # remove title
    canvas.delete(directions) # remove directions


#make a window
window = Tk()
window.title("Cat and Yarn Game")

#create a canvas to put objects on the screen
canvas = Canvas(window, width=400, height=400, bg='white')
canvas.pack()

#set up welcome screen with title and directions
title = canvas.create_text(200,200, text = 'Cat and Yarn', fill = 'black', \
    font = ("Helvetica", 30))
directions = canvas.create_text(200, 380, \
    text ="Collect yarn balls, don't let them touch the ground", \
    fill='black', font = ('Helvetica', 10))

#set up score display using label widget
score = 0
score_display = Label(window, text="Score: " + str(score))
score_display.pack()

#set up level display using label widget
level =1
level_display = Label(window, text="Level: " + str(level))
level_display.pack()

#create an image object using the cat gif file
player_image = PhotoImage(file="cat.gif")
#use image object to create a character at position
myCat = canvas.create_image(200, 300, image = player_image)


# start game loop by scheduling all the functions
window.after(1000, end_title)       # clear title and instructions
window.after(1000,generate_yarn)    # start making yarn balls
window.after(1000, move_yarn)       # start moving yarn
window.after(1000,check_hits)       # check if cat hit a yarn ball
window.after(1000,move_cat)         # handle keyboard controls

# bind the keys to the cat
canvas.bind_all('<KeyPress>', check_input) # bind key press
canvas.bind_all('<KeyRelease>', end_input) # bind all keys to circle

window.mainloop() #last line GUI main event loop
