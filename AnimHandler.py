import asyncio

class Frame:
    """A part of an animation. Acts as a container
    for a string and the duration for that string
    to be shown.
    """
    def __init__ (self, string: str, time: float):
        self.string = string
        self.duration = time

class Animation:
    """A collection of Frames, responsible for iterating through an animation.
    """
    def __init__(self, name: str):
        self.name = name
        self.frames = []
        self.frame = 0
        self.asyncWait = 0

    def restart(self):
        self.frame = 0

    def addFrame(self, frame: Frame) -> None:
        self.frames.append(frame)

    def getCurrentFrame(self) -> Frame:
        return self.frames[self.frame]

    def hasNextFrame(self) -> bool:
        """Checks if the Animation has more frames.

        Returns:
            bool: true if there is another frame in the animation
        """
        if self.frame < len(self.frames):
            return True
        return False

    def nextFrame(self) -> Frame:
        """Iterates through the animation, and returns the next frame of itself.

        Returns:
            Frame: the next frame of the animation
        """
        currentFrame = None
        if self.frame < len(self.frames):
            currentFrame = self.frames[self.frame]
            self.frame += 1
        return currentFrame
    
    def toJson(self) -> dict:
        data = []
        for frame in self.frames:
            data.append({"string": frame.string, "duration": frame.duration})

        return data
    
def stringToAnimation(name:str, string: str) -> Animation:
    """Attempts to generate an animation given a string

    Args:
        string (str): input, formatted: "[string]^^[duration]|[string]^^[duration]|..."

    Returns:
        Animation: An animation containing the frames
    """
    data = string.split("|")
    anim = Animation(name)
    for frame in data:
        content = frame.split("^^")
        if len(content) < 2:
            content.append("1")
        anim.addFrame(Frame(content[0], float(content[1])))

    return anim