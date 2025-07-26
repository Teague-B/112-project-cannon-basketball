from json import load
import sceneObjects

def loadUnparsedData(id):
    unparsedData = {}
    with open("scenes/"+id+".json", 'r') as sceneFile:
        unparsedData = load(sceneFile)
    return unparsedData


def loadFromID(id):

    unparsedData = loadUnparsedData(id)

    scene = {
        "id": id,
        "sceneType": unparsedData['sceneType']
    }

    print(unparsedData)

    # TODO: Actually parse the data into classes once
    # the classes are written

    
def drawSceneObjects(app):
    for obj in app.curScene['objectList']:
        obj.draw()
