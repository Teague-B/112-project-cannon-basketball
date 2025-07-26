from json import load
import drawing
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

    
def drawSceneObjects(app):
    for obj in app.curScene['objectList']:
        obj.draw()
