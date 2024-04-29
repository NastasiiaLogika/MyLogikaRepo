import os  # Імпортуємо модуль для роботи з операційною системою
from PyQt5.QtWidgets import (  # Імпортуємо класи віджетів з бібліотеки PyQt5
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt  # Імпортуємо константу та перерахування з модуля QtCore
from PyQt5.QtGui import QPixmap  # Імпортуємо клас для роботи з графікою з PyQt5

from PIL import Image  # Імпортуємо класи з бібліотеки Pillow для роботи з зображеннями
from PIL.ImageQt import ImageQt  # Для перенесення зображення з Pillow до Qt
from PIL import ImageFilter  # Імпортуємо фільтри для обробки зображень з Pillow
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)


app = QApplication([])  # Ініціалізуємо об'єкт додатку PyQt
win = QWidget()  # Створюємо головне вікно програми
win.resize(700, 500)  # Задаємо розміри вікна
win.setWindowTitle('Easy Editor')  # Встановлюємо заголовок вікна
lb_image = QLabel("Картинка")  # Створюємо мітку для відображення зображення
btn_dir = QPushButton("Папка")  # Створюємо кнопку для вибору каталогу
lw_files = QListWidget()  # Створюємо список файлів

btn_left = QPushButton("Вліво")  # Створюємо кнопку для повороту зображення вліво
btn_right = QPushButton("Вправо")  # Створюємо кнопку для повороту зображення вправо
btn_flip = QPushButton("Відзеркалити")  # Створюємо кнопку для відображення зображення відзеркаленого
btn_sharp = QPushButton("Різкість")  # Створюємо кнопку для застосування різкості до зображення
btn_bw = QPushButton("Ч/Б")  # Створюємо кнопку для перетворення зображення у чорно-біле

row = QHBoxLayout()  # Створюємо горизонтальний контейнер для розміщення віджетів
col1 = QVBoxLayout()  # Створюємо вертикальний контейнер для першого стовпця
col2 = QVBoxLayout()  # Створюємо вертикальний контейнер для другого стовпця
col1.addWidget(btn_dir)  # Додаємо кнопку вибору каталогу до першого стовпця
col1.addWidget(lw_files)  # Додаємо список файлів до першого стовпця
col2.addWidget(lb_image, 95)  # Додаємо мітку для зображення до другого стовпця
row_tools = QHBoxLayout()  # Створюємо горизонтальний контейнер для кнопок обробки зображення
row_tools.addWidget(btn_left)  # Додаємо кнопку для повороту зображення вліво
row_tools.addWidget(btn_right)  # Додаємо кнопку для повороту зображення вправо
row_tools.addWidget(btn_flip)  # Додаємо кнопку для відображення зображення відзеркаленого
row_tools.addWidget(btn_sharp)  # Додаємо кнопку для застосування різкості до зображення
row_tools.addWidget(btn_bw)  # Додаємо кнопку для перетворення зображення у чорно-біле
col2.addLayout(row_tools)  # Додаємо контейнер кнопок до другого стовпця

row.addLayout(col1, 20)  # Додаємо перший стовпець до головного контейнера з відсотковим співвідношенням 20%
row.addLayout(col2, 80)  # Додаємо другий стовпець до головного контейнера з відсотковим співвідношенням 80%
win.setLayout(row)  # Встановлюємо головний контейнер у вікно

win.show()  # Відображаємо головне вікно програми

workdir = ''  # Змінна для зберігання шляху робочого каталогу

def filter(files, extensions):
   """Функція для фільтрації файлів за розширенням."""
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result

def chooseWorkdir():
   """Функція для вибору робочого каталогу."""
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
   """Функція для відображення списку файлів з обраного каталогу."""
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)

   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
   """Клас для обробки зображень."""
   def __init__(self):
       self.image = None
       self.dir = None
       self.filename = None
       self.save_dir = "Modified/"

   def loadImage(self, filename):
       '''Завантажує зображення та запам'ятовує шлях та ім'я файлу.'''
       self.filename = filename
       fullname = os.path.join(workdir, filename)
       self.image = Image.open(fullname)

   def saveImage(self):
       '''Зберігає копію файлу у підпапці.'''
       path = os.path.join(workdir, self.save_dir)
       if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
       fullname = os.path.join(path, self.filename)

       self.image.save(fullname)

   def do_bw(self):
       """Перетворює зображення у чорно-біле."""
       self.image = self.image.convert("L")
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

   def do_left(self):
       """Повертає зображення на 90 градусів вліво."""
       self.image = self.image.transpose(Image.ROTATE_90)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

   def do_right(self):
       """Повертає зображення на 90 градусів вправо."""
       self.image = self.image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

   def do_flip(self):
       """Відображує зображення відзеркалене."""
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

   def do_sharpen(self):
       """Застосовує ефект різкості до зображення."""
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

   def showImage(self, path):
       """Відображає зображення на екрані."""
       lb_image.hide()
       pixmapimage = QPixmap(path)
       w, h = lb_image.width(), lb_image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       lb_image.setPixmap(pixmapimage)
       lb_image.show()

def showChosenImage():
   """Функція для відображення обраного зображення."""
   if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(filename)
       workimage.showImage(os.path.join(workdir, workimage.filename))

workimage = ImageProcessor()  # Поточне робоче зображення для роботи
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)

app.exec()  # Запускаємо головний цикл обробки подій