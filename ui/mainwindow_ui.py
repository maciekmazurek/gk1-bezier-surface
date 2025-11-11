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
    QMainWindow, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

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
        self.mainVerticalLayout.setSpacing(3)
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

        self.kdLabel = QLabel(self.centralwidget)
        self.kdLabel.setObjectName(u"kdLabel")
        sizePolicy1.setHeightForWidth(self.kdLabel.sizePolicy().hasHeightForWidth())
        self.kdLabel.setSizePolicy(sizePolicy1)

        self.mainVerticalLayout.addWidget(self.kdLabel)

        self.kdHorizontalLayout = QHBoxLayout()
        self.kdHorizontalLayout.setObjectName(u"kdHorizontalLayout")
        self.kdSlider = QSlider(self.centralwidget)
        self.kdSlider.setObjectName(u"kdSlider")
        sizePolicy1.setHeightForWidth(self.kdSlider.sizePolicy().hasHeightForWidth())
        self.kdSlider.setSizePolicy(sizePolicy1)
        self.kdSlider.setMinimumSize(QSize(120, 0))
        self.kdSlider.setMaximum(100)
        self.kdSlider.setValue(50)
        self.kdSlider.setOrientation(Qt.Orientation.Horizontal)

        self.kdHorizontalLayout.addWidget(self.kdSlider)

        self.kdValueLabel = QLabel(self.centralwidget)
        self.kdValueLabel.setObjectName(u"kdValueLabel")

        self.kdHorizontalLayout.addWidget(self.kdValueLabel)


        self.mainVerticalLayout.addLayout(self.kdHorizontalLayout)

        self.ksLabel = QLabel(self.centralwidget)
        self.ksLabel.setObjectName(u"ksLabel")
        sizePolicy1.setHeightForWidth(self.ksLabel.sizePolicy().hasHeightForWidth())
        self.ksLabel.setSizePolicy(sizePolicy1)

        self.mainVerticalLayout.addWidget(self.ksLabel)

        self.ksHorizontalLayout = QHBoxLayout()
        self.ksHorizontalLayout.setObjectName(u"ksHorizontalLayout")
        self.ksSlider = QSlider(self.centralwidget)
        self.ksSlider.setObjectName(u"ksSlider")
        sizePolicy1.setHeightForWidth(self.ksSlider.sizePolicy().hasHeightForWidth())
        self.ksSlider.setSizePolicy(sizePolicy1)
        self.ksSlider.setMinimumSize(QSize(120, 0))
        self.ksSlider.setMaximum(100)
        self.ksSlider.setValue(50)
        self.ksSlider.setOrientation(Qt.Orientation.Horizontal)

        self.ksHorizontalLayout.addWidget(self.ksSlider)

        self.ksValueLabel = QLabel(self.centralwidget)
        self.ksValueLabel.setObjectName(u"ksValueLabel")

        self.ksHorizontalLayout.addWidget(self.ksValueLabel)


        self.mainVerticalLayout.addLayout(self.ksHorizontalLayout)

        self.mLabel = QLabel(self.centralwidget)
        self.mLabel.setObjectName(u"mLabel")
        sizePolicy1.setHeightForWidth(self.mLabel.sizePolicy().hasHeightForWidth())
        self.mLabel.setSizePolicy(sizePolicy1)

        self.mainVerticalLayout.addWidget(self.mLabel)

        self.mHorizontalLayout = QHBoxLayout()
        self.mHorizontalLayout.setObjectName(u"mHorizontalLayout")
        self.mSlider = QSlider(self.centralwidget)
        self.mSlider.setObjectName(u"mSlider")
        sizePolicy1.setHeightForWidth(self.mSlider.sizePolicy().hasHeightForWidth())
        self.mSlider.setSizePolicy(sizePolicy1)
        self.mSlider.setMinimumSize(QSize(120, 0))
        self.mSlider.setMinimum(1)
        self.mSlider.setMaximum(100)
        self.mSlider.setValue(50)
        self.mSlider.setOrientation(Qt.Orientation.Horizontal)

        self.mHorizontalLayout.addWidget(self.mSlider)

        self.mValueLabel = QLabel(self.centralwidget)
        self.mValueLabel.setObjectName(u"mValueLabel")

        self.mHorizontalLayout.addWidget(self.mValueLabel)


        self.mainVerticalLayout.addLayout(self.mHorizontalLayout)

        self.lightLabel = QLabel(self.centralwidget)
        self.lightLabel.setObjectName(u"lightLabel")
        sizePolicy1.setHeightForWidth(self.lightLabel.sizePolicy().hasHeightForWidth())
        self.lightLabel.setSizePolicy(sizePolicy1)

        self.mainVerticalLayout.addWidget(self.lightLabel)

        self.lightHorizontalLayout = QHBoxLayout()
        self.lightHorizontalLayout.setObjectName(u"lightHorizontalLayout")
        self.lightSlider = QSlider(self.centralwidget)
        self.lightSlider.setObjectName(u"lightSlider")
        sizePolicy1.setHeightForWidth(self.lightSlider.sizePolicy().hasHeightForWidth())
        self.lightSlider.setSizePolicy(sizePolicy1)
        self.lightSlider.setMinimumSize(QSize(120, 0))
        self.lightSlider.setMinimum(-10)
        self.lightSlider.setMaximum(10)
        self.lightSlider.setValue(5)
        self.lightSlider.setOrientation(Qt.Orientation.Horizontal)

        self.lightHorizontalLayout.addWidget(self.lightSlider)

        self.lightValueLabel = QLabel(self.centralwidget)
        self.lightValueLabel.setObjectName(u"lightValueLabel")

        self.lightHorizontalLayout.addWidget(self.lightValueLabel)


        self.mainVerticalLayout.addLayout(self.lightHorizontalLayout)

        self.surfaceColorLabel = QLabel(self.centralwidget)
        self.surfaceColorLabel.setObjectName(u"surfaceColorLabel")

        self.mainVerticalLayout.addWidget(self.surfaceColorLabel)

        self.surfaceColorHorizontalLayout = QHBoxLayout()
        self.surfaceColorHorizontalLayout.setObjectName(u"surfaceColorHorizontalLayout")
        self.solidRadioButton = QRadioButton(self.centralwidget)
        self.solidRadioButton.setObjectName(u"solidRadioButton")
        self.solidRadioButton.setChecked(True)

        self.surfaceColorHorizontalLayout.addWidget(self.solidRadioButton)

        self.textureRadioButton = QRadioButton(self.centralwidget)
        self.textureRadioButton.setObjectName(u"textureRadioButton")

        self.surfaceColorHorizontalLayout.addWidget(self.textureRadioButton)


        self.mainVerticalLayout.addLayout(self.surfaceColorHorizontalLayout)

        self.lightColorButton = QPushButton(self.centralwidget)
        self.lightColorButton.setObjectName(u"lightColorButton")

        self.mainVerticalLayout.addWidget(self.lightColorButton)

        self.surfaceColorButton = QPushButton(self.centralwidget)
        self.surfaceColorButton.setObjectName(u"surfaceColorButton")

        self.mainVerticalLayout.addWidget(self.surfaceColorButton)

        self.surfaceTextureButton = QPushButton(self.centralwidget)
        self.surfaceTextureButton.setObjectName(u"surfaceTextureButton")

        self.mainVerticalLayout.addWidget(self.surfaceTextureButton)

        self.animationButton = QPushButton(self.centralwidget)
        self.animationButton.setObjectName(u"animationButton")

        self.mainVerticalLayout.addWidget(self.animationButton)

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
        self.kdLabel.setText(QCoreApplication.translate("MainWindow", u"kd (diffusion)", None))
        self.kdValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.ksLabel.setText(QCoreApplication.translate("MainWindow", u"ks (specularity)", None))
        self.ksValueLabel.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.mLabel.setText(QCoreApplication.translate("MainWindow", u"m (gloss)", None))
        self.mValueLabel.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.lightLabel.setText(QCoreApplication.translate("MainWindow", u"Light source (Z)", None))
        self.lightValueLabel.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.surfaceColorLabel.setText(QCoreApplication.translate("MainWindow", u"Surface color", None))
        self.solidRadioButton.setText(QCoreApplication.translate("MainWindow", u"Solid", None))
        self.textureRadioButton.setText(QCoreApplication.translate("MainWindow", u"Texture", None))
        self.lightColorButton.setText(QCoreApplication.translate("MainWindow", u"Select light color", None))
        self.surfaceColorButton.setText(QCoreApplication.translate("MainWindow", u"Select surface color", None))
        self.surfaceTextureButton.setText(QCoreApplication.translate("MainWindow", u"Upload surface texture", None))
        self.animationButton.setText(QCoreApplication.translate("MainWindow", u"Pause animation", None))
    # retranslateUi

