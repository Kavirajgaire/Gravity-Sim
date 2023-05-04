import math
import random
AU = 149.6*10**9
dt = 0.1
G = 6.67*10*-11

class Object:

    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.x_vel = random.uniform(-0.1, 0.1)
        self.y_vel = random.uniform(-0.1, 0.1)

    def apply_collision_force(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        overlap = AU - distance
        
        if overlap > 0:
            theta = math.atan2(dy, dx)
            force_x = math.cos(theta) * overlap * self.x_vel
            force_y = math.sin(theta) * overlap * self.y_vel
            
            return -force_x, -force_y
        return 0, 0

    def updatePos(self, fx, fy):
        
        self.x_vel -= fx / self.mass * dt
        self.y_vel -= fy / self.mass * dt
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt

class QuadTree:
    
    def __init__(self, x, y, w, h, point = None):
        self.x = x
        self.y = y
        self.w= w
        self.h = h
        self.capacity = 4
        self.root = point
        self.subtrees = []
        self.leaf = True
        self.cm = (0, 0)
        self.count = 0
        if self.root:
            self.mass = point.mass
            self.cm = (point.x, point.y)
            self.count = 1
        else:
            self.mass = 0
    
    def correctMass(self, point):
        self.mass += point.mass
        self.count += 1
        self.cm = (self.cm[0] + point.x, self.cm[1] + point.y)
    
    def insert(self, point):
        
        if not self.contains(point.x, point.y, self.w, self.h):
            return False
        if self.leaf:
            if self.root is None:
                self.root = point
                self.correctMass(point)
            else:
                self.split()
                self.insert(point)
        else:
            self.subtrees[self.index(point.x, point.y)].insert(point)
            self.correctMass(point)
        return True
        
    def split(self):
        x = self.x
        y = self.y
        w = self.w/2
        h = self.h / 2

        a = QuadTree(x, y, w, h)
        b = QuadTree(x + w, y, w, h)
        c = QuadTree(x, y + h, w, h)
        d = QuadTree(x + w, y + h, w, h)

        self.subtrees = [a, b, c, d]
        self.leaf = False
        if self.root is not None:
            self.subtrees[self.index(self.root.x, self.root.y)].insert(self.root)
            self.mass = self.root.mass
            self.root = None
    
    def contains(self, x, y, w, h):
        return (x >= self.x - self.w and x <= self.x + self.w + w and
                y >= self.y - self.h and y <= self.y + self.h + h)
    
    def index(self, x, y):
        halfWidth = self.w * 0.5
        if y < self.y + halfWidth:
            if x < self.x + halfWidth:
                return 0
            else:
                return 1
        else:
            if x < self.x + halfWidth:
                return 2
            else:
                return 3
def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def gravity(x1, y1, x2, y2, m1, m2):
        radius = distance(x1, y1, x2, y2)
        if radius > 0.05*AU:
            force = G * m1 * m2 / radius**2
            theta = math.atan2(y2 - y1, x2 - x1)
            force_x = math.cos(theta) * force
            force_y = math.sin(theta) * force
            return force_x, force_y
        return 0, 0

def gravitationalForce(object: Object, tree: QuadTree):
    if tree.leaf:
        if tree.root is None or tree.root == Object:
            return 0, 0
        else:
            return gravity(object.x, object.y, tree.root.x, tree.root.y, object.mass, tree.root.mass)
    elif tree.w / distance(object.x, object.y, tree.cm[0]/tree.count, tree.cm[1]/tree.count) < 0.5:
        return gravity(object.x, object.y, tree.cm[0]/tree.count, tree.cm[1]/tree.count, object.mass, tree.mass)
    else:
        totalx = 0
        totaly = 0
        for i in tree.subtrees:
            x, y = gravitationalForce(object, i)
            totalx += x
            totaly += y
        return totalx, totaly


if __name__ == '__main__':
    tree = QuadTree(0, 0, 1000, 1000)
    tree.insert(Object(0, 0, 1))
    tree.insert(Object(600, 0, 2))
    tree.insert(Object(0, 600, 3))
    tree.insert(Object(600, 600, 4))
    tree.insert(Object(600, 760, 30))
