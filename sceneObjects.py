import drawing

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

class Drawable:
    def draw(self):
        pass

class Location:
    x, y = 0, 0

class Circle(Location):
    r = 0.5

    def __init__(self, x, y, r):
        super(x, y)
        self.r = r

class Rectangle(Location):
    w, h = 0.5, 0.5

    def __init__(self, x, y, w, h, rotation):
        super(x, y)
        self.w = w
        self.h = h
        self.rotation = rotation
    
    def isTouchingRect(self, other):
        if not isinstance(other, Rectangle):
            assert False, "Idfk man that's not a rectangle"
    
        if self.x >= other.x + other.width or other.x >= self.x + self.width or self.y - self.height >= other.y or other.y - other.height >= self.y:
            return False
        return True


    # This is gonna be trashed, our rectangles are possibly
    # rotated
    def isTouchingCircle(self, other):
        assert isinstance(other, Circle), "Expected Circle"

        
        left = self.x,
        right = self.x + self.w
        top = self.y
        bottom = self.y + self.h

        closestX = max(left, min(other.x, right))
        closestY = max(top, min(other.y, bottom))

        dx = other.x - closestX
        dy = other.y - closestY

        return (dx*dx + dy*dy) <= (other.r * other.r)


class Wall(Rectangle):
    def __init__(self, x, y, w, h, rotation=0, fill='black'):
        super(x, y, w, h, rotation)
        self.fill = fill