from pyglet.gl import *
from pyglet.window import Window, key
from pyglet import app, graphics, clock
import numpy as np

w = width = height = 600 # Размер окна вывода
n_rot = 0
is_working = [0]*13
MODE = GL_BACK;
rot_x = 20 # Углы поворота вокруг осей X, Y и Z
rot_y = 45
R = 200
h = 400
x = (R, 0.0, -R, -R, 0.0, R)
y = (R, 1.5 * R, R, -R, -1.5 * R, -R)

#
mtClr0 = [0.233, 0.727811, 0.633, 0] # Цвет материала
light_position0 = [0, 0, h, 0] # Позиция источника света
lghtClr0 = [0.75, 0, 0, 0] # Цвет источника света
mtClr = (gl.GLfloat * 4)()
light_position = (gl.GLfloat * 4)()
lghtClr = (gl.GLfloat * 4)()
for k in range(4): mtClr[k] = mtClr0[k]
for k in range(4): light_position[k] = light_position0[k]
for k in range(4): lghtClr[k] = lghtClr0[k]
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
    glEnable(GL_LIGHTING)
    glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, mtClr)
    glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_position)
    glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, lghtClr)
    glEnable(gl.GL_LIGHT0)  # Включаем в уравнение освещенности источник GL_LIGHT0
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(n_rot, 0, 1, 0)
    hexagonalPrism()
    if (is_working[1] == 1):
        ShowNormTops()
    elif (is_working[1] == 2):
        ShowNormFringe()





@window.event
def on_key_press(ch, modifiers):
    global is_working
    if ch == key.E:
        if (not is_working[12]):
            clock.schedule_interval(rotate, 0.0000001)
            is_working[12] = 1
        else :
            clock.unschedule(rotate)
            is_working[12] = 0
    if ch == key._1:
        global MODE
        if(not is_working[0]):
            MODE = GL_FRONT_AND_BACK
            is_working[0] = 1
        else:
            MODE = GL_BACK
            is_working[0] = 0
    if ch == key._2:
        if(is_working[1] == 0):
            is_working[1] = 1
        elif (is_working[1] == 1):
            is_working[1] = 2
        else:
            is_working[1] = 0




def rotate(dt):
    global n_rot
    n_rot = (n_rot + dt * 60) % 361

def hexagonalPrism():
    glEnable(GL_NORMALIZE)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    glBegin(GL_QUADS)
    for i1 in range(6):
        i2 = (i1 + 1) % 6
        glVertex3f(x[i1], 0.0, y[i1])
        glVertex3f(x[i1], h, y[i1])
        glVertex3f(x[i2], h, y[i2])
        glVertex3f(x[i2], 0.0, y[i2])
    glEnd()



    glColor4f( 1, 1, 1, 1 )
    glCullFace(MODE)
    glFrontFace(GL_CCW)
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex3f(x[i], 0.0, y[i])
    glEnd()
    glFrontFace(GL_CW)
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex3f(x[i], h, y[i])
    glEnd()

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
    glEnd()


app.run()