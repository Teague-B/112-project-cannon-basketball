from cmu_graphics import *
import math

import scene

def clamp(s, x, m):
    return max(m, min(m, x))

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def scaleCoords(x, y):
    return app.dLeft + x * app.dWidth, app.dTop + y * app.dHeight

def unScaleCoords(x, y):
    return x / app.dWidth - app.dLeft, y / app.dHeight - app.dTop

def pointIsIn(x, y, l, t, r, b):
    #print(x, y, l, t, r, b)
    return (l < x < r) and (t < y < b)

def rectContains(inner, outer):
    return (
        outer.x <= inner.x and
        outer.y <= inner.y and
        inner.x + inner.w <= outer.x + outer.w and
        inner.y + inner.h <= outer.y + outer.h
    )

def convertToVector(x, y):
    return (x**2 + y**2)**0.5


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
            fill = rgb(*tuple(self.fill))
        )

    def doCollision(self, other):
        pass

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
            fill = rgb(*self.fill),
            border = 'black'
        )

class WindBox(BaseObject):
    def __init__(self, x, y, w, h, d):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.direction = d

    def draw(self):
        drawRect(
            self.x * app.dWidth,
            self.y * app.dHeight,
            self.w * app.dWidth,
            self.h * app.dHeight,
            opacity = 50,
            fill=rgb(255, 255, 255)
        )
        if self.direction == 'up':
            drawLine(
                self.x * app.dWidth + self.w * app.dWidth / 2,
                self.y * app.dHeight + self.h * app.dHeight - self.h * app.dHeight / 8,
                self.x * app.dWidth + self.w * app.dWidth / 2,
                self.y * app.dHeight + self.h * app.dHeight / 8,
                fill = rgb(255, 255, 255),
                arrowEnd=True
            )

class Hoop(BaseObject):
    def __init__(self, x, y, w, h, ns):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.nextScene = ns
    
    def draw(self):
        # net
        drawRect(
            app.dLeft + self.x * app.dWidth + self.w * app.dWidth / 16,
            app.dTop + self.y * app.dHeight,
            self.w * app.dWidth - self.w * app.dWidth / 8, 
            self.h * app.dHeight,
            fill = 'grey',
            border = 'black'
        )
        # hoop
        drawRect(
            app.dLeft + self.x * app.dWidth,
            app.dTop + self.y * app.dHeight,
            self.w * app.dWidth, 
            self.h * app.dHeight / 8,
            fill = 'red',
            border = 'black'
        )

