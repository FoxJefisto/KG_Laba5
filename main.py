from numpy.random import random
from pyglet.gl import *
from pyglet.window import Window, key
from pyglet import app, graphics, clock
import numpy as np

w = width = height = 800 # Размер окна вывода
n_rot = [0] * 3
is_working = [0]*13
MODE = GL_BACK;
rot_x = 20 # Углы поворота вокруг осей X, Y и Z
rot_y = 45
R = 200
h = 400
p = 20
x = (R, 0.0, -R, -R, 0.0, R)
y = (R, 1.5 * R, R, -R, -1.5 * R, -R)

verts = ((p, p, -p), # Координаты вершин куба
         (p, p, -p),
         (-p, p, -p),
         (-p, -p, -p),
         (p, -p, p),
         (p, p, p),
         (-p, -p, p),
         (-p, p, p))

faces = ((0, 1, 2, 3), # Индексы вершин граней куба
         (3, 2, 7, 6),
         (6, 7, 5, 4),
         (4, 5, 1, 0),
         (1, 5, 7, 2),
         (4, 0, 3, 6))
#позиция источника света0
x_clr0 = R
y_clr0 = h
z_clr0 = 2*h
#позиция источника света1
x_clr1 = -3*R
y_clr1 = 0
z_clr1 = -0.25*h

mtClr0 = [0.233, 0.727811, 0.633, 0] # Цвет материала
light_position0L = [x_clr0, y_clr0, z_clr0, 0] # Позиция источника света0
light_position1L = [x_clr1, y_clr1, z_clr1, 0] # Позиция источника света1
lghtClr0L = [0, 0.5, 0, 0] # Цвет источника света0
lghtClr1L = [0.75, 0, 0, 0] # Цвет источника света1
mtClr = (GLfloat * 4)()
light_position0 = (GLfloat * 4)()
light_position1 = (GLfloat * 4)()
lghtClr0 = (GLfloat * 4)()
lghtClr1 = (GLfloat * 4)()
for k in range(4): mtClr[k] = mtClr0[k]
for k in range(4): light_position0[k] = light_position0L[k]
for k in range(4): lghtClr0[k] = lghtClr0L[k]
for k in range(4): light_position1[k] = light_position1L[k]
for k in range(4): lghtClr1[k] = lghtClr1L[k]
#

window = Window(visible = True, width = width, height = height, resizable = True)
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glLineWidth(4)
glEnable(GL_NORMALIZE)
@window.event
def on_draw():
    window.clear()
    #Настраиваем матрицу проецирования
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-w, w, -w, w, -w, w)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glPushMatrix()
    glPushMatrix()
    glDisable(GL_LIGHTING)
    # Движение первого куба
    glTranslatef(light_position0L[0], light_position0L[1], light_position0L[2])
    glColor3f(0, 0.5, 0)
    cube_draw()
    # Движение второго куба
    glPopMatrix()
    glTranslatef(light_position1L[0], light_position1L[1], light_position1L[2])
    glColor3f(0.75, 0, 0)
    cube_draw()
    glPopMatrix()

    glMaterialfv(GL_FRONT, GL_SPECULAR, mtClr)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lghtClr0)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lghtClr1)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    #4 пункт
    glRotatef(n_rot[0], 1, 0, 0)
    glRotatef(n_rot[1], 0, 1, 0)
    glRotatef(n_rot[2], 0, 0, 1)
    hexagonalPrismNormalize()
    #2,3 пункты
    if (is_working[1] == 1):
        ShowNormTops()
    elif (is_working[1] == 2):
        ShowNormFringe()





@window.event
def on_key_press(ch, modifiers):
    global is_working
    if ch == key.E:
        if (not is_working[12]):
            clock.schedule_interval(rotate13, 0.0000001)
            is_working[12] = 1
        else :
            clock.unschedule(rotate13)
            is_working[12] = 0
    #1 пункт
    if ch == key._1:
        global MODE
        if(not is_working[0]):
            MODE = GL_FRONT_AND_BACK
            is_working[0] = 1
        else:
            MODE = GL_BACK
            is_working[0] = 0
    #2,3 пункты
    if ch == key._2:
        if(is_working[1] == 0):
            is_working[1] = 1
        elif (is_working[1] == 1):
            is_working[1] = 2
        else:
            is_working[1] = 0
    #4 пункт
    if ch == key._3:
        if(is_working[2] == 0):
            clock.schedule_interval(rotate4, 0.00001)
            is_working[2] = 1
        else:
            clock.unschedule(rotate4)
            is_working[2] = 0
    




def rotate4(dt):
    global n_rot
    n_rot[0] = (n_rot[0] + dt * np.random.uniform(20,60)) % 360
    n_rot[1] = (n_rot[1] + dt * np.random.uniform(20,60)) % 360
    n_rot[2] = (n_rot[2] + dt * np.random.uniform(20,60)) % 360

