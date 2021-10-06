# Вывод параболоида
import pyglet
from pyglet import app, gl, graphics
from pyglet.window import Window, key
import numpy as np, math
from sys import exit
# z = ac*x**2 + ac*y**2 (реально имеем: y = ac*x**2 + ac*z**2)
save_to_file = False # Флаг записи модели в файлы
read_from_file = False # Флаг чтения модели из файлов
if read_from_file: save_to_file = False
plot_surf = False # Флаг вывода поверхности z = ac*x**2 + ac*y**2
show_top = True # Флаг вывода крышки
show_normals = True
kn = 2 # Коэффициент увеличения длины отображаемой нормали
ac = 2.5 # Коэффициент в уравнении параболоида
n = 24 # Число вершин в сечении параболоида
ch = 7 # Число сечений параболоида плоскостями y = const
h_cover = 20 # Высота параболоида
vrts = [] # Координаты вершин параболоида
nrms = [] # Координаты нормалей к граням (рассчитываются для каждой вершины)
textr = [] # Координаты текстуры (задаются для каждой вершины)
vrts_top = [] # Координаты вершин крышки
textr_top = [] # Координаты тектстуры крышки
dh = h_cover / ch # Расстояние между сечениями
dal = 2 * math.pi / n # dal - угол между вершинами сечения
hp0 = 0.1 # Низ параболоида
# Текстура
use_txtr = True
texFromFile = False # True False
if use_txtr: show_normals = False
# Координаты текстуры меняются в диапазоне 0-1
dnx = 1 / (n - 1) # Шаг изменения координат текстуры по x
dny = 1 / ch # Шаг изменения координат текстуры по y
if read_from_file:
    print('Загрузка данных из двоичных файлов')
    def load_data(file, shape = None):
        with open(file, 'rb') as r_b:
            data = np.fromfile(r_b)
        if shape is not None:
            size = len(data)
            if len(shape) == 2:
                size = int(size / (shape[0] * shape[1]))
                data = data.reshape(size, shape[0], shape[1])
            else:
                size = int(size / shape[0])
                data = data.reshape(size, shape[0])
        return data
    vrts = load_data('vrts.bin', [4, 3])
    vrts_top = load_data('vrts_top.bin', [3])
    nrms = load_data('nrms.bin', [3])
    nrm_top = load_data('nrm_top.bin', None)
    textr = load_data('textr.bin', [2])
    textr_top = load_data('textr_top.bin', [2])
else:
    hp = hp0
    for i in range(ch): # Вершины
        al = 0 # Первая вершина лежит на оси Х
        s = ac * math.sqrt(hp)
        h0 = hp
        hp += dh
        s2 = ac * math.sqrt(hp)
        for j in range(n):
            co = math.cos(al)
            si = math.sin(al)
            al += dal
            co2 = math.cos(al)
            si2 = math.sin(al)
            # Координаты вершин очередной трапеции
            v0 = np.array([s * co, h0, -s * si])
            v1 = np.array([s * co2, h0, -s * si2])
            v2 = np.array([s2 * co2, hp, -s2 * si2])
            v3 = np.array([s2 * co, hp, -s2 * si])
            vrts.append([v0, v1, v2, v3])
            a = v1 - v0
            b = v3 - v0
            sab = np.cross(a, b) # Векторное произведение
            sab = sab / np.linalg.norm(sab) # Нормализация
            #sab = sab / np.sqrt(np.sum(sab**2))
            nrms.append(sab) # Координаты нормали
            textr.append([j * dnx, (h0 - hp0) / h_cover]) # Координаты текстуры
    n_vrts = len(vrts)
    # Крышка
    al = 0
    kt = 0.25
    for j in range(n):
        co = math.cos(al); si = math.sin(al)
        al += dal
        vrts_top.append([s2 * co, hp, -s2 * si])
        nrms.append(nrms[n_vrts - n + j])
        textr.append([j * dnx, 1])
        if texFromFile:
            j2 = 2 * j * dnx
            if j <= n / 4:
                textr_top.append([j2, 0.5 - j2])
            elif j <= n / 2:
                textr_top.append([j2, j2 - 0.5])
            elif j <= 3 * n / 4:
                textr_top.append([2 - j2, j2 - 0.5])
            else:
                textr_top.append([2 - j2, 2.5 - j2])
        else:
            textr_top.append([kt * co, kt * si])
    v0 = np.array(vrts_top[0])
    v1 = np.array(vrts_top[1])
    vn = np.array(vrts_top[n - 1])
    nrm_top = np.cross(v1 - v0, vn - v0) # Нормаль к крышке
    nrm_top = nrm_top / np.linalg.norm(sab)