class Basketball(BaseObject):
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
            fill = rgb(*self.fill),
            align = 'center',
            border = rgb(*tuple(app.jsonCfg['basketball']['border']))
        )
        drawLine(
            app.dLeft + self.x * app.dWidth,
            app.dTop + self.y * app.dHeight - self.w * app.dScale / 2,
            app.dLeft + self.x * app.dWidth,
            app.dTop + self.y * app.dHeight + self.w * app.dScale / 2,
            fill = 'black',
            lineWidth = 2
        )
        drawLine(
            app.dLeft + self.x * app.dWidth - self.w * app.dScale / 2,
            app.dTop + self.y * app.dHeight,
            app.dLeft + self.x * app.dWidth + self.w * app.dScale / 2,
            app.dTop + self.y * app.dHeight,
            fill = 'black',
            lineWidth = 2
        )
        drawLine(
            app.dLeft + self.x * app.dWidth - self.w * app.dScale / 2,
            app.dTop + self.y * app.dHeight - self.w * app.dScale / 4,
            app.dLeft + self.x * app.dWidth + self.w * app.dScale / 2,
            app.dTop + self.y * app.dHeight + self.w * app.dScale / 4,
            fill = 'black',
            lineWidth = 2
        )
        drawLine(
            app.dLeft + self.x * app.dWidth - self.w * app.dScale / 2,
            app.dTop + self.y * app.dHeight + self.w * app.dScale / 4,
            app.dLeft + self.x * app.dWidth + self.w * app.dScale / 2,
            app.dTop + self.y * app.dHeight - self.w * app.dScale / 4,
            fill = 'black',
            lineWidth = 2
        )

    def doCollision(rectA, rectB):
        # Basketballs are drawn such as their x, y is their center
        # Jesus christ I hate this funcion, so many fucking hours
        if isinstance(rectB, Cannon) or isinstance(rectB, LabelText):
            return
        ax, ay, aw, ah = rectA.x - rectA.w / 2, rectA.y - rectA.w / 2, rectA.w, rectA.h
        bx, by, bw, bh = rectB.x, rectB.y, rectB.w, rectB.h
        if isinstance(rectB, Basketball):
            bx, by = rectB.x - rectB.w / 2, rectB.y - rectA.w / 2
        ar = ax + aw
        ab = ax + ah
        br = bx + bw
        bb = by + bh
        if isinstance(rectB, WindBox):
            if pointIsIn(rectA.x, rectA.y, rectB.x, rectB.y, rectB.x + rectB.w, rectB.y + rectB.h):
                if rectB.direction == "up":
                    rectA.vy = abs(rectA.vy)
        
        if isinstance(rectB, Basketball) or isinstance(rectB, Rectangle):
            if pointIsIn(ax, ay, bx, by, br, bb) or pointIsIn(ar, ay, bx, by, br, bb) or pointIsIn(ax, ab, bx, by, br, bb) or pointIsIn(ar, ab, bx, by, br, bb):
                #print('boing', rectA, rectB)
                
                dxLeft = (rectA.x + rectA.w / 2) - rectB.x               
                dxRight = (rectB.x + rectB.w) - (rectA.x - rectA.w / 2)  
                dyTop = (rectA.y + rectA.h / 2) - rectB.y               
                dyBottom = (rectB.y + rectB.h) - (rectA.y - rectA.h / 2)

                absPenX = dxLeft if abs(dxLeft) < abs(dxRight) else -dxRight
                absPenY = dyTop if abs(dyTop) < abs(dyBottom) else -dyBottom


                if abs(absPenX) < abs(absPenY):
                    print("x", rectA, rectB)
                    rectA.x -= absPenX
                    rectA.vx = -rectA.vx
                else:
                    print("y", rectA, rectB)
                    if rectA.vy > 0:
                        rectA.y -= absPenY
                        rectA.vy = -rectA.vy
                
                

        elif isinstance(rectB, Hoop):
            x = app.dLeft + rectB.x * app.dWidth + rectB.w * app.dWidth / 16
            y = app.dTop + rectB.y * app.dHeight
            w = rectB.w * app.dWidth - rectB.w * app.dWidth / 8
            h = rectB.h * app.dHeight
            
            if rectContains(Rectangle(ax, ay, rectA.w, rectA.h), Rectangle(rectB.x + rectB.w / 16, rectB.y, rectB.w - rectB.w / 8, rectB.h)):
                app.curScene = scene.Scene(rectB.nextScene)

        
            
        
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
            fill = rgb(*self.fill),
            border = 'black'
        )


    def updateAngle(self, x, y):
        selfX, selfY = scaleCoords(self.x, self.y)

        # Law of cosines
        # all of this crap is meant to properly
        # calculate the angle of the cannon
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
        tx, ty = unScaleCoords(*self.getEndBarrelCoords())
        #print(tx, ty)
        c = Basketball(tx, ty, app.jsonCfg['cannon']['barrelWidth'] / 12, app.jsonCfg['cannon']['barrelWidth'] / 12)
        c.vx = app.jsonCfg['cannon']['strength'] * math.cos(self.angle)
        c.vy = -app.jsonCfg['cannon']['strength'] * math.sin(self.angle)
        c.moveable = True
        c.fill = app.jsonCfg['basketball']['fill']
        return c

class LabelText(BaseObject):
    def __init__(self, x, y, txt):
        self.x = x
        self.y = y
        self.txt = txt

    def draw(self):
        drawLabel(self.txt, *scaleCoords(self.x, self.y), bold=True, size=24)
        