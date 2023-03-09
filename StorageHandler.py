import AnimHandler
import json

class AnimationStorage:
    def __init__(self):
        pass

    def getJson(self) -> dict:
        return json.load(open("savedAnimations.json"))
    
    def setJson(self, data):
        with open("savedAnimations.json", "w") as output:
            output.write(json.dumps(data))
        
    def getAnimationByName(self, name:str) -> AnimHandler.Animation:
        animStorage = json.load(open("savedAnimations.json"))
        if name in animStorage:
            return animStorage[name]
        return None

storage = AnimationStorage()

def saveAnimation(anim: AnimHandler.Animation) -> bool:
    if storage.getAnimationByName(anim.name) == None:
        store = storage.getJson()
        store[anim.name] = anim.toJson()
        storage.setJson(store)
        return True
    return False

def deleteAnimation(animName: str) -> bool:
    if storage.getAnimationByName(animName) != None:
        store = storage.getJson()
        store.pop(animName)
        storage.setJson(store)
        return True
    return False

def getAnimation(animName: str) -> AnimHandler.Animation:
    animation = storage.getAnimationByName(animName)
    if animation != None:
        author = 0
        if "author" in animation:
            author = animation["author"]
        anim = AnimHandler.Animation(animName, int(author))
        for frame in animation["frames"]:
            anim.addFrame(AnimHandler.Frame(frame["string"], float(frame["duration"])))
        return anim
    return None

def getAllAnimationNames():
    data = storage.getJson()
    names = []
    for name in data:
        names.append(name)
    return names

def getAllAnimationNamesAsString() -> str:
    names = getAllAnimationNames()
    string = ""
    for name in names:
        string += name + "\n"
    return string