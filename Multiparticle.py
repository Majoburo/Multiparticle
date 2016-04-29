import random
import math
import pygame
import pdb
import numpy as np

worldWidth = 900
worldHeight = 900

pygame.init()
screen = pygame.display.set_mode((worldWidth,worldHeight))
clock=pygame.time.Clock()
maxfps=60
font = pygame.font.Font(None,30)
dt=0.05
dt_per_frame = 20
c = 1
G = 40

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
    self.color = np.array([255,255,255])
    self.colorwarp = np.array([0,0,0])
  def update(self, ax, ay, az, dt):
    self.vx=self.vx_+ax*dt
    self.vy=self.vy_+ay*dt
    self.vz=self.vz_+az*dt
    self.x_=self.x_+self.vx_*dt+0.5*ax*dt*dt
    self.y_=self.y_+self.vy_*dt+0.5*ay*dt*dt
    self.z_=self.z_+self.vz_*dt+0.5*az*dt*dt
    # we're on a torus
    if (self.x_<0):          self.x_ += worldWidth
    if (self.x_>worldWidth): self.x_ -= worldWidth
    if (self.y_<0) :         self.y_ += worldHeight
    if (self.y_>worldHeight):self.y_ -= worldHeight
    self.rad=min(self.mass_**(1./3.)*(self.z_/100+1)**(2* np.sign(self.z_)),worldWidth)
    if self.vz_>0:
        self.colorwarp = self.color+(np.array([255,0,0])-self.color)*self.vz_/c
    else:
        self.colorwarp = self.color+(np.array([0,0,255])-self.color)*np.abs(self.vz_)/c
  def render(self):
    pygame.draw.circle(screen,self.colorwarp,(int(self.x_),int(self.y_)),int(self.rad),0)

massPoints = []
for i in range(30):
    massPoints.append(MassPoint(100, random.uniform(worldWidth*0.2, worldWidth*0.8), random.uniform(worldHeight*0.2, worldHeight*0.8), 0, random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-0.3,0.3)))

t=0
while True:
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
          g = G*massPoint2.mass_*massPoint1.mass_/(r**3+10)
          ax = ax + g * (massPoint2.x_-massPoint1.x_)
          ay = ay + g * (massPoint2.y_-massPoint1.y_)
          az = az + g * (massPoint2.z_-massPoint1.z_)
    massPoint1.update(ax, ay, az,dt)
  if (t%dt_per_frame==0):
      for massPoint in massPoints:
        massPoint.render()
      text = font.render("t = %6.4f"%(t*dt), True, (255,255,255))
      screen.blit(text,(20,20))
      pygame.display.flip()
      clock.tick(maxfps)
