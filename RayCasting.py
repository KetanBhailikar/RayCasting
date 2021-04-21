# Author      : Ketan Bhailikar
# Requrements : 1) Python3.x 
#               2) pygame [https://pypi.org/project/pygame/]
import pygame
import math
import random
pygame.init()

# Variables
screenSize = 500
angleBetweenRays = 0.9     
feildOfView = 40
numberOfWalls = 4

# Ray Class
class ray():
    def __init__(self,angle):
        # angle is in radians
        self.angle = (angle*math.pi)/180
        # slope of the ray
        self.slope = math.tan(angle)

    # this function draws the ray
    def drawLine(self,screen,x,y,walls,k):
        # dmin is the minimum distance where the ray intersects a wall
        dmin = math.sqrt(2) * screenSize

        # epos is the end point of the ray
        epos = (x+(screenSize*math.sqrt(2)*math.cos(self.angle)),y+(screenSize*math.sqrt(2)*math.sin(self.angle)))

        insecs = []     # this array stores all the intersection points of a ray

        # loop through all the walls and get the point of intersection and store it in "insecs"
        for wa in walls:
            if wa.slope != self.slope  :
                inter = getIntersection(x,y,epos[0],epos[1],wa.spos[0],wa.spos[1],wa.epos[0],wa.epos[1])
                if (inter[0] <= max(x, epos[0]) and inter[0] >= min(x, epos[0]) and inter[1] <= max(y, epos[1]) and inter[1] >= min(y, epos[1])) and (inter[0] <= max(wa.spos[0], wa.epos[0]) and inter[0] >= min(wa.spos[0], wa.epos[0]) and inter[1] <= max(wa.spos[1], wa.epos[1]) and inter[1] >= min(wa.spos[1], wa.epos[1])):
                    insecs.append(inter)
        
        # if the ray doesn't intersect any point then just draw it to the end point otherwise draw it to the nearest end point
        if len(insecs) == 0:
            pygame.draw.line(screen,(255,255,255),(x,y),epos)
        else:
            f = -1
            dmin = 1000
            for i in range(len(insecs)):
                d = math.sqrt((y-insecs[i][1])**2+(x-insecs[i][0])**2)
                if d < dmin:
                    dmin = d
                    f = i
            inter = insecs[f]
            pygame.draw.line(screen,(255,255,255),(x,y),inter)
        
        # depending upon the distance of the endpoint, determine the brightness and the height of the corresponding rectangle and draw it
        br = 255 -((dmin/(math.sqrt(2) * screenSize)))*255
        he = screenSize - ((dmin/(math.sqrt(2) * screenSize)))*screenSize
        pygame.draw.rect(screen, (br, br, br), pygame.Rect(screenSize+(k*math.floor(screenSize/(feildOfView/angleBetweenRays))), (screenSize/2)-(he/2),math.floor(screenSize/(feildOfView/angleBetweenRays)),he))


# Wall Class
class wall():
    def __init__(self,c =0):
        # if the value of c is provided then this function makes the wall one of the boundary else it randomly makes a wall
        if c == 1:
            self.spos = (screenSize,0)
            self.epos = (screenSize +0.1,screenSize)
        elif c == 2:
            self.spos = (0,0)
            self.epos = (screenSize,0.1)
        elif c == 3:
            self.spos = (0,0)
            self.epos = (0.1,screenSize)
        elif c ==4 :
            self.spos = (0,screenSize +0.1)
            self.epos = (screenSize,screenSize)
        else:
            self.spos = (random.randint(0,400),random.randint(0,screenSize))
            self.epos = (random.randint(0,400),random.randint(0,screenSize))
        self.slope = (self.epos[1] - self.spos[1])/(self.epos[0] - self.spos[1])
        self.c = self.spos[1] + self.epos[1] - self.slope*(self.spos[0] + self.epos[0]) 

    # draw the wall on the screen
    def drawWall(self,screen):
        pygame.draw.line(screen,(255,255,255),self.spos,self.epos)

# return the intersection point 
def getIntersection(x1,y1,x2,y2,u1,v1,u2,v2):
    x = -1 * ((x1 - x2) * (u1 * v2 - u2 * v1) - (u2 - u1) * (x2 * y1 - x1 * y2)) / ((v1 - v2) * (x1 - x2) - (u2 - u1) * (y2 - y1))
    y = -1 * (u1 * v2 * y1 - u1 * v2 * y2 - u2 * v1 * y1 + u2 * v1 * y2 - v1 * x1 * y2 + v1 * x2 * y1 + v2 * x1 * y2 - v2 * x2 * y1) / (-1 * u1 * y1 + u1 * y2 + u2 * y1 - u2 * y2 + v1 * x1 - v1 * x2 - v2 * x1 + v2 * x2)
    return (x,y)



def main():
    # Initial position
    x = 200
    y = 200

    rays = []       # An array to contain all the ray objects
    walls = []      # An array to contain all the wall objects

    # Adding the four boundaries to the walls array
    b = wall(1)
    walls.append(b)
    b = wall(2)
    walls.append(b)
    b = wall(3)
    walls.append(b)
    b = wall(4)
    walls.append(b)

    # create the rays with a particular angle between them
    a = 1
    while a < feildOfView:
        a+= angleBetweenRays
        rays.append(ray(a))

    # create walls
    for j in range(numberOfWalls):
        walls.append(wall())

    loop = Trues

    # create a wndow of size "screenSize"
    win = pygame.display.set_mode((screenSize*2,screenSize))
    # set its title to "Ray Tracing"
    pygame.display.set_caption("Ray Casting")
    # calculate number of rays
    nofrays = feildOfView//angleBetweenRays

    # game loop
    while loop:
        # current angle of the persons vision is the angle of the center most array 
        currangle = rays[int(nofrays//2)].angle
        ki = pygame.key.get_pressed()

        # set the background to black
        win.fill((0,0,0))

        # panning the view
        for l in range(len(rays)):
            if ki[pygame.K_a]:
                rays[l].angle -= 0.005
            if ki[pygame.K_d]:
                rays[l].angle += 0.005
            
            # draw all the rays if the person is within the right boundry
            if x < screenSize:
                rays[l].drawLine(win,x,y,walls,l)
        
        # draw all the walls
        for w in walls:
            w.drawWall(win)
        
        # exit the game if "X" is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        
        # movement based on the keys pressed
        if ki[pygame.K_RIGHT]:
            x += 0.3*math.cos(currangle + math.pi/2)
            y += 0.3*math.sin(currangle + math.pi/2)
        if ki[pygame.K_LEFT]:
            x += 0.3*math.cos(currangle - math.pi/2)
            y += 0.3*math.sin(currangle - math.pi/2)
        if ki[pygame.K_UP]:
            x += 0.3*math.cos(currangle)
            y += 0.3*math.sin(currangle)
        if ki[pygame.K_DOWN]:
            x -= 0.3*math.cos(currangle)
            y -= 0.3*math.sin(currangle)
        
        # update the display
        pygame.display.flip()

main()
