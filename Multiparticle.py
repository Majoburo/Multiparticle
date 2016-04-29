import random
import math
import pygame
import pdb
import numpy as np

worldWidth = 900
worldHeight = 900
worldDepth = 3

pygame.init()
screen = pygame.display.set_mode((worldWidth,worldHeight))
done = False
clock=pygame.time.Clock()
maxfps=60
font = pygame.font.Font(None,30)
dt=0.1
class MassPoint:
  def __init__(self, mass, x, y, z, vx, vy, vz):
    self.mass_=mass
    self.x_=x
    self.y_=y
    self.z_=z
    self.vx_=vx
    self.vy_=vy
    self.vz_=vz
    self.rad=mass**(1./3.)
    self.color = (255,255,255)
    self.colorwarp = (0,0,0)
  def update(self, ax, ay, az, dt):
    self.vx=self.vx_+ax*dt
    self.vy=self.vy_+ay*dt
    self.vz=self.vz_+az*dt
    self.x_=self.x_+self.vx_*dt+0.5*ax*dt*dt
    self.y_=self.y_+self.vy_*dt+0.5*ay*dt*dt
    self.z_=self.z_+self.vz_*dt+0.5*az*dt*dt
    # we're on a torus
    if (self.x_<0):
        self.x_ += worldWidth
    if (self.x_>worldWidth):
        self.x_ -= worldWidth
    if (self.y_<0) :
        self.y_ += worldHeight
    if (self.y_>worldHeight) :
        self.y_ -= worldHeight
    self.rad=self.mass_**(1./3.)*(self.z_/100+1)**(2* np.sign(self.z_))
    if self.vz_>0:
        self.colorwarp = self.vz_
    else:
        self.colorwarp = (0,10,10)*z
  def render(self):
    pygame.draw.circle(screen,self.color,(int(self.x_),int(self.y_)),int(self.rad),0)

massPoints = []
for i in range(20):
  massPoints.append(MassPoint(100, random.uniform(worldWidth*0.3, worldWidth*0.7), random.uniform(worldHeight*0.3, worldHeight*0.7), 0, random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-0.1, 0.1)))

t=0
while not done:
  screen.fill((0,0,0))
  t=t+1
  for massPoint1 in massPoints:
    ax = 0
    ay = 0
    az = 0
    for massPoint2 in massPoints:
      if (massPoint2 != massPoint1):
        r = math.sqrt((massPoint2.x_-massPoint1.x_)**2+(massPoint2.y_-massPoint1.y_)**2+(massPoint2.z_-massPoint1.z_)**2)
        if r>0:
          g = 10.*massPoint2.mass_/(r**3+10)
          ax = ax + g * (massPoint2.x_-massPoint1.x_)
          ay = ay + g * (massPoint2.y_-massPoint1.y_)
          az = az + g * (massPoint2.z_-massPoint1.z_)
    massPoint1.update(ax, ay, az,dt)
  for massPoint in massPoints:
    massPoint.render()
  text = font.render("t = %6.4f"%t, True, (255,255,255))
  screen.blit(text,(20,20))
  pygame.display.flip()
  clock.tick(maxfps)
