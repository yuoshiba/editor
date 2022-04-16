#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (QListWidget, QFileDialog, QInputDialog, QFormLayout, QLineEdit, QTextEdit, QHBoxLayout, QRadioButton, QMessageBox, QApplication, QLabel, QVBoxLayout, QPushButton, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask
    )
app = QApplication([])
win = QWidget()

win.resize(700, 500)
win.SetWindowTitle = ('Easy Editor')
Ib_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
Iw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharpen = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(Iw_files)
col2.addWidget(Ib_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharpen)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 60)
row.addLayout(col2, 200)
win.setLayout(row)

win.show()

workdir = ''

def filter(files, extension):
    result = []
    for filename in files:
        for ext in extension:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extension = ['.jpg', '.jpeg', '.png', '.bmp']
    chooseworkdir()
    filenames = filter(os.listdir(workdir), extension)
    Iw_files.clear()
    for filename in filenames:
        Iw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def saveImage(self):
        '''сохраняет копию файла в подпапке'''
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        Ib_image.hide()
        pixmapimage = QPixmap(path)
        w, h = Ib_image.width(), Ib_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        Ib_image.setPixmap(pixmapimage)
        Ib_image.show()

workimage = ImageProcessor()

def showChosenImage():
    if Iw_files.currentRow() >= 0:
        filename = Iw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

Iw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharpen.clicked.connect(workimage.do_sharpen)

app.exec_()