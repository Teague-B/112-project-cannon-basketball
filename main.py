from cmu_graphics import *
from json import load

import scene

def onAppStart(app):
    app.jsonCfg = {}
    app.steps = 0

    with open('cfg.json', 'r') as jsonCfgFile:
        app.jsonCfg = load(jsonCfgFile)

    app.height = app.jsonCfg['appInitWindowHeight']
    app.width = app.jsonCfg['appInitWindowWidth']
    app.stepsPerSecond = app.jsonCfg['stepsPerSecond']

    app.curScene = scene.Scene(app.jsonCfg['appInitScene'])

    updateDrawVars(app)

def updateDrawVars(app):
    hRatio = app.height / app.jsonCfg['appAspectRatioHeight']
    wRatio = app.width / app.jsonCfg['appAspectRatioWidth']
    scale = hRatio
    if wRatio < hRatio:
        scale = wRatio

    app.dLeft = (app.width - scale * app.jsonCfg['appAspectRatioWidth']) / 2
    app.dTop = (app.height - scale * app.jsonCfg['appAspectRatioHeight']) / 2
    app.dWidth = app.left + scale * app.jsonCfg['appAspectRatioWidth']
    app.dHeight = app.top + scale * app.jsonCfg['appAspectRatioHeight']

    app.dScale = scale

def onStep(app):
    updateDrawVars(app)

    #print(len(app.curScene.objectList))
    app.curScene.doPhysics(app)
    app.curScene.clearOffscreen()
    app.steps += 1

def onMouseMove(app, x, y):
    app.curScene.onMouseMove(x, y)

def onMouseDrag(app, x, y):
    app.curScene.onMouseMove(x, y)

def onMousePress(app, x, y):
    app.curScene.onMouseClick(x, y)
    app.curScene.correctDrawOrder()

def redrawAll(app):
    # make sure window is completely black before drawing anything
    drawRect(0, 0, app.width, app.height, fill='black')

    app.curScene.drawScene(app)

def main():
    runApp()

if __name__ == '__main__':
    main()