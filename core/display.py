#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *

DEFAULT_DISPLAY_WIDTH = 500
DEFAULT_DISPLAY_HEIGHT = 500
MARGIN = 5

'''
Class that holds the graphic display of the simulation
'''


class Display:

    def __init__(self, width=DEFAULT_DISPLAY_WIDTH, height=DEFAULT_DISPLAY_HEIGHT):
        print("Let's display this!")

        self.width = width
        self.height = height
        self.xOrigin = 11
        self.yOrigin = 11

        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.width + 10, height=self.height + 10, bg="white", bd=8)
        self.canvas.pack()  # Affiche le Canvas

        self.drawBorders()

    def displayFinalState(self):
        self.window.mainloop()

    '''
    Return the relative position according to the x origin
    '''

    def getRelativeXPosition(self, x):
        return self.xOrigin + x

    '''
    Return the relative position according to the y origin
    '''

    def getRelativeYPosition(self, y):
        return self.yOrigin + y

    '''
    Draw the borders of the simulation
    '''

    def drawBorders(self):
        x1 = self.getRelativeXPosition(0)
        y1 = self.getRelativeYPosition(0)
        x2 = self.getRelativeXPosition(self.width)
        y2 = self.getRelativeYPosition(self.height)
        self.canvas.create_rectangle(x1, y1, x2, y2)

    '''
    Draw an obstacle on the display
    '''

    def drawObstacle(self, x1, y1, x2, y2):
        relativeX1 = self.getRelativeXPosition(x1)
        relativeY1 = self.getRelativeYPosition(y1)
        relativeX2 = self.getRelativeXPosition(x2)
        relativeY2 = self.getRelativeYPosition(y2)
        self.canvas.create_rectangle(relativeX1, relativeY1, relativeX2, relativeY2, outline="red", fill="red")
        self.window.update()

    '''
    Draw an colored dot on the display
    '''

    def drawDot(self, x, y, color):
        relativeX = self.getRelativeXPosition(x)
        relativeY = self.getRelativeYPosition(y)
        self.canvas.create_oval(relativeX, relativeY, relativeX, relativeY, outline=color)
        self.window.update()

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
