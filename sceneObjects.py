from cmu_graphics import *

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

class BaseObject:
    moveable = False
    isGhost = False
    isDrawable = True
    rotation = 0
    vx = 0
    vy = 0
    fill = [200, 200, 200]

    def draw(self, dScale, dLeft, dTop, dWidth, dHeight):
        pass

    def updatePos(self):
        pass

class Circle(BaseObject):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self, dScale, dLeft, dTop, dWidth, dHeight):
        drawCircle(
            dLeft + self.x * dWidth,
            dTop + self.y * dHeight,
            self.r * dScale,
            rotateAngle = self.rotation,
            fill = self.fill
        )

class Rectangle(BaseObject):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(self, dScale, dLeft, dTop, dWidth, dHeight):
        drawRect(
            dLeft + self.x * dWidth,
            dTop + self.y * dHeight,
            self.w * dWidth, 
            self.h * dHeight,
            rotateAngle = self.rotation,
            fill = self.fill
        )
        