def rotate13(dt):
    global n_rot
    n_rot[1] = (n_rot[1] + dt * np.random.uniform(20,60)) % 360

# def hexagonalPrism():
#     glEnable(GL_NORMALIZE)
#     glEnable(GL_CULL_FACE)
#     glCullFace(GL_BACK)
#     glFrontFace(GL_CCW)
#     #Рисование боковых граней
#     glBegin(GL_QUADS)
#     for i1 in range(6):
#         i2 = (i1 + 1) % 6
#         glVertex3f(x[i1], 0.0, y[i1])
#         glVertex3f(x[i1], h, y[i1])
#         glVertex3f(x[i2], h, y[i2])
#         glVertex3f(x[i2], 0.0, y[i2])
#     glEnd()
#
#
#     #рисование нижней грани
#     glColor4f( 1, 1, 1, 1 )
#     glCullFace(MODE)
#     glFrontFace(GL_CCW)
#     glBegin(GL_POLYGON)
#     for i in range(6):
#         glVertex3f(x[i], 0.0, y[i])
#     glEnd()
#     glFrontFace(GL_CW)
#     # рисование верхней грани
#     glBegin(GL_POLYGON)
#     for i in range(6):
#         glVertex3f(x[i], h, y[i])
#     glEnd()

def Norm(a,b):
    n = np.cross(a, b) # Векторное произведение
    return n

def ShowNormFringe():
    glDisable(GL_LIGHTING)
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i1 in range(6):
        i2 = (i1 + 1) % 6
        A = np.array([x[i1], 0.0, y[i1]])
        B = np.array([x[i1], h, y[i1]])
        D = np.array([x[i2], 0.0, y[i2]])
        AB = B - A
        AD = D - A
        norma = Norm(AB, AD)
        glVertex3f((A[0] + D[0])/2, h/2, (A[2]+D[2])/2)
        glVertex3f(norma[0], norma[1], norma[2])
    glVertex3f(0, h,0)
    glVertex3f(0, 1.5*h,0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -1.01*h, 0)
    glEnd()

def ShowNormTops():
    glLineWidth(1)
    glDisable(GL_LIGHTING)
    glColor3f(1,1,1)
    glBegin(GL_LINES)
    for i1 in range(6):
        i2 = (i1 + 1) % 6
        A = np.array([x[i1], 0.0, y[i1]])
        B = np.array([x[i1], h, y[i1]])
        C = np.array([x[i2], h, y[i2]])
        D = np.array([x[i2], 0.0, y[i2]])
        points = [A, B, C, D]
        for j in range(4):
            XY = points[j-1] - points[j]
            XZ = points[(j+1)%4] - points[j]
            norma = Norm(XZ, XY)
            glVertex3f(points[j][0], points[j][1], points[j][2])
            glVertex3f(norma[0], norma[1], norma[2])
    for i in range(6):
        #нижняя грань
        glVertex3f(x[i], 0, y[i])
        glVertex3f(x[i], -h, y[i])
        #верхняя грань
        glVertex3f(x[i], h, y[i])
        glVertex3f(x[i], 2*h, y[i])
    glEnd()

def hexagonalPrismNormalize():
    glEnable(GL_NORMALIZE)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    #Рисование боковых граней
    glBegin(GL_QUADS)
    for i1 in range(6):
        i2 = (i1 + 1) % 6
        A = np.array([x[i1], 0.0, y[i1]])
        B = np.array([x[i1], h, y[i1]])
        C = np.array([x[i2], h, y[i2]])
        D = np.array([x[i2], 0.0, y[i2]])
        points = [A, B, C, D]
        for j in range(4):
            XY = points[j - 1] - points[j]
            XZ = points[(j + 1) % 4] - points[j]
            norma = Norm(XZ, XY)
            glNormal3f(norma[0], norma[1], norma[2])
            glVertex3f(points[j][0],points[j][1],points[j][2])
    glEnd()


    #рисование нижней грани
    glColor4f( 1, 1, 1, 1 )
    glCullFace(MODE)
    glFrontFace(GL_CCW)
    glBegin(GL_POLYGON)
    for i in range(6):
        glNormal3f(0, -h, 0)
        glVertex3f(x[i], 0.0, y[i])
    glEnd()
    glFrontFace(GL_CW)
    # рисование верхней грани
    glBegin(GL_POLYGON)
    for i in range(6):
        glNormal3f(0, h, 0)
        glVertex3f(x[i], h, y[i])
    glEnd()

def cube_draw():
    glCullFace(GL_BACK)
    for face in faces:
        v4 = ()
        for v in face:
            v4 += verts[v]
        graphics.draw(4, GL_QUADS, ('v3f', v4))

app.run()