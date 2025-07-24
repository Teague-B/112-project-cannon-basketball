from json import load

def loadFromID(id):

    scene = {
        'id': id
    }
    
    with open("scenes/"+id+".json" as sceneFile):
        scene['objectList'] = load(sceneFile)

    
