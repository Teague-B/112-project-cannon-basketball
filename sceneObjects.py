from cmu_graphics import *
import math

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def scaleCoords(x, y):
    return app.dLeft + x * app.dWidth, app.dTop + y * app.dHeight


class BaseObject:
    moveable = False
    isGhost = False
    isDrawable = True
    rotation = 0
    vx = 0
    vy = 0
    fill = [200, 200, 200]
    img = None

    def draw(self):
        pass

    def updatePos(self):
        pass

class Circle(BaseObject):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        drawCircle(
            app.dLeft + self.x * app.dWidth,
            app.dTop + self.y * app.dHeight,
            self.r * app.dScale,
            rotateAngle = self.rotation,
            fill = self.fill
        )

class Rectangle(BaseObject):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(self):
        drawRect(
            app.dLeft + self.x * app.dWidth,
            app.dTop + self.y * app.dHeight,
            self.w * app.dWidth, 
            self.h * app.dHeight,
            rotateAngle = self.rotation,
            fill = self.fill
        )
        
class Cannon(BaseObject):
    def __init__(self, x, y):
        # angle is stored in radians
        self.angle = 0
        self.x = x
        self.y = y

    def draw(self):
        cx, cy = app.dLeft + self.x * app.dWidth, app.dTop + self.y * app.dHeight
        drawLine(
            cx, 
            cy, 
            cx + 2 * math.cos(self.angle) * app.dScale,
            cy + 2 * math.sin(self.angle) * app.dScale,
            fill = 'red',
            lineWidth = 0.5 * app.dScale,
        )
        drawCircle(
            cx,
            cy,
            0.5 * app.dScale,
            rotateAngle = self.rotation,
            fill = self.fill
        )


    def updateAngle(self, x, y):

        selfX, selfY = scaleCoords(self.x, self.y)
        # Law of cosines
        c = distance(selfX, selfY, x, y)
        b = x - selfX
        a = y - selfY

        if a > 0:
            a = 0

        cosA = 0

        print(f"A: {a}, B: {b}, C: {c}")
        if rounded(b) == 0:
            print('h')
            if a < 0:
                cosA = math.radians(0)
            else:
                cosA = math.radians(0)
        else:
            cosA = (b*b + c*c - a*a) / (2*b*c)
                
        
        cosA = max(-1, min(1, cosA))
        print(cosA)
        angle = math.acos(cosA)
        print("angle", math.degrees(angle))
        self.angle = math.radians(360) - angle