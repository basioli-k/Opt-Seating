import math


class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def distance(self, p):
        return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)
