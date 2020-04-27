import pygame
import math
pygame.init()

screen_x = 800
screen_y = 600
screen = pygame.display.set_mode((screen_x, screen_y))
font = pygame.font.SysFont('Times new roman', 32)
Grad = math.pi/180
bullets = []

goSound1 = pygame.mixer.Sound ("move.wav")
FireSound = pygame.mixer.Sound ("fire.wav")

class Tank():
    def __init__(self, x, y, color, keys, infocoor, speed):
        self.center =[x, y]
        self.size = 20
        self.color = color
        self.degrees = 45
        self.cannondegree = 90
        self.keys = keys
        self.mvu, self.mvd = True, True
        self.ammo = 100
        self.speed = speed
        self.hp, self.score = 10, 0
        self.time = 30
        self.infocoor = infocoor
        self.coordinate =[[self.size*math.cos(self.degrees*Grad)+self.center[0], self.size*math.sin(self.degrees*Grad)+self.center[1]], [self.size*math.cos((self.degrees+90)*Grad)+self.center[0], self.size*math.sin((self.degrees+90)*Grad)+self.center[1]], [self.size*math.cos((self.degrees+180)*Grad)+self.center[0], self.size*math.sin((self.degrees+180)*Grad)+self.center[1]], [self.size*math.cos((self.degrees+270)*Grad)+self.center[0], self.size*math.sin((self.degrees+270)*Grad)+self.center[1]]]
        self.dx = ((self.coordinate[0][0]+self.coordinate[1][0])/2-self.center[0])/self.speed
        self.dy = ((self.coordinate[0][1]+self.coordinate[1][1])/2-self.center[1])/self.speed

    def draw(self):
        if self.hp>0:
            self.coordinate =[[self.size*math.cos(self.degrees*Grad)+self.center[0], self.size*math.sin(self.degrees*Grad)+self.center[1]], [self.size*math.cos((self.degrees+90)*Grad)+self.center[0], self.size*math.sin((self.degrees+90)*Grad)+self.center[1]], [self.size*math.cos((self.degrees+180)*Grad)+self.center[0], self.size*math.sin((self.degrees+180)*Grad)+self.center[1]], [self.size*math.cos((self.degrees+270)*Grad)+self.center[0], self.size*math.sin((self.degrees+270)*Grad)+self.center[1]]]
            pygame.draw.polygon(screen, self.color, self.coordinate, 2)
            pygame.draw.circle(screen, self.color, (int(self.center[0]),int(self.center[1])), self.size//2)
            pygame.draw.line(screen, (255 - self.color[0], 255 - self.color[1], 255 - self.color[2]), ((self.coordinate[1][0]+self.center[0])//2,(self.coordinate[1][1]+self.center[1])//2), ((self.center[0]+(self.coordinate[0][0]+self.coordinate[1][0])/2)//2,(self.center[1]+(self.coordinate[0][1]+self.coordinate[1][1])/2)//2), 2)
            pygame.draw.line(screen, self.color, self.center, (self.center[0]+int(2*self.size*math.cos(self.cannondegree*Grad)), self.center[1]+ 2*self.size*math.sin(self.cannondegree*Grad)), 4)

    def selfinfo(self):
        if self.hp>0:    
            scoretext = font.render('SCORE:' + str(self.score)+ '  HP:'+str(self.hp), True, self.color)
            ammotext = font.render('AMMO:'+ str(self.ammo), True, self.color)
            screen.blit(scoretext, self.infocoor)
            screen.blit(ammotext, (self.infocoor[0], self.infocoor[1]+35))

    def move(self, a):
        if self.hp>0:
            self.coordinate =[[self.size*math.cos(self.degrees*Grad)+self.center[0], self.size*math.sin(self.degrees*Grad)+self.center[1]], [self.size*math.cos((self.degrees+90)*Grad)+self.center[0], self.size*math.sin((self.degrees+90)*Grad)+self.center[1]], [self.size*math.cos((self.degrees+180)*Grad)+self.center[0], self.size*math.sin((self.degrees+180)*Grad)+self.center[1]], [self.size*math.cos((self.degrees+270)*Grad)+self.center[0], self.size*math.sin((self.degrees+270)*Grad)+self.center[1]]]
            self.dx = ((self.coordinate[0][0]+self.coordinate[1][0])/2-self.center[0])/self.speed
            self.dy = ((self.coordinate[0][1]+self.coordinate[1][1])/2-self.center[1])/self.speed
            if self.center[0] < (0-self.size):
                self.center[0] += (screen_x+2*self.size)
            if self.center[1] < (0-self.size):
                self.center[1] += (screen_y+2*self.size)
            if self.center[0] > screen_x+self.size:
                self.center[0] -= (screen_x+2*self.size)
            if self.center[1] > screen_y+self.size:
                self.center[1] -= (screen_y+2*self.size)
            if a == self.keys[0] and self.mvu==True:
                self.center[0] += self.dx
                self.center[1] += self.dy    
                goSound1.play()
            elif a == self.keys[1] and self.mvd==True:
                self.center[0] -= self.dx
                self.center[1] -= self.dy
                goSound1.play()
            elif a == self.keys[2]:
                self.degrees -= 2
                self.cannondegree -= 2
                goSound1.play()
            elif a == self.keys[3]:
                self.degrees += 2
                self.cannondegree += 2
                goSound1.play()
            elif a == self.keys[4]:
                self.cannondegree-=4
            elif a == self.keys[5]:
                self.cannondegree+=4
            elif a == self.keys[6]:
                if self.time>1:
                    self.time=0
                    if self.ammo>0:
                        FireSound.play()
                        b = Bullet(self.center[0]+int(2*self.size*math.cos(self.cannondegree*Grad)), self.center[1]+ 2*self.size*math.sin(self.cannondegree*Grad), self.cannondegree, self.color, self)
                        self.ammo -= 1
                        b.attack = True
                        bullets.append(b)
            self.mvu, self.mvd = True, True
            
class Bullet():
    def __init__(self, x, y, a, color, tank):
        self.x = x
        self.y = y
        self.tank = tank
        self.attack = False
        self.degree = a
        self.time = 5
        self.color = color
        self.radius = 3
    def move(self):
        if self.attack == True:
            self.x+=4*math.cos(self.degree*Grad)
            self.y+=4*math.sin(self.degree*Grad)
        self.draw()
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
def point(x1, y1, x2, y2):
    a = 1
    c = True
    if x2==x1:
        b = y1
        c = False
    else:
        a = (y2-y1)/(x2-x1)
        b = y1-a*x1
    return a, b, c
def ProVer1(x, a, b, c, d):
    e = False 
    e = any((all((x in range(a, b), any((x in range(c, d), x in range(d, c) )) )), all((x in range(b, a), any((x in range(c, d), x in range(d, c) )) )) ))
    return e
def ProVer2(x, y ,a, b, c, d):
    otvet = False
    otvet = any((all((x in range(a, b), any((y in range(c, d), y in range(d, c) )) )),all((x in range(b, a), any((y in range(c, d), y in range(d, c) )) )) ))
    return otvet
    
tank1 = Tank(200, 300, (255, 0, 0), (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e, pygame.K_SPACE), (10, 10), 5)
tank2 = Tank(600, 300, (0, 255, 0),(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_MINUS, pygame.K_PLUS, pygame.K_l), (screen_x-270, 10), 5)

tanks = [tank1, tank2]

run = True
FPS = 30
clock = pygame.time.Clock()

while run:
    mill = clock.tick(FPS)
    second = mill/1000
    pressed = pygame.key.get_pressed()
    for i in range(len(tanks)):
        for j in range(len(tanks)):
            if tanks[i] != tanks[j]:
                if (tanks[i].center[0]-tanks[j].center[0]+tanks[i].dx)**2+(tanks[i].center[1]-tanks[j].center[1]+tanks[i].dy)**2<(tanks[i].size+tanks[j].size)**2:
                    tanks[i].mvu = False
                if (tanks[i].center[0]-tanks[j].center[0]-tanks[i].dx)**2+(tanks[i].center[1]-tanks[j].center[1]-tanks[i].dy)**2<(tanks[i].size+tanks[j].size)**2:
                    tanks[i].mvd = False
    for i in range(0,len(bullets)-1):
        for j in range(i+1, len(bullets)):
            try:
                if (bullets[i].x-bullets[j].x)**2+(bullets[i].y-bullets[j].y)**2<=(bullets[i].radius+bullets[j].radius)**2 and bullets[i].tank!=bullets[j].tank:
                    bullets.pop(i)
                    bullets.pop(j-1)
            except IndexError:
                print('',end='')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in range(len(bullets)):
        for tank in tanks:
            a1, b1, c = point(tank.coordinate[0][0],tank.coordinate[0][1],tank.coordinate[1][0],tank.coordinate[1][1])
            a2, b2, d = point(tank.coordinate[1][0],tank.coordinate[1][1],tank.coordinate[2][0],tank.coordinate[2][1])
            a3, b3, c = point(tank.coordinate[2][0],tank.coordinate[2][1],tank.coordinate[3][0],tank.coordinate[3][1])
            a4, b4, d = point(tank.coordinate[3][0],tank.coordinate[3][1],tank.coordinate[0][0],tank.coordinate[0][1])
            if all((c, d)) == True:
                try:
                    e = ProVer1(int(100*bullets[i].x), int(100*(bullets[i].y-b3)//a3), int(100*(bullets[i].y-b1)//a1), int(100*(bullets[i].y-b2)//a2), int(100*(bullets[i].y-b4)//a4))
                    if e == True:
                        bullets[i].tank.score+=1
                        bullets.pop(i)
                        tank.hp -=1
                except ZeroDivisionError:
                    print('', end='')
                except  IndexError:
                    print('', end='')
            else:
                try:
                    if ProVer2(int(100*bullets[i].x), int(100*bullets[i].y), int(100*tank.coordinate[0][0]),int(100*tank.coordinate[2][0]), int(100*tank.coordinate[0][1]), int(100*tank.coordinate[2][1])) == True:
                        bullets[i].tank.score+=1
                        bullets.pop(i)
                        tank.hp -=1
                except IndexError:
                    print('', end='')
        try:
            if bullets[i].tank.hp<=0:
                bullets.pop(i)
        except IndexError:
            print('', end='')
    if pressed[pygame.K_ESCAPE]: run = False
    try:
        for i in range(len(bullets)):
            bullets[i].time-=second
            if bullets[i].time<0:
                bullets.pop(i)
    except IndexError:
        print('', end='')
    for tank in tanks:
        for a in tank.keys:
            if pressed[a]==True:
                tank.move(a)
    screen.fill((50, 50, 50))
    try:    
        for i in range (len(tanks)):
            if tanks[i].hp<=0:
                tanks.pop(i)
            tanks[i].time += second
            tanks[i].draw()
            tanks[i].selfinfo()
    except IndexError:
            print('', end='')
    for bullet in bullets:
        bullet.move()
    pygame.display.flip()
pygame.quit()