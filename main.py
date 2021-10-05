from pyglet.gl import *
from pyglet.window import Window, key
from pyglet import app, graphics, clock
import numpy as np

w = width = height = 600 # Размер окна вывода
n_rot = 0
is_working = False
rot_x = 20 # Углы поворота вокруг осей X, Y и Z
rot_y = 45
R = 200
h = 400

def rotate(dt):
    global n_rot
    n_rot = (n_rot + dt*60) % 361


def hexagonalPrism():

    x = ( R, 0.0, -R, -R,  0.0,  R )
    y = ( R,   1.5*R,  R,   -R,   -1.5*R, -R )
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glBegin(GL_QUADS)
    for i1 in range(6):
        glColor4f(1.0 if i1 < 2 or i1 > 4 else 0.0, 1.0 if i1 > 1 and i1 < 5  else 0.0, 1.0 if i1 > 2 else 0.0, 1.0)
        i2 = (i1 + 1) % 6
        glVertex3f(x[i1], 0.0, y[i1])
        glVertex3f(x[i1], h, y[i1])
        glVertex3f(x[i2], h, y[i2])
        glVertex3f(x[i2], 0.0, y[i2])


    glEnd()
    glColor4f( 1, 1, 1, 1 )
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex3f(x[i], 0.0, y[i])
    glEnd()
    glDisable(GL_CULL_FACE)
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex3f(x[i], h, y[i])
    glEnd()


window = Window(visible = True, width = width, height = height, resizable = True)
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glLineWidth(4)
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
    glRotatef(n_rot, 0, 1, 0)
    hexagonalPrism()


@window.event
def on_key_press(ch, modifiers):
    global is_working
    if ch == key._1:
        if (not is_working):
            clock.schedule_interval(rotate, 0.0000001)
            is_working = True
        else :
            clock.unschedule(rotate)
            is_working = False

app.run()
