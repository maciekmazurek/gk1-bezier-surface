# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

from bezier_renderer import BezierCanvas

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.canvas = BezierCanvas(self.centralwidget)
        self.canvas.setObjectName(u"canvas")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.canvas)

        self.mainVerticalLayout = QVBoxLayout()
        self.mainVerticalLayout.setSpacing(1)
        self.mainVerticalLayout.setObjectName(u"mainVerticalLayout")
        self.mainVerticalLayout.setContentsMargins(0, -1, -1, -1)
        self.triangulationLabel = QLabel(self.centralwidget)
        self.triangulationLabel.setObjectName(u"triangulationLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.triangulationLabel.sizePolicy().hasHeightForWidth())
        self.triangulationLabel.setSizePolicy(sizePolicy1)
        self.triangulationLabel.setMaximumSize(QSize(16777215, 16777215))

        self.mainVerticalLayout.addWidget(self.triangulationLabel)

        self.triangulationHorizontalLayout = QHBoxLayout()
        self.triangulationHorizontalLayout.setObjectName(u"triangulationHorizontalLayout")
        self.triangulationSlider = QSlider(self.centralwidget)
        self.triangulationSlider.setObjectName(u"triangulationSlider")
        sizePolicy1.setHeightForWidth(self.triangulationSlider.sizePolicy().hasHeightForWidth())
        self.triangulationSlider.setSizePolicy(sizePolicy1)
        self.triangulationSlider.setMinimumSize(QSize(120, 0))
        self.triangulationSlider.setMaximumSize(QSize(16777215, 16777215))
        self.triangulationSlider.setMinimum(1)
        self.triangulationSlider.setMaximum(50)
        self.triangulationSlider.setValue(10)
        self.triangulationSlider.setOrientation(Qt.Orientation.Horizontal)

        self.triangulationHorizontalLayout.addWidget(self.triangulationSlider)

        self.triangulationValueLabel = QLabel(self.centralwidget)
        self.triangulationValueLabel.setObjectName(u"triangulationValueLabel")
        sizePolicy1.setHeightForWidth(self.triangulationValueLabel.sizePolicy().hasHeightForWidth())
        self.triangulationValueLabel.setSizePolicy(sizePolicy1)
        self.triangulationValueLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.triangulationHorizontalLayout.addWidget(self.triangulationValueLabel)


        self.mainVerticalLayout.addLayout(self.triangulationHorizontalLayout)

        self.alphaLabel = QLabel(self.centralwidget)
        self.alphaLabel.setObjectName(u"alphaLabel")
        sizePolicy1.setHeightForWidth(self.alphaLabel.sizePolicy().hasHeightForWidth())
        self.alphaLabel.setSizePolicy(sizePolicy1)
        self.alphaLabel.setMaximumSize(QSize(16777215, 16777215))

        self.mainVerticalLayout.addWidget(self.alphaLabel)

        self.alphaHorizontalLayout = QHBoxLayout()
        self.alphaHorizontalLayout.setObjectName(u"alphaHorizontalLayout")
        self.alphaSlider = QSlider(self.centralwidget)
        self.alphaSlider.setObjectName(u"alphaSlider")
        sizePolicy1.setHeightForWidth(self.alphaSlider.sizePolicy().hasHeightForWidth())
        self.alphaSlider.setSizePolicy(sizePolicy1)
        self.alphaSlider.setMinimumSize(QSize(120, 0))
        self.alphaSlider.setMinimum(-90)
        self.alphaSlider.setMaximum(90)
        self.alphaSlider.setOrientation(Qt.Orientation.Horizontal)

        self.alphaHorizontalLayout.addWidget(self.alphaSlider)

        self.alphaValueLabel = QLabel(self.centralwidget)
        self.alphaValueLabel.setObjectName(u"alphaValueLabel")

        self.alphaHorizontalLayout.addWidget(self.alphaValueLabel)


        self.mainVerticalLayout.addLayout(self.alphaHorizontalLayout)

        self.betaLabel = QLabel(self.centralwidget)
        self.betaLabel.setObjectName(u"betaLabel")
        sizePolicy1.setHeightForWidth(self.betaLabel.sizePolicy().hasHeightForWidth())
        self.betaLabel.setSizePolicy(sizePolicy1)

        self.mainVerticalLayout.addWidget(self.betaLabel)

        self.betaHorizontalLayout = QHBoxLayout()
        self.betaHorizontalLayout.setObjectName(u"betaHorizontalLayout")
        self.betaSlider = QSlider(self.centralwidget)
        self.betaSlider.setObjectName(u"betaSlider")
        sizePolicy1.setHeightForWidth(self.betaSlider.sizePolicy().hasHeightForWidth())
        self.betaSlider.setSizePolicy(sizePolicy1)
        self.betaSlider.setMinimumSize(QSize(120, 0))
        self.betaSlider.setMinimum(-90)
        self.betaSlider.setMaximum(90)
        self.betaSlider.setOrientation(Qt.Orientation.Horizontal)

        self.betaHorizontalLayout.addWidget(self.betaSlider)

        self.betaValueLabel = QLabel(self.centralwidget)
        self.betaValueLabel.setObjectName(u"betaValueLabel")

        self.betaHorizontalLayout.addWidget(self.betaValueLabel)


        self.mainVerticalLayout.addLayout(self.betaHorizontalLayout)

        self.polygonCheckBox = QCheckBox(self.centralwidget)
        self.polygonCheckBox.setObjectName(u"polygonCheckBox")
        self.polygonCheckBox.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.polygonCheckBox.sizePolicy().hasHeightForWidth())
        self.polygonCheckBox.setSizePolicy(sizePolicy1)
        self.polygonCheckBox.setMinimumSize(QSize(120, 0))
        self.polygonCheckBox.setMaximumSize(QSize(16777215, 16777215))
        self.polygonCheckBox.setChecked(True)

        self.mainVerticalLayout.addWidget(self.polygonCheckBox)

        self.meshCheckBox = QCheckBox(self.centralwidget)
        self.meshCheckBox.setObjectName(u"meshCheckBox")
        self.meshCheckBox.setMinimumSize(QSize(120, 0))
        self.meshCheckBox.setChecked(True)

        self.mainVerticalLayout.addWidget(self.meshCheckBox)

        self.fillCheckBox = QCheckBox(self.centralwidget)
        self.fillCheckBox.setObjectName(u"fillCheckBox")
        self.fillCheckBox.setMinimumSize(QSize(120, 0))
        self.fillCheckBox.setChecked(False)

        self.mainVerticalLayout.addWidget(self.fillCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainVerticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.mainVerticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"gk1-bezier-surface", None))
        self.triangulationLabel.setText(QCoreApplication.translate("MainWindow", u"Triangulation", None))
        self.triangulationValueLabel.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.alphaLabel.setText(QCoreApplication.translate("MainWindow", u"Alpha (Z)", None))
        self.alphaValueLabel.setText(QCoreApplication.translate("MainWindow", u"0\u00b0", None))
        self.betaLabel.setText(QCoreApplication.translate("MainWindow", u"Beta (X)", None))
        self.betaValueLabel.setText(QCoreApplication.translate("MainWindow", u"0\u00b0", None))
        self.polygonCheckBox.setText(QCoreApplication.translate("MainWindow", u"Polygon", None))
        self.meshCheckBox.setText(QCoreApplication.translate("MainWindow", u"Mesh", None))
        self.fillCheckBox.setText(QCoreApplication.translate("MainWindow", u"Fill", None))
    # retranslateUi

