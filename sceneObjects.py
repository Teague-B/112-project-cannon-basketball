from cmu_graphics import *
import math

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def scaleCoords(x, y):
    return app.dLeft + x * app.dWidth, app.dTop + y * app.dHeight

def unScaleCoords(x, y):
    return x / app.dWidth - app.dLeft, y / app.dHeight - app.dTop


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

    def draw(self): app.jsonCfg['cannon']['scale']
        drawCircle(
            app.dLeft + self.x * app.dWidth,
            app.dTop + self.y * app.dHeight,
            self.r * app.dScale,
            rotateAngle = self.rotation,
            fill = rgb(*tuple(self.fill))
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
            fill = rgb(*self.fill)
        )
        
class Cannon(BaseObject):
    def __init__(self, x, y):
        # angle is stored in radians
        self.angle = 0
        self.x = x
        self.y = y

    def getEndBarrelCoords(self):
        cx, cy = app.dLeft + self.x * app.dWidth, app.dTop + self.y * app.dHeight
        cannonCfg = app.jsonCfg['cannon']
        barrelLen = cannonCfg['barrelLength'] * cannonCfg['scale']
        return cx + barrelLen * math.cos(self.angle) * app.dScale, cy + barrelLen * math.sin(self.angle) * app.dScale

    def draw(self):
        cx, cy = app.dLeft + self.x * app.dWidth, app.dTop + self.y * app.dHeight
        drawLine(
            cx, 
            cy, 
            *self.getEndBarrelCoords(),
            fill = rgb(*tuple(app.jsonCfg['cannon']['barrelColor'])),
            lineWidth = 0.5 * app.dScale * app.jsonCfg['cannon']['scale'],
        )
        drawCircle(
            cx,
            cy,
            0.4 * app.dScale * app.jsonCfg['cannon']['scale'],
            rotateAngle = self.rotation,
            fill = rgb(*self.fill)
        )


    def updateAngle(self, x, y):
        selfX, selfY = scaleCoords(self.x, self.y)

        # Law of cosines
        # all of this crap through the print calls
        # are to calculate the angle of the cannon
        # properly with some additional rules
        c = distance(selfX, selfY, x, y)
        b = x - selfX
        a = y - selfY

        # if the cursor is below the cannon stop
        # the cannon from angling down
        if a > 0:
            a = 0

        cosA = 0

        #print(f"A: {a}, B: {b}, C: {c}")
        if rounded(b) == 0:
            #print('h')
            cosA = math.radians(0)
        elif c != 0:
            cosA = (b*b + c*c - a*a) / (2*b*c)
            cosA = max(-1, min(1, cosA))
            self.angle = math.radians(360) - math.acos(cosA)
        else:
            cosA = self.angle
                
        #print(cosA)
        #print("angle", math.degrees(self.angle))

    def fireBall(self, x, y):
        self.updateAngle(x, y)
        c = Circle(
                *unScaleCoords(*self.getEndBarrelCoords()),
                app.jsonCfg['cannon']['barrelWidth'] * app.dScale / 200
            )
        c.vx = app.jsonCfg['cannon']['strength'] * math.cos(self.angle)
        c.vy = -app.jsonCfg['cannon']['strength'] * math.sin(self.angle)
        c.moveable = True
        return c
        