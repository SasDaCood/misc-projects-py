# osu! clickspeed measurer - By SasDaGreat

# Known bugs:
# - sometimes, a score doesn't submit to the leaderboards if the cps is the same as another cps. Will look into this further.
# - inputting \ at the end of the name to be submitted into the highscores list crashes the game because formatting sux.
# - there's this huge dangerous-looking fly-like abomination whizzing around this room rn and i dont know if i should be scared or not

import turtle,configparser
from time import time,sleep
#from winsound import PlaySound,SND_ASYNC

def initialiseLoopRedirect(): initialiseLoop(0,0)
def bye(x,y):
    turtle.bye()
    exit()

def highscores():
    turtle.onkey(None,"h")
    text.clear()
    
    text.goto(-240,200)
    text.color("red")
    text.write("    Name",align="left",font=("Calibri",20,"bold"))
    text.goto(240,200)
    text.color("blue")
    text.write("Clicks per second",align="right",font=("Calibri",20,"bold"))

    text.goto(-270,-60)
    text.color("#303030")
    text.write("1st\n2nd\n3rd\n4th\n5th\n6th\n7th\n8th\n9th\n10th",align="left",font=("Calibri",15))
    text.color("black")
    text.setx(-215)
    text.write("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}".format((eval(config["DEFAULT"]["{}".format(1)])[1]),(eval(config["DEFAULT"]["{}".format(2)])[1]),(eval(config["DEFAULT"]["{}".format(3)])[1]),(eval(config["DEFAULT"]["{}".format(4)])[1]),(eval(config["DEFAULT"]["{}".format(5)])[1]),(eval(config["DEFAULT"]["{}".format(6)])[1]),(eval(config["DEFAULT"]["{}".format(7)])[1]),(eval(config["DEFAULT"]["{}".format(8)])[1]),(eval(config["DEFAULT"]["{}".format(9)])[1]),(eval(config["DEFAULT"]["{}".format(10)])[1])),align="left",font=("Calibri",15))
    text.color("powderblue")
    text.setx(240)
    text.write("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}".format((eval(config["DEFAULT"]["{}".format(1)])[0]),(eval(config["DEFAULT"]["{}".format(2)])[0]),(eval(config["DEFAULT"]["{}".format(3)])[0]),(eval(config["DEFAULT"]["{}".format(4)])[0]),(eval(config["DEFAULT"]["{}".format(5)])[0]),(eval(config["DEFAULT"]["{}".format(6)])[0]),(eval(config["DEFAULT"]["{}".format(7)])[0]),(eval(config["DEFAULT"]["{}".format(8)])[0]),(eval(config["DEFAULT"]["{}".format(9)])[0]),(eval(config["DEFAULT"]["{}".format(10)])[0])),align="right",font=("Calibri",15))

    text.color("black")
    text.goto(0,-250)
    text.write("'None' means the slot is empty. Perhaps you could fill in the gap?\nClick anywhere to exit, or press R to retry your hand at getting a highscore!\nJust don't get repetitive strain injury :p",align="center",font=("Calibri",13,"bold"))


