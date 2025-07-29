from cmu_graphics import *
from json import load

import sceneObjects

class Scene:
    # If anyone has a better idea for converting JSON to classes,
    # please let me know bc I hate just about everything in this
    # friggin function
    def __init__(self, id):
        data = {}
        with open("scenes/"+id+".json", 'r') as sceneFile:
            data = load(sceneFile)
        
        self.id = id
        self.sceneType = data['sceneType']
        self.objectList = []

        for obj in data['objectList']:
            if obj['type'] == "Rect":
                self.objectList.append(sceneObjects.Rectangle(
                    obj['x'],
                    obj['y'],
                    obj['width'],
                    obj['height']
                ))
            elif obj['type'] == "Circle":
                self.objectList.append(sceneObjects.Circle(
                    obj['x'],
                    obj['y'],
                    obj['r']
                ))
            else:
                assert False, f"Unknown object type: {obj['type']}"
            
            # Optional variables
            # Whoever coded undertale would be proud
            self.objectList[-1].rotation = obj.get('rotation', sceneObjects.BaseObject.rotation)
            self.objectList[-1].fill = rgb(*tuple(obj.get('fill', sceneObjects.BaseObject.fill)))
            self.objectList[-1].moveable = obj.get('moveable', sceneObjects.BaseObject.moveable)
            self.objectList[-1].isGhost = obj.get('isGhost', sceneObjects.BaseObject.isGhost)
            self.objectList[-1].isDrawable = obj.get('isDrawable', sceneObjects.BaseObject.isDrawable)
            self.objectList[-1].img = obj.get('img', sceneObjects.BaseObject.img)

    def drawScene(self, app):
        # Calculate the scale constant
        dLeft, dTop, dWidth, dHeight, dScale = 0, 0, 0, 0, 0

        hRatio = app.height / app.jsonCfg['appAspectRatioHeight']
        wRatio = app.width / app.jsonCfg['appAspectRatioWidth']
        scale = hRatio
        if wRatio < hRatio:
            scale = wRatio

        dLeft = (app.width - scale * app.jsonCfg['appAspectRatioWidth']) / 2
        dTop = (app.height - scale * app.jsonCfg['appAspectRatioHeight']) / 2
        dWidth = app.left + scale * app.jsonCfg['appAspectRatioWidth']
        dHeight = app.top + scale * app.jsonCfg['appAspectRatioHeight']

        dScale = scale

        # Draw drawable objects
        for obj in self.objectList:
            if obj.isDrawable:
                obj.draw(dScale, dLeft, dTop, dWidth, dHeight)

    def doPhysics(self, app):
        for obj in self.objectList:
            if obj.moveable:
                obj.vy -= app.jsonCfg['gravityForce']



                obj.x += obj.vx / app.stepsPerSecond
                obj.y -= obj.vy / app.stepsPerSecond
