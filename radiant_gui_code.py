# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radiant_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from obj_detect import object_detector
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

from PIL import Image

#from PyQt5.QtGui import QImage, QPixmap, QPainter

VALID_FORMAT = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')

def getImages(folder):
    ''' Get the names and paths of all the images in a directory. '''
    image_list = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(VALID_FORMAT):
                im_path = os.path.join(folder, file)
                image_obj = {'name': file, 'path': im_path }
                image_list.append(image_obj)
    return image_list
def get_qimage(image: np.ndarray):
    assert (np.max(image) <= 255)
    image8 = image.astype(np.uint8, order='C', casting='unsafe')
    height, width, colors = image8.shape
    bytesPerLine = 3 * width

    image = QImage(image8.data, width, height, bytesPerLine,
                       QImage.Format_RGB888)

    #image = image.rgbSwapped()
    return image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(934, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.open_folder = QtWidgets.QPushButton(self.centralwidget)
        self.open_folder.setGeometry(QtCore.QRect(10, 40, 121, 81))
        self.open_folder.setObjectName("open_folder")

        self.next_image = QtWidgets.QPushButton(self.centralwidget)
        self.next_image.setGeometry(QtCore.QRect(10, 160, 121, 81))
        self.next_image.setObjectName("next_image")

        self.prev_img = QtWidgets.QPushButton(self.centralwidget)
        self.prev_img.setGeometry(QtCore.QRect(10, 280, 121, 81))
        self.prev_img.setObjectName("prev_img")

        self.save_annotations = QtWidgets.QPushButton(self.centralwidget)
        self.save_annotations.setGeometry(QtCore.QRect(10, 400, 121, 81))
        self.save_annotations.setObjectName("save_annotations")

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(206, 44, 471, 421))
        self.image.setObjectName("image")

        self.select_model = QtWidgets.QLabel(self.centralwidget)
        self.select_model.setGeometry(QtCore.QRect(770, 30, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans CJK SC DemiLight")
        font.setPointSize(14)
        self.select_model.setFont(font)
        self.select_model.setObjectName("select_model")

        self.model_selector = QtWidgets.QComboBox(self.centralwidget)
        self.model_selector.setGeometry(QtCore.QRect(780, 90, 121, 23))
        self.model_selector.setObjectName("model_selector")
        self.model_selector.addItem("")
        self.model_selector.addItem("")
        self.model_selector.addItem("")

        self.th_label = QtWidgets.QLabel(self.centralwidget)
        self.th_label.setGeometry(QtCore.QRect(770, 180, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.th_label.setFont(font)
        self.th_label.setObjectName("th_label")
        self.th_show = QtWidgets.QLabel(self.centralwidget)
        self.th_show.setGeometry(QtCore.QRect(806, 220, 51, 41))
        self.th_show.setObjectName("th_show")

        self.th_slider = QtWidgets.QSlider(self.centralwidget)
        self.th_slider.setGeometry(QtCore.QRect(760, 280, 160, 16))
        self.th_slider.setOrientation(QtCore.Qt.Horizontal)
        self.th_slider.setObjectName("th_slider")

        self.label_filter = QtWidgets.QLabel(self.centralwidget)
        self.label_filter.setGeometry(QtCore.QRect(766, 340, 151, 20))
        self.label_filter.setObjectName("label_filter")

        self.label_selector = QtWidgets.QComboBox(self.centralwidget)
        self.label_selector.setGeometry(QtCore.QRect(780, 390, 131, 23))
        self.label_selector.setObjectName("label_selector")
        self.label_selector.addItem("")
        self.label_selector.addItem("")
        self.label_selector.addItem("")
        self.label_selector.addItem("")
        self.label_selector.addItem("")

        self.Detect = QtWidgets.QPushButton(self.centralwidget)
        self.Detect.setGeometry(QtCore.QRect(769, 430, 141, 61))
        self.Detect.setObjectName("Detect")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 934, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.cntr = 0
        self.numImages=0

        self.obj=object_detector()
        self.obj.set_model_name("faster_rcnn_inception_v2_coco_2018_01_28")
        self.obj.set_class_selector(1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Radiant GUI Tool"))
        self.open_folder.setText(_translate("MainWindow", "Open Folder"))
        self.next_image.setText(_translate("MainWindow", "Next Image"))
        self.prev_img.setText(_translate("MainWindow", "Previous Image"))
        self.save_annotations.setText(_translate("MainWindow", "Save Annotations"))

        self.image.setText(_translate("MainWindow", "                                                             image "))
        #self.show_image("~/frame_18.png")

        self.select_model.setText(_translate("MainWindow", "  Select Model"))

        self.model_selector.setItemText(0, _translate("MainWindow", "FRCNN"))
        self.model_selector.setItemText(1, _translate("MainWindow", "SSD MobileNet"))
        self.model_selector.setItemText(2, _translate("MainWindow", "SSD Inception"))

        self.th_label.setText(_translate("MainWindow", "Detection Threshold"))
        self.th_show.setText(_translate("MainWindow", " show"))
        self.label_filter.setText(_translate("MainWindow", "          Label Filter"))

        self.label_selector.setItemText(0, _translate("MainWindow", "Person"))
        self.label_selector.setItemText(1, _translate("MainWindow", "Cat"))
        self.label_selector.setItemText(2, _translate("MainWindow", "Dog"))
        self.label_selector.setItemText(3, _translate("MainWindow", "Bottle"))
        self.label_selector.setItemText(4, _translate("MainWindow", "Chair"))

        self.Detect.setText(_translate("MainWindow", "Detect"))

        self.th_slider.setMinimum(0)
        self.th_slider.setMaximum(200)
        self.th_slider.setValue(0)

        self.th_show.setText(str(self.th_slider.value()*0.005))

        self.connect_slots()

    def connect_slots(self):
         self.open_folder.clicked.connect(self.selectDir)
         self.next_image.clicked.connect(self.nextImg)
         self.prev_img.clicked.connect(self.prevImg)
         self.model_selector.currentIndexChanged.connect(self.selectionchange)
         self.th_slider.valueChanged.connect(self.val_change)
         self.label_selector.currentIndexChanged.connect(self.label_change)
         self.Detect.clicked.connect(self.detect_clicked)

    def show_image(self,image_path):
        self.qimage=QImage(image_path)
        self.qpixmap=QPixmap(self.image.size())
        if not self.qimage.isNull():
            self.qimage_scaled=self.qimage.scaled(self.image.width(), self.image.height(), QtCore.Qt.KeepAspectRatio)
            self.qpixmap=QPixmap.fromImage(self.qimage_scaled)
            self.image.setPixmap(self.qpixmap)
        else:
            self.image.setText("Not a valid image or path not proper")

    def selectDir(self):
        ''' Select a directory, make list of images in it and display the first image in the list. '''
        # open 'select folder' dialog box
        self.folder = str(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory"))
        if not self.folder:
            QtWidgets.QMessageBox.warning(None, 'No Folder Selected', 'Please select a valid Folder')
            return

        self.logs = getImages(self.folder)
        self.numImages = len(self.logs)

        self.cntr = 0
        if not self.logs:
            QtWidgets.QMessageBox.warning(None, 'No Folder Selected', 'Please select a valid Folder')
            return
        self.show_image(self.logs[self.cntr]['path'])

    def nextImg(self):
        if self.cntr < self.numImages -1:
            self.cntr += 1
            self.show_image(self.logs[self.cntr]['path'])
        else:
            QtWidgets.QMessageBox.warning(None, 'Sorry', 'No more Images!')

    def prevImg(self):
        if self.cntr > 0:
            self.cntr -= 1
            self.show_image(self.logs[self.cntr]['path'])
        else:
            QtWidgets.QMessageBox.warning(None, 'Sorry', 'No previous Image!')

    def selectionchange(self,i):

        if(i==0):
            self.obj.set_model_name("faster_rcnn_inception_v2_coco_2018_01_28")
        elif(i==1):
            self.obj.set_model_name("ssd_mobilenet_v1_coco_2018_01_28")
        elif (i==2):
            self.obj.set_model_name("ssd_inception_v2_coco_2018_01_28")



    def val_change(self):
        self.th_show.setText(str(self.th_slider.value()*0.005))
        self.obj.set_threshold(self.th_slider.value()*0.005)

    def label_change(self,i):
        if(i==0):
            self.obj.set_class_selector(1)
        elif(i==1):
            self.obj.set_class_selector(17)
        elif(i==2):
            self.obj.set_class_selector(18)
        elif(i==3):
            self.obj.set_class_selector(44)
        elif(i==4):
            self.obj.set_class_selector(62)
        #print(i)

    def detect_clicked(self):
        result=self.obj.show_inference(self.logs[self.cntr]['path'])
        self.qimage=get_qimage(result)
        if not self.qimage.isNull():
            self.qimage_scaled=self.qimage.scaled(self.image.width(), self.image.height(), QtCore.Qt.KeepAspectRatio)
            self.qpixmap=QPixmap.fromImage(self.qimage_scaled)
            self.image.setPixmap(self.qpixmap)
        else:
            self.image.setText("Not a valid image or path not proper")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
