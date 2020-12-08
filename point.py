import math

class point:
    
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        
    def distance(self,p):
        return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)
    