if save_to_file:
    print('Запись данных в двоичные файлы')
    def write_to_bin(file, data):
        fn = open(file, 'wb')
        fn.write(np.array(data))
        fn.close()
    write_to_bin('vrts.bin', vrts)
    write_to_bin('vrts_top.bin', vrts_top)
    write_to_bin('nrms.bin', nrms)
    write_to_bin('nrm_top.bin', nrm_top)
    write_to_bin('textr.bin', textr)
    write_to_bin('textr_top.bin', textr_top)
if plot_surf:
    from mpl_toolkits.mplot3d import Axes3D # Для projection = '3d'
    from matplotlib import cm
    import matplotlib.pyplot as plt
    xy, z = [], []
    x_min = x_max = vrts[0][0][0]
    y_min = y_max = vrts[0][0][2]
    for quad in vrts:
        for v in quad:
            p = [v[0], v[2]]
            if not p in xy:
                xy.append(p)
                z.append(v[1])
                if p[0] < x_min: x_min = p[0]
                if p[0] > x_max: x_max = p[0]
                if p[1] < y_min: y_min = p[1]
                if p[1] > y_max: y_max = p[1]
    step = 0.5
    X = np.arange(x_min, x_max, step) # Формирование сетки
    Y = np.arange(y_min, y_max, step)
    X, Y = np.meshgrid(X, Y)
    Z = ac*X**2 + ac*Y**2 # Формируем массив Z формы (len(X), len(Y))
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    surf = ax.plot_surface(X, Y, Z, cmap = cm.plasma) # plasma Spectral
    ax.set_xlabel('X') # Метки осей координат
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    for label in ax.xaxis.get_ticklabels(): # Настройка оси X
        label.set_color('black')
        label.set_rotation(-45)
        label.set_fontsize(9)
    for label in ax.yaxis.get_ticklabels(): # Настройка оси Y
        label.set_fontsize(9)
    for label in ax.zaxis.get_ticklabels(): # Настройка оси Z
        label.set_fontsize(9)
    ax.view_init(elev = 30, azim = 45) # Проецирование
    fig.colorbar(surf, shrink = 0.5, aspect = 5) # Шкала цветов
    plt.show() # Отображение результата
    exit()
#
def c_float_Array(data): # Преобразование в си-массив
    return (gl.GLfloat * len(data))(*data)
