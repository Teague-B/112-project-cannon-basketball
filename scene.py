from cmu_graphics import *
from json import load

import sceneObjects

class Scene:
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
            
            if isinstance(self.objectList[-1], sceneObjects.Drawable):
                self.objectList[-1].rotation = obj.get('rotation', sceneObjects.Drawable.rotation)
                self.objectList[-1].fill = rgb(*tuple(obj.get('fill', sceneObjects.Drawable.fill)))

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
            if isinstance(obj, sceneObjects.Drawable):
                obj.draw(dScale, dLeft, dTop, dWidth, dHeight)
