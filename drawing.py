from cmu_graphics import *

dLeft, dTop, dWidth, dHeight, dScale = 0, 0, 0, 0, 0

def updateDrawVars(app):
    # Since the window is user-adjustable, we want to make sure 
    # that we are always rendering in a consistant aspect ratio
    # (default is 16:9) so that drawables don't get all fucked
    # and stretched in disproportial ways. Also keeps the math
    # simpler so that we have only one scale variable, and not
    # one for both width and height

    global dLeft, dTop, dWidth, dHeight, dScale
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

def scaledCoords(x, y):
    return dLeft + x * dWidth, dTop + y * dHeight

def scaledRadius(r):
    return r * dScale

def scaledDimensions(w, h):
    return width * dWidth, height * dHeight

def drawScaledRect(x, y, h, w, fill=None):
    drawRect(
        *scaledCoords(x, y),
        *scaledDimensions(h, w),
        fill = fill
        )