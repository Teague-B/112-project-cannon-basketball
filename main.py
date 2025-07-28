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

def onStep(app):
    # write stuff here

    app.curScene.doPhysics(app)
    app.steps += 1

def redrawAll(app):
    # make sure window is completely black before drawing anything
    drawRect(0, 0, app.width, app.height, fill='black')

    app.curScene.drawScene(app)



def main():
    runApp()

if __name__ == '__main__':
    main()