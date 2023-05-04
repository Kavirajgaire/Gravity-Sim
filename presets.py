from physics import Object, AU
import random

objSize = 0.05* AU

def createCluster(size):
    objects = []
    max = 7*AU
    for i in range(size):
        objects.append(Object(random.randint(0, max), random.randint(0, max), 5.97*10**27))
    return objects