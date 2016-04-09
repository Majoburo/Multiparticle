from Tkinter import *
import random
import math

worldWidth = 500
worldHeight = 500

tk = Tk()
canvas = Canvas(tk, width = worldWidth, height = worldHeight)
tk.title("souvik's gravity simulator")
canvas.pack()

class MassPoint:
  def __init__(self, mass, x, y, z, vx, vy, vz):
    self.mass_=mass
    self.x_=x
    self.y_=y
    self.z_=z
    self.vx_=vx
    self.vy_=vy
    self.vz_=vz
    rad=mass**(1./3.)
    self.shape=canvas.create_oval(self.x_-rad/2, self.y_-rad/2, self.x_+rad/2, self.y_+rad/2, fill="orange")
    
  def update1(self, ax, ay, az, dt):
    self.vx_new=self.vx_+ax*dt
    self.vy_new=self.vy_+ay*dt
    self.vz_new=self.vz_+az*dt
    self.x_new=self.x_+self.vx_*dt+0.5*ax*dt*dt
    self.y_new=self.y_+self.vy_*dt+0.5*ay*dt*dt
    self.z_new=self.z_+self.vz_*dt+0.5*az*dt*dt
    if (self.x_new<0 or self.x_new>worldWidth):
      self.vx_new=-self.vx_new;
    if (self.y_new<0 or self.y_new>worldHeight):
      self.vy_new=-self.vy_new;
    
  def update2(self):
    canvas.move(self.shape, self.x_new-self.x_, self.y_new-self.y_)
    self.vx_=self.vx_new
    self.vy_=self.vy_new
    self.vz_=self.vz_new
    self.x_=self.x_new
    self.y_=self.y_new
    self.z_=self.z_new
    
  def render(self):
    canvas.coords(self.x_, self.y_)
    
massPoints = []
for i in range(10):
  massPoints.append(MassPoint(1, random.randrange(worldWidth*0.3, worldWidth*0.7), random.randrange(worldHeight*0.3, worldHeight*0.7), 0, random.randrange(-10, 10), random.randrange(-10, 10), random.randrange(-5, 5)))

#massPoints.append(MassPoint(1000, worldWidth*0.5, worldHeight*0.5, 0, 0, 0, 0))
#massPoints.append(MassPoint(10, 500, 350, 0, 0, 7, 0))

t=0
while True:
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
    massPoint1.update1(ax, ay, az, 0.01)
    
  for massPoint in massPoints:  
    massPoint.update2()
    
  if (t%1==0):
    for massPoint in massPoints:
      massPoint.render()
    tk.update()

