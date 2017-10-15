#!/usr/bin/python
# -*- coding: utf-8 -*-

import turtle
from threading import Lock

DEFAULT_DISPLAY_WIDTH = 500
DEFAULT_DISPLAY_HEIGHT = 500
MARGIN = 5

'''
Class that holds the graphic display of the simulation
'''
class Display :

    def __init__(self, width = DEFAULT_DISPLAY_WIDTH, height = DEFAULT_DISPLAY_HEIGHT):
        print("Let's display this!")
        
        self.width = width
        self.height = height
        self.xOrigin = MARGIN - width/2
        self.yOrigin = height/2 - MARGIN
        
        self.sharedDisplayLock = Lock()
        
        turtle.setup(width, height)  #Initialise la fen�tre en 500*500
        turtle.title("Projet Prog Concurente")
        turtle.penup()
        turtle.goto(self.xOrigin, self.yOrigin)
        turtle.hideturtle() #Cache le curseur
        
    '''
    Return the relative position according to the x origin
    '''
    def getRelativeXPosition(self, x):
        return self.xOrigin + x
    
    '''
    Return the relative position according to the y origin
    '''
    def getRelativeYPosition(self, y):
        return self.yOrigin - y
        
    '''
    Draw the borders of the simulation
    '''
    def drawBorders(self, width, height):
        turtle.goto(self.getRelativeXPosition(-1), self.getRelativeYPosition(-1))
        turtle.pendown()
        turtle.goto(self.getRelativeXPosition(width+1), self.getRelativeYPosition(-1))
        turtle.goto(self.getRelativeXPosition(width+1), self.getRelativeYPosition(height+1))
        turtle.goto(self.getRelativeXPosition(-1), self.getRelativeYPosition(height+1))
        turtle.goto(self.getRelativeXPosition(-1), self.getRelativeYPosition(-1))
        turtle.penup()
    
    '''
    Draw an obstacle on the display
    '''
    def drawObstacle(self, x1, y1, x2, y2):
        turtle.color("red")
        turtle.fill(True)
        turtle.goto(self.getRelativeXPosition(x1), self.getRelativeYPosition(y1))
        turtle.pendown()
        turtle.goto(self.getRelativeXPosition(x2), self.getRelativeYPosition(y1))
        turtle.goto(self.getRelativeXPosition(x2), self.getRelativeYPosition(y2))
        turtle.goto(self.getRelativeXPosition(x1), self.getRelativeYPosition(y2))
        turtle.goto(self.getRelativeXPosition(x1), self.getRelativeYPosition(y1))
        turtle.penup()
        turtle.fill(False)
        turtle.color("black")
    
    '''
    Draw an colored dot on the display
    '''
    def drawDot(self, x, y, color):
        self.sharedDisplayLock.acquire()
        turtle.color(color)
        turtle.goto(self.getRelativeXPosition(x), self.getRelativeYPosition(y))
        turtle.pendown()
        turtle.dot(2)
        turtle.penup()
        turtle.color("black")
        self.sharedDisplayLock.release()
    
    '''
    Draw an exit dot on the display
    '''
    def drawExit(self, x, y):
        self.drawDot(x, y, "green")
    
    '''
    Draw an person dot on the display
    '''
    def drawPerson(self, x, y):
        self.drawDot(x, y, "blue")
        
    '''
    Erase a person dot
    '''
    def erasePerson(self, x, y):
        self.drawDot(x, y, "white")
    
    '''
    Close the display
    '''
    def close(self):
        turtle.bye()