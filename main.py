import pygame
from physics import *
import presets
screen_width = 800
screen_height = 600
objSize = 0.05* AU
scale = 250 / AU

screen = pygame.display.set_mode((screen_width, screen_height))
preset = presets.createCluster(50)

showTree = False
includePreset = True

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scale = 1
    def update(self, x, y):
        self.x -= x
        self.y -= y
        

def draw_screen(camera, objects):
    for obj in objects:
        #print(camera.x, camera.y)
        #print('a: ', obj.x, obj.y)
        rect = pygame.Rect((obj.x - camera.x - objSize // 2)*camera.scale*scale, (obj.y - camera.y - objSize // 2)*camera.scale*scale, objSize*camera.scale*scale, objSize*camera.scale*scale)
        pygame.draw.rect(screen, (255, 0, 0), rect)

def updatePos(objects):
    if len(objects) > 0:
        minx = min([obj.x for obj in objects])
        maxx = max([obj.x for obj in objects])
        miny = min([obj.y for obj in objects])
        maxy = max([obj.y for obj in objects])
        tree = QuadTree(minx, miny, maxx - minx, maxy - miny)
        for obj in objects:
            #print(obj.x_vel, obj.y_vel)
            tree.insert(obj)
        for obj in objects:
            x, y = gravitationalForce(obj, tree)
            obj.updatePos(x, y)
        return tree

def drawTree(tree, camera):
    if tree.leaf:
       rect = pygame.Rect((tree.x - camera.x)*camera.scale*scale, (tree.y - camera.y )*camera.scale*scale, tree.w*camera.scale*scale, tree.h*camera.scale*scale)
       pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    else:
        if tree.mass > 0:
            #print(tree.cm[0]/ tree.count - camera.x, tree.cm[1]/tree.count - camera.y)
            cm = pygame.Rect((tree.cm[0]/ tree.count - camera.x)*camera.scale*scale - 2.5*camera.scale, (tree.cm[1]/tree.count - camera.y)*camera.scale*scale - 2.5*camera.scale, 5*camera.scale, 5*camera.scale)
            pygame.draw.rect(screen, (0, 255, 0), cm)
        for i in tree.subtrees:
            drawTree(i, camera)



def Render_Text(what, color, where):
    font = pygame.font.SysFont('Verdana', 30)
    text = font.render(what, 1, pygame.Color(color))
    screen.blit(text, where)
    


def cleanUp(objects, camera):
    for i in objects:
        if distance(i.x, i.y, camera.x, camera.y) > 25 * AU:
            objects.remove(i)

def main():

    objects = []
    if includePreset:
        objects.extend(preset)
    camera = Camera()

    running = True
    isDragging = False
    dragStartPos = None
    

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == pygame.BUTTON_RIGHT:
                    mousePos = pygame.mouse.get_pos()
                    obj = Object(mousePos[0]//(camera.scale*scale) + camera.x ,  mousePos[1]//(camera.scale*scale) + camera.y, 5.97*10**27)
                    objects.append(obj)
                if event.button == pygame.BUTTON_LEFT:
                    isDragging = True
                    dragStartPos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    camera.update((pygame.mouse.get_pos()[0] - dragStartPos[0])//(camera.scale*scale), (pygame.mouse.get_pos()[1] - dragStartPos[1])//(camera.scale*scale))
                    isDragging = False
                    dragStartPos = None
            elif event.type == pygame.MOUSEMOTION and isDragging:
                
                camera.update((pygame.mouse.get_pos()[0] - dragStartPos[0])//(camera.scale*scale), (pygame.mouse.get_pos()[1] - dragStartPos[1])//(camera.scale*scale))
                dragStartPos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and camera.scale < 3:
                    camera.scale += 0.25
                elif event.key == pygame.K_e and camera.scale > 0.25:
                    camera.scale -= 0.25                        

        
        # for obj in objects:
        #     obj.update_positions(objects)
        cleanUp(objects, camera)
        
        tree = updatePos(objects)
        if showTree and tree:
            drawTree(tree, camera)
        draw_screen(camera, objects)
        Render_Text(str(int(clock.get_fps())), (255,0,0), (0,0))
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    main()