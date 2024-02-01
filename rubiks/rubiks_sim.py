'''
Rubik's Cube Simulator
129L Final Project
Author: Blake Chellew
'''

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import queue

#Cube class: each of the 26 smaller cubes is an instance of this class
class Cube:

    #coordinates are center of cube
    def __init__(self, x, y, z, num, ax):

        self.ax = ax
        #starting positions
        self.x0 = x
        self.y0 = y
        self.z0 = z
        #current positions
        self.x = x
        self.y = y
        self.z = z
        self.thx = 0
        self.thy = 0
        self.thz = 0
        #face colors
        self.colors = {
            'front': 'b',
            'back': 'g',
            'left': 'orange',
            'right': 'r',
            'top': 'y',
            'bottom': 'w',
        }
        #initialize matplotlib 3D objects
        verts_0 = [[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]]
        self.front_face = Poly3DCollection(verts_0, facecolors=self.colors['front'])
        self.back_face = Poly3DCollection(verts_0, facecolors=self.colors['back'])
        self.left_face = Poly3DCollection(verts_0, facecolors=self.colors['left'])
        self.right_face = Poly3DCollection(verts_0, facecolors=self.colors['right'])
        self.top_face = Poly3DCollection(verts_0, facecolors=self.colors['top'])
        self.bottom_face = Poly3DCollection(verts_0, facecolors=self.colors['bottom'])
        self.ax.add_collection3d(self.front_face, zs='z')
        self.ax.add_collection3d(self.back_face, zs='z')
        self.ax.add_collection3d(self.left_face, zs='z')
        self.ax.add_collection3d(self.right_face, zs='z')
        self.ax.add_collection3d(self.top_face, zs='z')
        self.ax.add_collection3d(self.bottom_face, zs='z')

        #set radius (relative to center of face) (1 for edge pieces, sqrt(2) for corners)
        rads = np.array([self.x-1, self.y-1, self.z-1]) #better name
        num_zeros = len(rads[rads==0])
        if num_zeros == 2:
            self.r = 0
        elif num_zeros == 1:
            self.r = 1
        else:
            self.r = np.sqrt(2)

    #update the position of the cube's vertices
    def display(self):
        if self.thy != 0:
            #front face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thy), \
                  self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thy)]
            ys = [self.y-0.5, self.y-0.5, self.y-0.5, self.y-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thy), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thy)]
            verts1 = [list(zip(xs, ys, zs))]
            #back face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thy), \
                  self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thy)]
            ys = [self.y+0.5, self.y+0.5, self.y+0.5, self.y+0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thy), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thy)]
            verts2 = [list(zip(xs, ys, zs))]
            #left face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thy), \
                  self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thy)]
            ys = [self.y+0.5, self.y+0.5, self.y-0.5, self.y-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thy), \
                  self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thy)]
            verts3 = [list(zip(xs, ys, zs))]
            #right face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thy), \
                  self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thy)]
            ys = [self.y+0.5, self.y+0.5, self.y-0.5, self.y-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thy), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thy)]
            verts4 = [list(zip(xs, ys, zs))]
            #bottom face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thy) \
                  , self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thy)]
            ys = [self.y-0.5, self.y+0.5, self.y+0.5, self.y-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thy) \
                  , self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thy)]
            verts5 = [list(zip(xs, ys, zs))]
            #top face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thy) \
                  , self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thy), self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thy)]
            ys = [self.y-0.5, self.y+0.5, self.y+0.5, self.y-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thy), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thy), self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thy)]
            verts6 = [list(zip(xs, ys, zs))]

        elif self.thx != 0:
            #front face
            ys = [self.y+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thx), \
                  self.y+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thx)]
            xs = [self.x+0.5, self.x+0.5, self.x-0.5, self.x-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thx), \
                  self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thx)]
            verts1 = [list(zip(xs, ys, zs))]
            #back face
            ys = [self.y+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thx), \
                  self.y+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thx)]
            xs = [self.x+0.5, self.x+0.5, self.x-0.5, self.x-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thx), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thx)]
            verts2 = [list(zip(xs, ys, zs))]
            #left face
            ys = [self.y+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thx), \
                  self.y+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thx)]
            xs = [self.x-0.5, self.x-0.5, self.x-0.5, self.x-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thx), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thx)]
            verts3 = [list(zip(xs, ys, zs))]
            #right face
            ys = [self.y+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thx), \
                  self.y+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thx)]
            xs = [self.x+0.5, self.x+0.5, self.x+0.5, self.x+0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thx), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thx)]
            verts4 = [list(zip(xs, ys, zs))]
            #bottom face
            ys = [self.y+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(5*np.pi/4 + self.thx) \
                  , self.y+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(-np.pi/4 + self.thx)]
            xs = [self.x-0.5, self.x+0.5, self.x+0.5, self.x-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(5*np.pi/4 + self.thx) \
                  , self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(-np.pi/4 + self.thx)]
            verts5 = [list(zip(xs, ys, zs))]
            #top face
            ys = [self.y+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(3*np.pi/4 + self.thx) \
                  , self.y+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thx), self.y+(np.sqrt(2)/2)*np.cos(np.pi/4 + self.thx)]
            xs = [self.x-0.5, self.x+0.5, self.x+0.5, self.x-0.5]
            zs = [self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(3*np.pi/4 + self.thx), \
                  self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thx), self.z+(np.sqrt(2)/2)*np.sin(np.pi/4 + self.thx)]
            verts6 = [list(zip(xs, ys, zs))]

        #final else will execute also when all angles are 0 (no rotation)
        else:
            #front face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 - self.thz) \
                  , self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 - self.thz)]
            zs = [self.z-0.5, self.z+0.5, self.z+0.5, self.z-0.5]
            ys = [self.y+(np.sqrt(2)/2)*np.sin(5*np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(5*np.pi/4 - self.thz) \
                  , self.y+(np.sqrt(2)/2)*np.sin(-np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(-np.pi/4 - self.thz)]
            verts1 = [list(zip(xs, ys, zs))]
            #back face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 - self.thz) \
                  , self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 - self.thz)]
            zs = [self.z-0.5, self.z+0.5, self.z+0.5, self.z-0.5]
            ys = [self.y+(np.sqrt(2)/2)*np.sin(3*np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(3*np.pi/4 - self.thz), \
                  self.y+(np.sqrt(2)/2)*np.sin(np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(np.pi/4 - self.thz)]
            verts2 = [list(zip(xs, ys, zs))]
            #left face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 - self.thz), \
                  self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 - self.thz)]
            zs = [self.z+0.5, self.z+0.5, self.z-0.5, self.z-0.5]
            ys = [self.y+(np.sqrt(2)/2)*np.sin(5*np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(3*np.pi/4 - self.thz), \
                  self.y+(np.sqrt(2)/2)*np.sin(3*np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(5*np.pi/4 - self.thz)]
            verts3 = [list(zip(xs, ys, zs))]
            #right face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 - self.thz), \
                  self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 - self.thz)]
            zs = [self.z+0.5, self.z+0.5, self.z-0.5, self.z-0.5]
            ys = [self.y+(np.sqrt(2)/2)*np.sin(-np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(np.pi/4 - self.thz), \
                  self.y+(np.sqrt(2)/2)*np.sin(np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(-np.pi/4 - self.thz)]
            verts4 = [list(zip(xs, ys, zs))]
            #bottom face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 - self.thz), \
                  self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 - self.thz)]
            zs = [self.z-0.5, self.z-0.5, self.z-0.5, self.z-0.5]
            ys = [self.y+(np.sqrt(2)/2)*np.sin(5*np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(3*np.pi/4 - self.thz), \
                  self.y+(np.sqrt(2)/2)*np.sin(np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(-np.pi/4 - self.thz)]
            verts5 = [list(zip(xs, ys, zs))]
            #top face
            xs = [self.x+(np.sqrt(2)/2)*np.cos(5*np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(3*np.pi/4 - self.thz), \
                  self.x+(np.sqrt(2)/2)*np.cos(np.pi/4 - self.thz), self.x+(np.sqrt(2)/2)*np.cos(-np.pi/4 - self.thz)]
            zs = [self.z+0.5, self.z+0.5, self.z+0.5, self.z+0.5]
            ys = [self.y+(np.sqrt(2)/2)*np.sin(5*np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(3*np.pi/4 - self.thz), \
                  self.y+(np.sqrt(2)/2)*np.sin(np.pi/4 - self.thz), self.y+(np.sqrt(2)/2)*np.sin(-np.pi/4 - self.thz)]
            verts6 = [list(zip(xs, ys, zs))]

        #update vertices:
        self.front_face.set_verts(verts1)
        self.back_face.set_verts(verts2)
        self.left_face.set_verts(verts3)
        self.right_face.set_verts(verts4)
        self.bottom_face.set_verts(verts5)
        self.top_face.set_verts(verts6)
        #update face colors:
        self.front_face.set_facecolor(self.colors['front'])
        self.back_face.set_facecolor(self.colors['back'])
        self.top_face.set_facecolor(self.colors['top'])
        self.bottom_face.set_facecolor(self.colors['bottom'])
        self.left_face.set_facecolor(self.colors['left'])
        self.right_face.set_facecolor(self.colors['right'])  

        
class Rubiks:
    def __init__(self):
        self.num_frames = 10 #frames per face rotation
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)
        self.ax.view_init(elev=20, azim=240) #initialize viewing angle
        #set axis limits and labels
        self.ax.set_xlim(-1, 3)
        self.ax.set_ylim(-1, 3)
        self.ax.set_zlim(-1, 3)
        plt.axis("off")
        #self.ax.set_xlabel("x")
        #self.ax.set_ylabel("y")
        #self.ax.set_zlabel("z")
        #buttons: positions and corresponding functions
        self.button_ax_F = self.fig.add_axes([0, 0.075, 0.1, 0.075])
        self.bF = Button(self.button_ax_F, 'F')
        self.bF.on_clicked(self.F_button)
        self.button_ax_R = plt.axes([0.1, 0.075, 0.1, 0.075])
        self.bR = Button(self.button_ax_R, 'R')
        self.bR.on_clicked(self.R_button)
        self.button_ax_U = plt.axes([0.2, 0.075, 0.1, 0.075])
        self.bU = Button(self.button_ax_U, 'U')
        self.bU.on_clicked(self.U_button)
        self.button_ax_B = plt.axes([0.3, 0.075, 0.1, 0.075])
        self.bB = Button(self.button_ax_B, 'B')
        self.bB.on_clicked(self.B_button)
        self.button_ax_L = plt.axes([0.4, 0.075, 0.1, 0.075])
        self.bL = Button(self.button_ax_L, 'L')
        self.bL.on_clicked(self.L_button)
        self.button_ax_D = plt.axes([0.5, 0.075, 0.1, 0.075])
        self.bD = Button(self.button_ax_D, 'D')
        self.bD.on_clicked(self.D_button)
        self.button_ax_FP = plt.axes([0, 0, 0.1, 0.075])
        self.bFP = Button(self.button_ax_FP, 'F\'')
        self.bFP.on_clicked(self.FP_button)
        self.button_ax_RP = plt.axes([0.1, 0, 0.1, 0.075])
        self.bRP = Button(self.button_ax_RP, 'R\'')
        self.bRP.on_clicked(self.RP_button)
        self.button_ax_UP = plt.axes([0.2, 0, 0.1, 0.075])
        self.bUP = Button(self.button_ax_UP, 'U\'')
        self.bUP.on_clicked(self.UP_button)
        self.button_ax_BP = plt.axes([0.3, 0, 0.1, 0.075])
        self.bBP = Button(self.button_ax_BP, 'B\'')
        self.bBP.on_clicked(self.BP_button)
        self.button_ax_LP = plt.axes([0.4, 0, 0.1, 0.075])
        self.bLP = Button(self.button_ax_LP, 'L\'')
        self.bLP.on_clicked(self.LP_button)
        self.button_ax_DP = plt.axes([0.5, 0, 0.1, 0.075])
        self.bDP = Button(self.button_ax_DP, 'D\'')
        self.bDP.on_clicked(self.DP_button)
        self.button_ax_rand = plt.axes([0.8, 0, 0.2, 0.075])
        self.brand = Button(self.button_ax_rand, 'Randomize')
        self.brand.on_clicked(self.randomize_button)
        self.button_ax_reset = plt.axes([0.8, 0.075, 0.2, 0.075])
        self.breset = Button(self.button_ax_reset, 'Reset')
        self.breset.on_clicked(self.reset_button)
        self.button_ax_super = plt.axes([0.8, 0.15, 0.2, 0.075])
        self.bsuper = Button(self.button_ax_super, 'Superflip')
        self.bsuper.on_clicked(self.super_button)
        #button queue:
        self.busy = 0
        self.q = queue.Queue()

        #create cubes with side length 1
        self.cubes = []
        self.cubes.append(Cube(0, 0, 0, 0, self.ax))
        self.cubes.append(Cube(1, 0, 0, 1, self.ax))
        self.cubes.append(Cube(2, 0, 0, 2, self.ax))
        self.cubes.append(Cube(0, 0, 1, 3, self.ax))
        self.cubes.append(Cube(1, 0, 1, 4, self.ax))
        self.cubes.append(Cube(2, 0, 1, 5, self.ax))
        self.cubes.append(Cube(0, 0, 2, 6, self.ax))
        self.cubes.append(Cube(1, 0, 2, 7, self.ax))
        self.cubes.append(Cube(2, 0, 2, 8, self.ax))
        self.cubes.append(Cube(0, 1, 0, 9, self.ax))
        self.cubes.append(Cube(1, 1, 0, 10, self.ax))
        self.cubes.append(Cube(2, 1, 0, 11, self.ax))
        self.cubes.append(Cube(0, 1, 1, 12, self.ax))
        self.cubes.append(Cube(2, 1, 1, 13, self.ax))
        self.cubes.append(Cube(0, 1, 2, 14, self.ax))
        self.cubes.append(Cube(1, 1, 2, 15, self.ax))
        self.cubes.append(Cube(2, 1, 2, 16, self.ax))
        self.cubes.append(Cube(0, 2, 0, 17, self.ax))
        self.cubes.append(Cube(1, 2, 0, 18, self.ax))
        self.cubes.append(Cube(2, 2, 0, 19, self.ax))
        self.cubes.append(Cube(0, 2, 1, 20, self.ax))
        self.cubes.append(Cube(1, 2, 1, 21, self.ax))
        self.cubes.append(Cube(2, 2, 1, 22, self.ax))
        self.cubes.append(Cube(0, 2, 2, 23, self.ax))
        self.cubes.append(Cube(1, 2, 2, 24, self.ax))
        self.cubes.append(Cube(2, 2, 2, 25, self.ax))
        self.cubes = np.array(self.cubes)

    #reset positions of each cube to default
    #colors are updated elsewhere so cube does not appear to actually reset
    def reset(self):
        for c in self.cubes:
            c.x = c.x0
            c.y = c.y0
            c.z = c.z0
            c.thx = 0
            c.thy = 0
            c.thz = 0

    #call display function on each of the smaller cubes
    def display(self):
        for c in self.cubes:
            c.display()
        plt.pause(0.001)

    #rotate front face
    def F(self, cw = 1):
        self.busy = 1
        ind = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        cubes = self.cubes[ind]
        #display frames
        for i in range(1, self.num_frames+1):
            d_th = i*np.pi/(2*self.num_frames)
            if cw == 1:
                d_th = -d_th
            for c in cubes:
                try:
                    if c.z0 > 0:
                        angle = np.arccos((c.x0-1)/c.r) + d_th    
                    else:
                        angle = -np.arccos((c.x0-1)/c.r) + d_th
                    c.x = 1 + c.r*np.cos(angle)
                    c.z = 1 + c.r*np.sin(angle) 
                except: #happens when r = 0:
                    pass
                c.thy = d_th
            self.display()
        #update colors and reset
        if cw == 1: #clockwise
            for c in cubes:
                temp = c.colors['right']
                c.colors['right'] = c.colors['top']
                c.colors['top'] = c.colors['left']
                c.colors['left'] = c.colors['bottom']
                c.colors['bottom'] = temp
            #corners
            temp = self.cubes[6].colors
            self.cubes[6].colors = self.cubes[0].colors
            self.cubes[0].colors = self.cubes[2].colors
            self.cubes[2].colors = self.cubes[8].colors
            self.cubes[8].colors = temp
            #edges
            temp = self.cubes[7].colors
            self.cubes[7].colors = self.cubes[3].colors
            self.cubes[3].colors = self.cubes[1].colors
            self.cubes[1].colors = self.cubes[5].colors
            self.cubes[5].colors = temp
        else: #counter-clockwise
            for c in cubes:
                temp = c.colors['right']
                c.colors['right'] = c.colors['bottom']
                c.colors['bottom'] = c.colors['left']
                c.colors['left'] = c.colors['top']
                c.colors['top'] = temp
            #corners
            temp = self.cubes[6].colors
            self.cubes[6].colors = self.cubes[8].colors
            self.cubes[8].colors = self.cubes[2].colors
            self.cubes[2].colors = self.cubes[0].colors
            self.cubes[0].colors = temp
            #edges
            temp = self.cubes[7].colors
            self.cubes[7].colors = self.cubes[5].colors
            self.cubes[5].colors = self.cubes[1].colors
            self.cubes[1].colors = self.cubes[3].colors
            self.cubes[3].colors = temp
        self.reset()
        self.busy = 0

    #rotate right face
    def R(self, cw = 1):
        self.busy = 1
        ind = [2, 5, 8, 11, 13, 16, 19, 22, 25]
        cubes = self.cubes[ind]
        for i in range(1, self.num_frames+1):
            d_th = i*np.pi/(2*self.num_frames)
            if cw == 1:
                d_th = -d_th
            for c in cubes:
                try:
                    if c.z0 > 0:
                        angle = np.arccos((c.y0-1)/c.r) + d_th    
                    else:
                        angle = -np.arccos((c.y0-1)/c.r) + d_th
                    c.y = 1 + c.r*np.cos(angle)
                    c.z = 1 + c.r*np.sin(angle)
                except: #happens when r = 0
                    pass
                c.thx = d_th 
            self.display()
        #update colors and reset
        if cw == 1: #clockwise
            for c in cubes:
                temp = c.colors['front']
                c.colors['front'] = c.colors['bottom']
                c.colors['bottom'] = c.colors['back']
                c.colors['back'] = c.colors['top']
                c.colors['top'] = temp
            #corners
            temp = self.cubes[8].colors
            self.cubes[8].colors = self.cubes[2].colors
            self.cubes[2].colors = self.cubes[19].colors
            self.cubes[19].colors = self.cubes[25].colors
            self.cubes[25].colors = temp
            #edges
            temp = self.cubes[16].colors
            self.cubes[16].colors = self.cubes[5].colors
            self.cubes[5].colors = self.cubes[11].colors
            self.cubes[11].colors = self.cubes[22].colors
            self.cubes[22].colors = temp
        else: #counter-clockwise
            for c in cubes:
                temp = c.colors['front']
                c.colors['front'] = c.colors['top']
                c.colors['top'] = c.colors['back']
                c.colors['back'] = c.colors['bottom']
                c.colors['bottom'] = temp
            #corners
            temp = self.cubes[8].colors
            self.cubes[8].colors = self.cubes[25].colors
            self.cubes[25].colors = self.cubes[19].colors
            self.cubes[19].colors = self.cubes[2].colors
            self.cubes[2].colors = temp
            #edges
            temp = self.cubes[16].colors
            self.cubes[16].colors = self.cubes[22].colors
            self.cubes[22].colors = self.cubes[11].colors
            self.cubes[11].colors = self.cubes[5].colors
            self.cubes[5].colors = temp
        self.reset()
        self.busy = 0

    #rotate left face
    def L(self, cw = 1):
        self.busy = 1
        ind = [0, 3, 6, 9, 12, 14, 17, 20, 23]
        cubes = self.cubes[ind]
        for i in range(1, self.num_frames+1):
            d_th = i*np.pi/(2*self.num_frames)
            if cw == 0:
                d_th = - d_th
            for c in cubes:
                try:
                    if c.z0 > 0:
                        angle = np.arccos((c.y0-1)/c.r) + d_th    
                    else:
                        angle = -np.arccos((c.y0-1)/c.r) + d_th
                    c.y = 1 + c.r*np.cos(angle)
                    c.z = 1 + c.r*np.sin(angle)
                except: #happens when r = 0:
                    pass
                c.thx = d_th
            self.display()
        #update colors and reset
        if cw == 1: #clockwise
            for c in cubes:
                temp = c.colors['front']
                c.colors['front'] = c.colors['top']
                c.colors['top'] = c.colors['back']
                c.colors['back'] = c.colors['bottom']
                c.colors['bottom'] = temp
            #corners
            temp = self.cubes[6].colors
            self.cubes[6].colors = self.cubes[23].colors
            self.cubes[23].colors = self.cubes[17].colors
            self.cubes[17].colors = self.cubes[0].colors
            self.cubes[0].colors = temp
            #edges
            temp = self.cubes[3].colors
            self.cubes[3].colors = self.cubes[14].colors
            self.cubes[14].colors = self.cubes[20].colors
            self.cubes[20].colors = self.cubes[9].colors
            self.cubes[9].colors = temp
        else: #counter-clockwise
            for c in cubes:
                temp = c.colors['front']
                c.colors['front'] = c.colors['bottom']
                c.colors['bottom'] = c.colors['back']
                c.colors['back'] = c.colors['top']
                c.colors['top'] = temp
            #corners
            temp = self.cubes[6].colors
            self.cubes[6].colors = self.cubes[0].colors
            self.cubes[0].colors = self.cubes[17].colors
            self.cubes[17].colors = self.cubes[23].colors
            self.cubes[23].colors = temp
            #edges
            temp = self.cubes[3].colors
            self.cubes[3].colors = self.cubes[9].colors
            self.cubes[9].colors = self.cubes[20].colors
            self.cubes[20].colors = self.cubes[14].colors
            self.cubes[14].colors = temp
        self.reset()
        self.busy = 0

    #rotate up face
    def U(self, cw=1):
        self.busy = 1
        ind = [6, 7, 8, 14, 15, 16, 23, 24, 25]
        cubes = self.cubes[ind]
        for i in range(1, self.num_frames+1):
            d_th = i*np.pi/(2*self.num_frames)
            if cw == 1:
                d_th = -d_th
            for c in cubes:
                try:
                    if c.y0 > 0:
                        angle = np.arccos((c.x0-1)/c.r) + d_th    
                    else:
                        angle = -np.arccos((c.x0-1)/c.r) + d_th
                    c.x = 1 + c.r*np.cos(angle)
                    c.y = 1 + c.r*np.sin(angle)
                except: #happens when r = 0
                    pass
                c.thz = -d_th
            self.display()
        #update colors and reset
        if cw == 1: #clockwise
            for c in cubes:
                temp = c.colors['front']
                c.colors['front'] = c.colors['right']
                c.colors['right'] = c.colors['back']
                c.colors['back'] = c.colors['left']
                c.colors['left'] = temp
            #corners
            temp = self.cubes[23].colors
            self.cubes[23].colors = self.cubes[6].colors
            self.cubes[6].colors = self.cubes[8].colors
            self.cubes[8].colors = self.cubes[25].colors
            self.cubes[25].colors = temp
            #edges
            temp = self.cubes[24].colors
            self.cubes[24].colors = self.cubes[14].colors
            self.cubes[14].colors = self.cubes[7].colors
            self.cubes[7].colors = self.cubes[16].colors
            self.cubes[16].colors = temp
        else: #counter-clockwise
            for c in cubes:
                temp = c.colors['front']
                c.colors['front'] = c.colors['left']
                c.colors['left'] = c.colors['back']
                c.colors['back'] = c.colors['right']
                c.colors['right'] = temp
            #corners
            temp = self.cubes[23].colors
            self.cubes[23].colors = self.cubes[25].colors
            self.cubes[25].colors = self.cubes[8].colors
            self.cubes[8].colors = self.cubes[6].colors
            self.cubes[6].colors = temp
            #edges
            temp = self.cubes[24].colors
            self.cubes[24].colors = self.cubes[16].colors
            self.cubes[16].colors = self.cubes[7].colors
            self.cubes[7].colors = self.cubes[14].colors
            self.cubes[14].colors = temp
        self.reset()
        self.busy = 0

    #rotate down face
    def D(self, cw=1):
        self.busy = 1
        ind = [0, 1, 2, 9, 10, 11, 17, 18, 19]
        cubes = self.cubes[ind]
        for i in range(1, self.num_frames+1):
            d_th = i*np.pi/(2*self.num_frames)
            if cw == 0:
                d_th = - d_th
            for c in cubes:
                try:
                    if c.y0 > 0:
                        angle = np.arccos((c.x0-1)/c.r) + d_th    
                    else:
                        angle = -np.arccos((c.x0-1)/c.r) + d_th
                    c.x = 1 + c.r*np.cos(angle)
                    c.y = 1 + c.r*np.sin(angle)
                except: #happens when r = 0
                    pass
                c.thz = -d_th
            self.display()
        #update colors and reset
        if cw == 1: #clockwise
            for c in cubes:
                temp = c.colors['right']
                c.colors['right'] = c.colors['front']
                c.colors['front'] = c.colors['left']
                c.colors['left'] = c.colors['back']
                c.colors['back'] = temp
            #corners
            temp = self.cubes[0].colors
            self.cubes[0].colors = self.cubes[17].colors
            self.cubes[17].colors = self.cubes[19].colors
            self.cubes[19].colors = self.cubes[2].colors
            self.cubes[2].colors = temp
            #edges
            temp = self.cubes[1].colors
            self.cubes[1].colors = self.cubes[9].colors
            self.cubes[9].colors = self.cubes[18].colors
            self.cubes[18].colors = self.cubes[11].colors
            self.cubes[11].colors = temp
        else: #counter-clockwise
            for c in cubes:
                temp = c.colors['right']
                c.colors['right'] = c.colors['back']
                c.colors['back'] = c.colors['left']
                c.colors['left'] = c.colors['front']
                c.colors['front'] = temp
            #corners
            temp = self.cubes[0].colors
            self.cubes[0].colors = self.cubes[2].colors
            self.cubes[2].colors = self.cubes[19].colors
            self.cubes[19].colors = self.cubes[17].colors
            self.cubes[17].colors = temp
            #edges
            temp = self.cubes[1].colors
            self.cubes[1].colors = self.cubes[11].colors
            self.cubes[11].colors = self.cubes[18].colors
            self.cubes[18].colors = self.cubes[9].colors
            self.cubes[9].colors = temp
        self.reset()
        self.busy = 0

    #rotate back face
    def B(self, cw = 1):
        self.busy = 1
        ind = [17, 18, 19, 20, 21, 22, 23, 24, 25]
        cubes = self.cubes[ind]
        for i in range(1, self.num_frames+1):
            d_th = i*np.pi/(2*self.num_frames)
            if cw == 0:
                d_th = - d_th
            for c in cubes:
                try:
                    if c.z0 > 0:
                        angle = np.arccos((c.x0-1)/c.r) + d_th    
                    else:
                        angle = -np.arccos((c.x0-1)/c.r) + d_th
                    c.x = 1 + c.r*np.cos(angle)
                    c.z = 1 + c.r*np.sin(angle)
                except: #happens when r = 0
                    pass
                c.thy = d_th  
            self.display()
        #update colors and reset
        if cw == 1: #clockwise
            for c in cubes:
                temp = c.colors['right']
                c.colors['right'] = c.colors['bottom']
                c.colors['bottom'] = c.colors['left']
                c.colors['left'] = c.colors['top']
                c.colors['top'] = temp
            #corners
            temp = self.cubes[25].colors
            self.cubes[25].colors = self.cubes[19].colors
            self.cubes[19].colors = self.cubes[17].colors
            self.cubes[17].colors = self.cubes[23].colors
            self.cubes[23].colors = temp
            #edges
            temp = self.cubes[22].colors
            self.cubes[22].colors = self.cubes[18].colors
            self.cubes[18].colors = self.cubes[20].colors
            self.cubes[20].colors = self.cubes[24].colors
            self.cubes[24].colors = temp
        else: #counter-clockwise
            for c in cubes:
                temp = c.colors['right']
                c.colors['right'] = c.colors['top']
                c.colors['top'] = c.colors['left']
                c.colors['left'] = c.colors['bottom']
                c.colors['bottom'] = temp
            #corners
            temp = self.cubes[25].colors
            self.cubes[25].colors = self.cubes[23].colors
            self.cubes[23].colors = self.cubes[17].colors
            self.cubes[17].colors = self.cubes[19].colors
            self.cubes[19].colors = temp
            #edges
            temp = self.cubes[22].colors
            self.cubes[22].colors = self.cubes[24].colors
            self.cubes[24].colors = self.cubes[20].colors
            self.cubes[20].colors = self.cubes[18].colors
            self.cubes[18].colors = temp
        self.reset()
        self.busy = 0

    #rotate front face (ccw)
    def FP(self):
        self.F(cw=0)

    #rotate right face (ccw)
    def RP(self):
        self.R(cw=0)

    #rotate left face (ccw)
    def LP(self):
        self.L(cw=0)

    #rotate up face (ccw)
    def UP(self):
        self.U(cw=0)

    #rotate down face (ccw)
    def DP(self):
        self.D(cw=0)

    #rotate back face (ccw)
    def BP(self):
        self.B(cw=0)

    def F_button(self, event=None):
        self.q.put(self.F)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def R_button(self, event=None):
        self.q.put(self.R)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def U_button(self, event=None):
        self.q.put(self.U)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def B_button(self, event=None):
        self.q.put(self.B)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def L_button(self, event=None):
        self.q.put(self.L)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def D_button(self, event=None):
        self.q.put(self.D)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def FP_button(self, event=None):
        self.q.put(self.FP)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def RP_button(self, event=None):
        self.q.put(self.RP)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def UP_button(self, event=None):
        self.q.put(self.UP)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def BP_button(self, event=None):
        self.q.put(self.BP)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def LP_button(self, event=None):
        self.q.put(self.LP)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def DP_button(self, event=None):
        self.q.put(self.DP)
        #if not busy, execute everything in the queue
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def randomize_button(self, event=None):
        self.q.put(self.randomize)
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def reset_button(self, event=None):
        self.q.put(self.reset_all)
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    def super_button(self, event=None):
        self.q.put(self.super)
        if not self.busy:
            while not self.q.empty():
                self.q.get()()

    #generate 25 random moves
    def randomize(self):
        move_dict = {
            1: self.F,
            2: self.R,
            3: self.U,
            4: self.B,
            5: self.L,
            6: self.D,
            7: self.FP,
            8: self.RP,
            9: self.UP,
            10: self.BP,
            11: self.LP,
            12: self.DP
        }
        for i in range(25):
            move_dict[np.random.randint(1, 13)]()

    #reset colors for all the small cubes
    def reset_all(self):
        for c in self.cubes:
            c.colors = {'front': 'b', 'back': 'g', 'left': 'orange', 'right': 'r', 'top': 'y', 'bottom': 'w'}
        self.display()

    #if cube starts in solved position, this brings it to the "superflip" position
    def super(self):
        #U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2
        r.U(); r.R(); r.R(); r.F(); r.B(); r.R(); r.B(); r.B(); r.R()
        r.U(); r.U(); r.L(); r.B(); r.B(); r.R(); r.UP(); r.DP(); r.R()
        r.R(); r.F(); r.RP(); r.L(); r.B(); r.B(); r.U(); r.U(); r.F(); r.F()
            
#display the cube
r = Rubiks()
r.display()

#block program from ending
plt.show()
