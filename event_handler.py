import pygame


class EventHandler():
    def __init__(self):
        self.eventTable = {}
    
    def on(self, eventType, eventHandler):
        self.eventTable[eventType] = eventHandler
        
    def listen(self):
        for event in pygame.event.get():
            if event.type in self.eventTable:
                self.eventTable[event.type](event)