lghtClr0 = [0.75, 0, 0, 0]
mtClr = c_float_Array([1, 1, 0, 0])
light_position = c_float_Array([-80, 20, 90, 0])
lghtClr = c_float_Array([0.75, 0, 0, 0])
#
def texInit():
    if texFromFile:
        fn = 'G:\\python\\openGL\\кот.jpg'
        img = pyglet.image.load(fn)
        iWidth = img.width
        iHeight = img.height
        img = img.get_data('RGB', iWidth * 3)
    else:
        iWidth = iHeight = 64
        n = 3 * iWidth * iHeight
        img = np.zeros((3, iWidth, iHeight), dtype = 'uint8')
        for i in range(iHeight): # Генерация черно-белого образа, на основе которого создается текстура
         for j in range(iWidth):
            img[:, i, j] = ((i - 1) & 16 ^ (j - 1) & 16) * 255
        img = img.reshape(n)
        img = (gl.GLubyte * n)(*img)
    p = gl.GL_TEXTURE_2D
    r = gl.GL_RGB
    gl.glTexParameterf(p, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameterf(p, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameterf(p, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf(p, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_DECAL)
    gl.glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, gl.GL_UNSIGNED_BYTE, img)
    if use_txtr:
        gl.glEnable(p)
w = h = h_cover
width, height = 20 * w, 10 * w
window = Window(visible = True, width = width, height = height,
                resizable = True, caption = 'Параболоид')
gl.glClearColor(1, 1, 1, 1) # Белый цвет фона
gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
gl.glLineWidth(2)
gl.glPointSize(4)
gl.glEnable(gl.GL_POINT_SMOOTH)
gl.glShadeModel(gl.GL_SMOOTH) # GL_SMOOTH, GL_FLAT - без интерполяции цветов
gl.glCullFace(gl.GL_BACK) # Запрещен вывод граней, показанных нелицевой стороной
gl.glEnable(gl.GL_CULL_FACE) # Активизируем режим GL_CULL_FACE
##gl.glEnable(gl.GL_NORMALIZE)
if show_normals:
    gl.glEnable(gl.GL_DEPTH_TEST) # Активизируем тест глубины
texInit()
@window.event
def on_draw():
    window.clear()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-w, w, -0.5 * h, h, -w, w) # Ортографическое проецирование
    gl.glRotatef(30, 1, 0, 0) # Поворот относительно оси X
    if use_txtr and texFromFile:
        gl.glRotatef(90, 0, 1, 0) # Поворот относительно оси Y
    gl.glTranslatef(0, -7, 0) # Перенос объекта вниз (вдоль оси Y)
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, mtClr)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_position)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, lghtClr)
    gl.glEnable(gl.GL_LIGHTING) # Активизируем заданные параметры освещенности
    gl.glEnable(gl.GL_LIGHT0)
    gl.glBegin(gl.GL_QUADS)
    k = -1
    for i in range(ch):
        for j in range(n):
            k += 1
            v = vrts[k]
            v0 = v[0]; v1 = v[1]; v2 = v[2]; v3 = v[3]
            sn = nrms[k] # Нормаль к вершине (она же нормаль к грани)
            gl.glNormal3f(sn[0], sn[1], sn[2])
            tc = textr[k] # Координаты текстуры
            gl.glTexCoord2f(tc[0], tc[1])
            gl.glVertex3f(v0[0], v0[1], v0[2])
            sn = nrms[k + 1]
            gl.glNormal3f(sn[0], sn[1], sn[2])
            gl.glTexCoord2f(tc[0] + dnx, tc[1])
            gl.glVertex3f(v1[0], v1[1], v1[2])
            sn = nrms[k + n]
            gl.glNormal3f(sn[0], sn[1], sn[2])
            gl.glTexCoord2f(tc[0] + dnx, tc[1] + dny)
            gl.glVertex3f(v2[0], v2[1], v2[2])
            sn = nrms[k + n - 1]
            gl.glNormal3f(sn[0], sn[1], sn[2])
            gl.glTexCoord2f(tc[0], tc[1] + dny)
            gl.glVertex3f(v3[0], v3[1], v3[2])
    gl.glEnd() # Заканчиваем вывод боковых граней
    if show_top:
        gl.glBegin(gl.GL_POLYGON) # Вывод крышки
        gl.glNormal3f(nrm_top[0], nrm_top[1], nrm_top[2]) # Нормаль к крышке
        for j in range(n):
            v = vrts_top[j]
            tc = textr_top[j]
            gl.glTexCoord2f(tc[0], tc[1])
            gl.glVertex3f(v[0], v[1], v[2])
        gl.glEnd() # Заканчиваем вывод крышки
    if show_normals:
        # Вывод нормалей
        gl.glDisable(gl.GL_LIGHTING) # Отключаем расчет освещенности
        gl.glLineWidth(2) # Задание толщины линии
        gl.glColor3f(0, 0, 0) # Задание текущего цвета
        gl.glBegin(gl.GL_LINES)
        k = -1
        for i in range(ch):
            for j in range(n):
                k += 1
                v = vrts[k][0]
                gl.glVertex3f(v[0], v[1], v[2])
                sn = nrms[k]
                sx = kn * sn[0]
                sy = kn * sn[1]
                sz = kn * sn[2]
                gl.glVertex3f(v[0] + sx, v[1] + sy, v[2] + sz)
                # Нормали в верхнем сечении совпадают с нормалями в предыдущем сечении
                if i == ch - 1:
                    v = vrts[k][3]
                    gl.glVertex3f(v[0], v[1], v[2])
                    gl.glVertex3f(v[0] + sx, v[1] + sy, v[2] + sz)
        gl.glEnd()
        if show_top:
            gl.glColor3f(1, 1, 1) # Текущий цвет
            gl.glBegin(gl.GL_LINES) # Нормаль к крышке
            gl.glVertex3f(0, h_cover, 0)
            gl.glVertex3f(kn * nrm_top[0], h_cover + kn * nrm_top[1], kn * nrm_top[2])
            gl.glEnd()
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key._1:
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_CULL_FACE)
    elif symbol == key._2:
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_CULL_FACE)
    elif symbol == key._3:
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE) # Вывод ребер
    elif symbol == key._4:
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_POINT)
    elif symbol == key._5:
        gl.glDisable(gl.GL_CULL_FACE)
app.run()