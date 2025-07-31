from cmu_graphics import *
from json import load
from os import sep as pathSep

import sceneObjects

class Scene:
    # If anyone has a better idea for converting JSON to classes,
    # please let me know bc I hate just about everything in this
    # friggin function
    def __init__(self, id):
        data = {}
        with open("scenes"+pathSep+id+".json", 'r') as sceneFile:
            data = load(sceneFile)
        
        self.id = id
        self.objectList = []

        for obj in data['objectList']:
            if obj['type'] == "Rect":
                self.objectList.append(sceneObjects.Rectangle(
                    obj['x'],
                    obj['y'],
                    obj['width'],
                    obj['height']
                ))
            elif obj['type'] == "Label":
                self.objectList.append(sceneObjects.LabelText(
                    obj['x'],
                    obj['y'],
                    obj['text']
                ))
            elif obj['type'] == "Circle":
                self.objectList.append(sceneObjects.Circle(
                    obj['x'],
                    obj['y'],
                    obj['r']
                ))
            elif obj['type'] == "Cannon":
                self.objectList.append(sceneObjects.Cannon(
                    obj['x'],
                    obj['y']
                ))
            elif obj['type'] == "Hoop":
                self.objectList.append(sceneObjects.Hoop(
                    obj['x'],
                    obj['y'],
                    obj['w'],
                    obj['h'],
                    obj['nextScene']
                ))
            elif obj['type'] == "WindBox":
                self.objectList.append(sceneObjects.WindBox(
                    obj['x'],
                    obj['y'],
                    obj['width'],
                    obj['height'],
                    obj['direction']
                ))
            else:
                assert False, f"Unknown object type: {obj['type']}"
            
            # Optional variables
            # Whoever coded undertale would be proud
            self.objectList[-1].rotation = obj.get('rotation', sceneObjects.BaseObject.rotation)
            self.objectList[-1].fill = tuple(obj.get('fill', sceneObjects.BaseObject.fill))
            self.objectList[-1].moveable = obj.get('moveable', sceneObjects.BaseObject.moveable)
            self.objectList[-1].isGhost = obj.get('isGhost', sceneObjects.BaseObject.isGhost)
            self.objectList[-1].isDrawable = obj.get('isDrawable', sceneObjects.BaseObject.isDrawable)
            self.objectList[-1].img = obj.get('img', sceneObjects.BaseObject.img)

    def drawScene(self, app):
        drawImage(app.jsonCfg['sprites']['background'], app.dTop, app.dLeft, height=app.dTop + app.dHeight, width=app.dLeft+app.dWidth)
        # Draw drawable objects
        for obj in self.objectList:
            if obj.isDrawable:
                obj.draw()
        
        if self.id == "end":
            sum = 0
            for key in app.timers:
                if key != "intro":
                    sum += app.timers[key]
            mins = sum // app.stepsPerSecond
            seconds = sum % app.stepsPerSecond
            if seconds < 10:
                seconds = "0" + str(seconds)
            drawLabel(f"Total Time: {mins}.{str(seconds)} seconds!", 0.5 * app.dScale, 0.5 * app.dScale, bold=True, size=24)

    def clearOffscreen(self):
        i = 0
        while i < len(self.objectList):
            if self.objectList[i].y > 1.1 or self.objectList[i].x < -0.1 or self.objectList[i].x > 1.1 or self.objectList[i].y < -0.1:
                self.objectList.pop(i)
            else:
                i += 1
    
    def correctDrawOrder(self):
        def f(x):
            #print(x)
            return isinstance(x, sceneObjects.Cannon)
        self.objectList.sort(key=f)
        #print(self.objectList)

    def doCollisions(self):
        for obj in self.objectList:
            if not obj.isGhost and isinstance(obj, sceneObjects.Basketball):
                for obj2 in self.objectList:
                    if obj != obj2 and obj.isGhost == False:
                        obj.doCollision(obj2)
                        
    def doPhysics(self, app):
        for obj in self.objectList:
            if obj.moveable:
                obj.vy -= app.jsonCfg['gravityForce'] / app.stepsPerSecond

        self.doCollisions()

        for obj in self.objectList:
            if obj.moveable:
                obj.x += obj.vx / app.stepsPerSecond
                obj.y -= obj.vy / app.stepsPerSecond


    def onMouseMove(self, x, y):
        for obj in self.objectList:
            if isinstance(obj, sceneObjects.Cannon):
                obj.updateAngle(x, y)

    def onMouseClick(self, x, y):
        for obj in self.objectList:
            if isinstance(obj, sceneObjects.Cannon):
                self.objectList.append(obj.fireBall(x, y))