def exitLoop():
    button.onclick(None)
    turtle.onkey(None,"z")
    turtle.onkey(None,"x")
    button.reset()
    button.ht()
    text.clear()
    
    config.read("highscores.ini")
    clicksPerSecond = round(counter/roundTime,5)

    try:
        for number in range(1,11):
            if clicksPerSecond > eval(config["DEFAULT"]["{}".format(number)])[0]:
                name = turtle.textinput("HIGHSCORE!","Congratulations, you have achieved a highscore!\nPlease enter you name here - only 20 letters long, please, and no \ characters!!\n(And while you're at it,\ngive me your social security and credit card numbers as well!\nI'll make good use of them, I promise :^) )")
                if name == None or len(name) > 20 or len(name) == 0 or name == "None" or "\\" in name:
                    text.goto(0,250)
                    text.color("red")
                    text.write("Invalid name. Highscore couldn't be recorded.",align="center",font=("Calibri",10,"bold"))
                    text.color("black")
                    break
                
                for nummer in range(10,number,-1):
                    config["DEFAULT"]["{}".format(nummer)] = config["DEFAULT"]["{}".format(nummer-1)]

                config["DEFAULT"]["{}".format(number)] = '[{0},"{1}"]'.format((clicksPerSecond),(name))

                with open("highscores.ini","w") as configfile: config.write(configfile)
                break
            
    except TypeError or NameError:
        text.write("Sorry, but it seems you've changed the highscores file.\nThat will not be tolerated, and as such,\nthis program will close in 3 seconds.",align="center",font=("Calibri",15))
        sleep(1)
        text.clear()
        text.write("Sorry, but it seems you've changed the highscores file.\nThat will not be tolerated, and as such,\nthis program will close in 2 seconds.",align="center",font=("Calibri",15))
        sleep(1)
        text.clear()
        text.write("Sorry, but it seems you've changed the highscores file.\nThat will not be tolerated, and as such,\nthis program will close in 1 second...",align="center",font=("Calibri",15))
        sleep(1)
        turtle.bye()
        exit()
    
    text.goto(0,0)
    text.write("{0} times clicked in total.\nYour click speed is approximately {1} clicks per second!\nClick anywhere to exit,\nor alternatively, press R to retry!\nLastly, you can press H to view them highscores!".format((counter),(clicksPerSecond)),align = "center",font=("Calibri",15,"bold"))
    turtle.onscreenclick(bye)
    turtle.onkey(initialiseLoopRedirect,"r")
    turtle.onkey(highscores,"h")

    turtle.listen()


def counterAdd(x,y):
    global counter
    counter += 1
    if playHitsound: PlaySound("hit.wav",SND_ASYNC)
    text.clear()
    text.write("{} times clicked".format(counter),align = "center",font=("Calibri",15))
    turtle.update()
    

def counterAddRedirect(): counterAdd(0,0)

def mainLoop():
    timertext = turtle.Turtle()
    timertext.ht()
    timertext.up()
    timertext.color("green")
    timertext.goto(0,-200)

    endTime = startTime + roundTime
    
    while round(time()-startTime,2) <= roundTime:
        timertext.clear()
        timertext.write("{0} seconds left\n{1} clicks per second".format(round(endTime-time(),2),round(counter/(time()-startTime),5)),align="center",font=("Comic Sans MS",20))
        
        button.onclick(counterAdd)
        button.onclick(counterAdd,3)
        turtle.onkey(counterAddRedirect,"z")
        turtle.onkey(counterAddRedirect,"x")

        turtle.listen()

    timertext.clear()
    turtle.tracer(1)
    exitLoop()
    

def initialiseLoop(x,y):
    global roundTime,playHitsound,startTime,counter,button
    text.clear()
    turtle.onscreenclick(None)
    turtle.onkey(None,"r")
    turtle.onkey(None,"h")
    text.goto(0,0)
    
    try:
        roundTime = int(turtle.numinput("Time for round","How many seconds do you want allocated for your round?\n(Maximum is 60 seconds, mind you.)",minval=1,maxval=60))
    except TypeError:
        text.write("Sorry, but you typed in an invalid 'number'.\nThis program will exit in 3 seconds.",align="center",font=("Calibri",15,"bold"))
        sleep(3)
        turtle.bye()
        exit()
        
    playHitsound = False

    for number in range(3,0,-1):
        text.write("{}".format(number),align = "center",font=("Calibri",50,"bold"))
        sleep(1)
        text.clear()
        if number == 2: text.color("red")
        
    text.goto(0,230)
    text.color("black")
    
    button = turtle.Turtle()
    button.shape("square")
    button.resizemode("user")
    button.shapesize(10,10)
    button.color("#300000")
    button.fillcolor("red")

    startTime = time()
    counter = 0
    
    turtle.tracer(0,0)
    mainLoop()
    

screen = turtle.Screen()
screen.bgcolor("gray")
screen.title("osu! clickspeed test")
text = turtle.Turtle()
config = configparser.ConfigParser()

text.up()
text.ht()
text.speed(0)
text.write("In this program, you can click using both the keyboard and the mouse.\nKinda like aus- I mean osu!, huh?\nClick anywhere to continue.",align="center",font=("Calibri",15,"bold"))
turtle.onscreenclick(initialiseLoop)

turtle.mainloop()
