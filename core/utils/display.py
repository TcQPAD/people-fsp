#!/usr/bin/python
# -*- coding: utf-8 -*-

import Queue  # a Thread safe Queue to receive the commands from other Threads
from Tkinter import *

from core.threads.main_background_thread import Main

DEFAULT_DISPLAY_WIDTH = 500
DEFAULT_DISPLAY_HEIGHT = 500
MARGIN = 5

'''
Class that holds the graphic display of the simulation

This class MUST BE RUN ON THE MAIN THREAD or a "main loop not in main thread"
error will spawn randomly

This class uses a Queue in order to get the messages/commands
from background threads running the simulation.

This is useful to avoid blocking the main Thread, and to communicate with
the background threads in order to draw the simulation
'''


class Display:

    def __init__(self, nbP, args, gui, width=DEFAULT_DISPLAY_WIDTH, height=DEFAULT_DISPLAY_HEIGHT):
        print("Let's display this!")

        self.nbP = nbP
        self.args = args

        self.queue = Queue.Queue()

        self.width = width
        self.height = height
        self.xOrigin = 11
        self.yOrigin = 11

        self.window = gui
        self.canvas = Canvas(self.window, width=self.width + 10, height=self.height + 10, bg="white", bd=8)
        self.startTk()

    @property
    def queue(self):
        return self.queue

    def startTk(self):
        self.canvas.pack()  # Affiche le Canvas
        self.drawBorders()

        Main(self.nbP, self.queue, self.args).start()

        self.window.after(10, self.draw)

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

    """
    Draws something based on the message
    received in the thread safe queue, from a background worker thread
    
    This method is called indefinitely till the main thread is destroyed,
    typically when reaching the end of the simulation
    """

    def draw(self):
        try:
            msg = self.queue.get(0)

            print(msg)

            # if all threads finished working
            if "exit" in msg:
                self.displayFinalState()
            # this a person coordinate
            else:
                msg = msg.split()  # splits coordinates in an array of size 2 or 4
                if len(msg) == 2:  # this is a person
                    self.drawPerson(int(msg[0]), int(msg[1]))
                elif len(msg) == 4:  # this an obstacle
                    self.drawObstacle(int(msg[0]), int(msg[1]), int(msg[2]), int(msg[3]))

        except Queue.Empty:
            # wait 100ms before de-queuing
            self.window.after(10, self.draw)

    '''
    Erase a person dot
    '''

    def erasePerson(self, x, y):
        self.drawDot(x, y, "white")
