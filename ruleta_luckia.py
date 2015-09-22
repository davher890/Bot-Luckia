import os, sys
from PIL import Image, ImageGrab, ImageOps
import time, random
from random import randrange
import win32api, win32con
from numpy import *
from threading import Thread
import datetime
import logging
from win32api import keybd_event

#Define play area
bottomRight = (903,737)
xPad, yPad = 104, 85


##Grabs entire play area
def grab():
    box= (xPad,yPad,bottomRight[0],bottomRight[1])
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\Grab001.png', 'PNG')
    return im

def grabBox(x1, y1, x2, y2):
    im = ImageGrab.grab((xPad+x1, yPad+y1, xPad+x2, yPad+y2))
    im.save(os.getcwd() + '\\Grab001.png', 'PNG')
    return im


def getCords():
    x,y = win32api.GetCursorPos()
    x = x - xPad
    y = y - yPad
    s = grab()
    log(x+y+s.getpixel((x,y)))

def mousePos(x=(0,0)):
    win32api.SetCursorPos(x)

def selectCoin050():
    mousePos(coin['c050'])
    leftClick()

def selectCoin1():
    mousePos(coin['c1'])
    leftClick()
     
def selectColor(betColor):
    i = 0
    while i < bet: 
        mousePos(betColor)
        leftClick()
        i += betAmount    

def cleanBet():
    mousePos(menuLoc['clean'])
    leftClick()

def closeExpTimeMsg():
    mousePos(menuLoc['expiredTimeButton'])
    leftClick()

def changeBetColor():
    global betColor
    if betColor == menuLoc['red']:
        betColor = menuLoc['black']
    else:
        betColor = menuLoc['red']

def getPixelAv(box):
    im = ImageOps.grayscale(ImageGrab.grab(box))
    im.save(os.getcwd() + '\\Grab001.png', 'PNG')
    a = array(im.getcolors())
    a = a.sum()
    #im.save(os.getcwd() + '\\Grab001.png', 'PNG')
    return a
    
#
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    sleep(.01)

def run(saldoParam, betParam=0.5):

    global betAmount, bet, winGames, saldo
    
    betAmount = betParam
    bet = betParam
    saldo = saldoParam

    log("Play with betAmount=",betAmount, " and balance = ", saldo)
    log("Waiting for x of the same color")

    if (winGames*bet < 5):    
        while True:
            sleep(8)
            ## To move the mouse and avoid expired session
            mousePos(coin['c050'])
            ##
            color1 = getPixelAv(menuLoc['colorWin1'])
            color2 = getPixelAv(menuLoc['colorWin2'])
            color3 = getPixelAv(menuLoc['colorWin3'])
            color4 = getPixelAv(menuLoc['colorWin4'])
            if (color1 == color2 == color3 == color4):
                if (color1 == blackPixelAv):
                    log( "x seguidos negros")
                    play(menuLoc['red'])
                elif (color1 == redPixelAv):
                    
                    log( "x seguidos rojos")
                    play(menuLoc['black'])
    else:
        log("Day win")
            
def play(color):
    global winGames, bet, betAmount, saldo
    
    #Can bet, green light
    log( "Waiting for green light to bet")
    while getPixelAv(menuLoc['greenLight']) != 1384:        
        sleep(4)
        
    if betAmount == 0.5:
        selectCoin050()

    if betAmount == 1:
        selectCoin1()
    
    selectColor(color)
    
    if checkIfWin(color) == True:
        saldo += bet
        bet = betAmount
        winGames += 1
        cleanBet()
        run(saldo, betAmount)

    else:
        saldo -= bet
        bet *= 2
        if saldo < 10 or (saldo-bet) < 10:
            cleanBet()
            run(saldo, betAmount)

def checkIfWin(color):
    s = grab()
    #New result

    log( "Waiting for the yellow light")
    while getPixelAv(menuLoc['yellowLight']) != yellowLight :
        sleep(2)

    log( "Waiting for the gree light -> result")
    while getPixelAv(menuLoc['greenLight']) != greenLight : 
        sleep(3)
        
    #Si ha salido negro y he apostado al negro
    if getPixelAv(menuLoc['colorWin1']) == blackPixelAv and color == menuLoc['black']:
        log( "Win. Balance=", saldo)
        return True
    #Si ha salido rojo y he apostado al rojo
    if getPixelAv(menuLoc['colorWin1']) == redPixelAv and color == menuLoc['red']:
        log( "Win. Balance=", saldo)
        return True

    log( "Not Win. Balance=", saldo)
    return False

def sleep(timeSleep):
    time.sleep(timeSleep)
    if getPixelAv(menuLoc['expiredTime']) == expiredTimeAv:
        closeExpTimeMsg();

def log(*message):
    logging.info(message)


def restartApp():
    rest_time = 0.05
    KeyDown(18)
    time.sleep(rest_time)
    KeyDown(73)
    time.sleep(rest_time)
    KeyUp(73)
    time.sleep(rest_time)
    KeyUp(18)


def KeyUp(Key):
    keybd_event(Key, 0, 2, 0)


def KeyDown(Key):
    keybd_event(Key, 0, 1, 0)
    
#--------------------------

#GLOBALS

coin = {'c050':(xPad+323,yPad+597),
        'c1':(xPad+369,yPad+597),
        'c5':(xPad+410,yPad+597),
        'c25':(xPad+450,yPad+597),
        'c100':(xPad+491,yPad+597),
        'c500':(xPad+533,yPad+597)}

blackPixelAv = 1336
redPixelAv = 1251
ceroPixelAv = 1241

expiredTimeAv = 7859
expiredSessionScreenAv = 53464

greenLight = 1384
yellowLight = 1613
redLight = 694

betAmount = 0.5
bet = 0.5
saldo = 0

menuLoc = {'red':(xPad+181,yPad+330),
           'black':(xPad+218,yPad+378),
           'colorWin1':((xPad+712,yPad+113,xPad+774,yPad+131)),
           'colorWin2':((xPad+712,yPad+133,xPad+774,yPad+151)),
           'colorWin3':((xPad+712,yPad+153,xPad+774,yPad+171)),
           'colorWin4':((xPad+712,yPad+173,xPad+774,yPad+191)),
           'clean':(xPad+250,yPad+597),
           'greenLight':((xPad+668,yPad+5,xPad+671,yPad+8)),
           'yellowLight':((xPad+711,yPad+5,xPad+714,yPad+8)),
           'redLight':((xPad+757,yPad+5,xPad+760,yPad+8)),
           'expiredTime':((xPad+520,yPad+327,xPad+550,yPad+348)),
           'expiredTimeButton':(xPad+535,yPad+335),
           'expiredSessionScreen':((xPad+13,yPad+255,xPad+791,yPad+322))
            }

winGames = 0

def main():

    logging.basicConfig(format='%(asctime)s %(message)s',filename='example.log',level=logging.DEBUG)
    log("thread finished...exiting")


if __name__ == '__main__':
    main()

